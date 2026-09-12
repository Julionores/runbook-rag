"""Extraction et nettoyage de texte depuis des PDF de runbooks internes."""

import os
from pypdf import PdfReader


def extract_clean_text(pdf_path):
    """Extrait le texte d'un PDF, en retirant la premiere ligne (en-tete
    repetitif) et la derniere (pied de page repetitif) de chaque page."""
    reader = PdfReader(pdf_path)
    pages_nettoyees = []
    for page in reader.pages:
        lignes = page.extract_text().split("\n")
        pages_nettoyees.append("\n".join(lignes[1:-1]))
    return "\n".join(pages_nettoyees)


def load_corpus(pdf_dir):
    """Charge et nettoie tous les PDF d'un dossier. Retourne (chunks, sources),
    deux listes paralleles (texte nettoye, nom de fichier source)."""
    chunks, sources = [], []
    for filename in sorted(os.listdir(pdf_dir)):
        if not filename.lower().endswith(".pdf"):
            continue
        chunks.append(extract_clean_text(os.path.join(pdf_dir, filename)))
        sources.append(filename)
    return chunks, sources
