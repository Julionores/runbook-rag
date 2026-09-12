import pytest

from runbook_rag import load_corpus, Retriever


@pytest.fixture(scope="module")
def retriever(runbooks_dir):
    chunks, sources = load_corpus(runbooks_dir)
    return Retriever(chunks, sources)


def test_search_retrieves_the_relevant_document(retriever):
    resultats = retriever.search(
        "Au bout de combien de temps un rollback est-il possible ?", top_k=2
    )
    assert resultats[0]["source"] == "rollback.pdf"


def test_search_results_are_sorted_by_score_descending(retriever):
    resultats = retriever.search("Quelle est la politique de sauvegarde ?", top_k=3)
    scores = [r["score"] for r in resultats]
    assert scores == sorted(scores, reverse=True)


def test_in_domain_question_scores_higher_than_out_of_domain(retriever):
    """Documente le comportement reel utilise pour detecter une question hors
    du perimetre documentaire (voir RunbookAssistant.ask)."""
    score_dans_domaine = retriever.best_score(
        "Au bout de combien de temps un rollback est-il possible ?"
    )
    score_hors_domaine = retriever.best_score(
        "Quelle est la politique de remboursement des billets d'avion ?"
    )
    assert score_dans_domaine > score_hors_domaine
