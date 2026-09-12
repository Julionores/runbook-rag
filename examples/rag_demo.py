"""Demo complete : genere le corpus, montre l'hallucination du LLM nu, puis
la reponse RAG exacte et sourcee, puis la detection d'une question hors
domaine."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from generate_runbooks import generate_runbooks  # noqa: E402

from runbook_rag import load_corpus, Retriever  # noqa: E402
from runbook_rag.generation import RunbookAssistant  # noqa: E402

RUNBOOKS_DIR = "runbooks"

if not os.path.isdir(RUNBOOKS_DIR):
    generate_runbooks(RUNBOOKS_DIR)

chunks, sources = load_corpus(RUNBOOKS_DIR)
print("Corpus charge:", sources)

retriever = Retriever(chunks, sources)
assistant = RunbookAssistant(retriever)

question = (
    "Au bout de combien de temps un rollback de deploiement doit-il etre possible ?"
)

print("\n=== LLM nu (sans documentation) ===")
print("Question:", question)
print(assistant.ask_without_context(question))

print("\n=== Avec RAG ===")
resultat = assistant.ask(question)
print("Reponse:", resultat["reponse"])
print("Sources citees:", resultat["sources"])
print("Score de confiance:", round(resultat["score"], 3))

print("\n=== Question hors domaine ===")
question_hs = "Quelle est la politique de remboursement des billets d'avion ?"
resultat_hs = assistant.ask(question_hs)
print("Question:", question_hs)
print("Reponse:", resultat_hs["reponse"])
print("Hors domaine detecte:", resultat_hs["hors_domaine"])
print("Score:", round(resultat_hs["score"], 3))
