import pytest

from runbook_rag import load_corpus, Retriever
from runbook_rag.generation import RunbookAssistant


@pytest.fixture(scope="module")
def retriever(runbooks_dir):
    chunks, sources = load_corpus(runbooks_dir)
    return Retriever(chunks, sources)


def test_out_of_domain_question_never_loads_the_llm(retriever):
    """Une question hors domaine doit etre rejetee par le seuil de similarite
    AVANT tout chargement du modele de generation -- verifie en s'assurant
    que le generateur reste non charge apres l'appel."""
    assistant = RunbookAssistant(retriever)
    resultat = assistant.ask(
        "Quelle est la politique de remboursement des billets d'avion ?"
    )

    assert resultat["hors_domaine"] is True
    assert resultat["sources"] == []
    assert assistant._generator is None  # jamais charge


def test_in_domain_question_calls_generation_with_retrieved_context(
    retriever, monkeypatch
):
    """Remplace le LLM reel par un faux generateur pour un test rapide et
    deterministe : verifie que le pipeline RAG assemble bien le contexte
    recupere avant de generer, sans dependre du temps d'inference reel."""
    assistant = RunbookAssistant(retriever)

    prompts_recus = []

    def faux_generate(prompt, max_new_tokens=120):
        prompts_recus.append(prompt)
        return "reponse simulee"

    monkeypatch.setattr(assistant, "_generate", faux_generate)

    resultat = assistant.ask(
        "Au bout de combien de temps un rollback est-il possible ?"
    )

    assert resultat["hors_domaine"] is False
    assert resultat["reponse"] == "reponse simulee"
    assert "rollback.pdf" in resultat["sources"]
    assert len(prompts_recus) == 1
    assert (
        "10 minutes" in prompts_recus[0]
    )  # le contexte recupere contient bien la reponse
