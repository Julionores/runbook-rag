from runbook_rag import extract_clean_text, load_corpus


def test_extraction_strips_repetitive_header_and_footer(runbooks_dir):
    import os

    path = os.path.join(runbooks_dir, "rollback.pdf")
    texte = extract_clean_text(path)

    assert "CloudOps Interne" not in texte  # en-tete retire
    assert "Document confidentiel" not in texte  # pied de page retire
    assert "10 minutes" in texte  # le contenu utile reste present


def test_load_corpus_returns_all_five_runbooks(runbooks_dir):
    chunks, sources = load_corpus(runbooks_dir)
    assert len(chunks) == 5
    assert len(sources) == 5
    assert "rollback.pdf" in sources


def test_load_corpus_chunks_are_non_empty(runbooks_dir):
    chunks, _ = load_corpus(runbooks_dir)
    assert all(len(chunk) > 100 for chunk in chunks)
