"""Recherche semantique 'maison' : embeddings normalises + produit scalaire,
sans base vectorielle dediee."""

import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


class Retriever:
    def __init__(self, chunks, sources, model_name=DEFAULT_MODEL):
        self.chunks = chunks
        self.sources = sources
        self.embedder = SentenceTransformer(model_name)
        self.embeddings = self.embedder.encode(chunks, normalize_embeddings=True)

    def search(self, question, top_k=2):
        """Retourne les top_k chunks les plus pertinents pour la question,
        sous forme de liste de dicts {source, chunk, score}, tries par score
        decroissant."""
        question_embedding = self.embedder.encode(question, normalize_embeddings=True)
        similarites = self.embeddings @ question_embedding
        indices_top = np.argsort(-similarites)[:top_k]
        return [
            {
                "source": self.sources[i],
                "chunk": self.chunks[i],
                "score": float(similarites[i]),
            }
            for i in indices_top
        ]

    def best_score(self, question):
        """Le meilleur score de similarite pour une question, utile pour
        detecter si elle sort du perimetre documentaire (voir RunbookAssistant)."""
        question_embedding = self.embedder.encode(question, normalize_embeddings=True)
        return float((self.embeddings @ question_embedding).max())
