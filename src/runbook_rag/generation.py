"""Assemblage complet du pipeline RAG : recherche puis generation, avec
detection des questions hors du perimetre documentaire."""

from transformers import pipeline

DEFAULT_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
SEUIL_HORS_DOMAINE = 0.5

PROMPT_TEMPLATE = (
    "Tu es un assistant support technique interne. Voici la documentation disponible :\n\n"
    "{contexte}\n\n"
    "Question : {question}\n"
    "Consigne : reponds uniquement a partir de la documentation ci-dessus. "
    "Si l'information n'y figure pas, dis explicitement que tu ne sais pas."
)


class RunbookAssistant:
    def __init__(
        self, retriever, model_name=DEFAULT_MODEL, seuil_hors_domaine=SEUIL_HORS_DOMAINE
    ):
        self.retriever = retriever
        self.model_name = model_name
        self._generator = None  # charge paresseusement : voir _get_generator()
        self.seuil_hors_domaine = seuil_hors_domaine

    def _get_generator(self):
        """Charge le LLM seulement au premier besoin reel de generation --
        les questions detectees hors domaine ne declenchent donc jamais le
        telechargement/chargement du modele."""
        if self._generator is None:
            self._generator = pipeline("text-generation", model=self.model_name)
        return self._generator

    def _generate(self, prompt, max_new_tokens=120):
        messages = [{"role": "user", "content": prompt}]
        result = self._get_generator()(
            messages, max_new_tokens=max_new_tokens, do_sample=False
        )
        return result[0]["generated_text"][-1]["content"]

    def ask_without_context(self, question, max_new_tokens=120):
        """Interroge le LLM nu, sans documentation -- pour diagnostiquer
        l'hallucination avant d'y remedier."""
        return self._generate(question, max_new_tokens=max_new_tokens)

    def ask(self, question, top_k=2, max_new_tokens=120):
        """Pipeline RAG complet : verifie d'abord que la question est dans le
        perimetre documentaire, recupere les chunks pertinents, puis genere
        une reponse ancree dans ces chunks. Retourne un dict avec la reponse,
        les sources citees, et le score de confiance de la recherche."""
        meilleur_score = self.retriever.best_score(question)
        if meilleur_score < self.seuil_hors_domaine:
            return {
                "reponse": "Cette question semble sortir de la documentation disponible.",
                "sources": [],
                "score": meilleur_score,
                "hors_domaine": True,
            }

        resultats = self.retriever.search(question, top_k=top_k)
        contexte = "\n\n".join(r["chunk"] for r in resultats)
        prompt = PROMPT_TEMPLATE.format(contexte=contexte, question=question)
        reponse = self._generate(prompt, max_new_tokens=max_new_tokens)

        return {
            "reponse": reponse,
            "sources": [r["source"] for r in resultats],
            "score": meilleur_score,
            "hors_domaine": False,
        }
