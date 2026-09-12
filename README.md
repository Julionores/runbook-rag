# RunbookRAG

[![CI](https://github.com/Julionores/runbook-rag/actions/workflows/ci.yml/badge.svg)](https://github.com/Julionores/runbook-rag/actions/workflows/ci.yml)

Un assistant documentaire (RAG — Retrieval-Augmented Generation) qui répond aux questions d'une
équipe DevOps à partir de ses **runbooks internes** (PDF), en citant ses sources et en sachant
reconnaître qu'une question sort de son périmètre — plutôt que d'halluciner une réponse
plausible mais fausse.

> Projet réalisé par **Junior Tsafack Megnekeu** ([blog.jtmcloud.com](https://blog.jtmcloud.com) ·
> [GitHub](https://github.com/Julionores) ·
> [LinkedIn](https://www.linkedin.com/in/junior-tsafack-megnekeu-b673151b9)) — pièce d'un
> portfolio technique orienté Machine Learning. Voir aussi
> [`agent-matching-recrutement`](https://github.com/Julionores/agent-matching-recrutement),
> [`gradientforge`](https://github.com/Julionores/gradientforge),
> [`radar-risque-impaye`](https://github.com/Julionores/radar-risque-impaye),
> [`collecte-agricole-planner`](https://github.com/Julionores/collecte-agricole-planner),
> [`ticket-tide`](https://github.com/Julionores/ticket-tide),
> [`inspectline`](https://github.com/Julionores/inspectline), et l'ensemble du portfolio :
> [`devsecops-pipeline-reference`](https://github.com/Julionores/devsecops-pipeline-reference),
> [`securebank-api`](https://github.com/Julionores/securebank-api),
> [`postgresql-ha-repmgr`](https://github.com/Julionores/postgresql-ha-repmgr),
> [`iso27001-isms-toolkit`](https://github.com/Julionores/iso27001-isms-toolkit),
> [`dynamodb-streams-cdc-pipeline`](https://github.com/Julionores/dynamodb-streams-cdc-pipeline),
> [`aws-troubleshooting-challenge`](https://github.com/Julionores/aws-troubleshooting-challenge),
> [`s3-cross-region-replication`](https://github.com/Julionores/s3-cross-region-replication),
> [`aws-alb-deployment-patterns`](https://github.com/Julionores/aws-alb-deployment-patterns),
> [`aws-vpc-connectivity-patterns`](https://github.com/Julionores/aws-vpc-connectivity-patterns) et
> [`mcp-odoo-toolkit`](https://github.com/Julionores/mcp-odoo-toolkit).
> Ce projet accompagne le module 9 de mon
> [cours Machine Learning & Deep Learning](https://blog.jtmcloud.com/machine-learning/09-nlp-llm-rag/).

## Le scénario

Une équipe DevOps interne dispose de 5 runbooks (astreinte, escalade, sauvegardes, rollback,
bascule de base de données) en PDF. Un modèle de langage généraliste, seul, ne peut pas répondre
précisément à leurs questions — cette documentation n'a jamais fait partie de son entraînement.
Un **modèle local** est utilisé délibérément (plutôt qu'une API externe) : ces documents sont
sensibles et ne doivent jamais quitter l'infrastructure de l'entreprise.

## Le problème, démontré

```bash
python examples/rag_demo.py
```

```
=== LLM nu (sans documentation) ===
Question: Au bout de combien de temps un rollback de deploiement doit-il etre possible ?
Un rollback de déploiement est une opération qui permet aux développeurs d'annuler les
changements effectués dans leur application avant qu'ils ne soient en cours d'exécution.
Le délai pour un rollback de déploiement peut varier selon plusieurs facteurs, notamment :

1. **Durée du déploiement** : Les dépendances entre les services peuvent être complexes,
ce qui peut nécessiter des délais plus longs pour que tous les services soient désactivés.
...
```

Le modèle ne donne **aucune réponse concrète** — il esquive avec des généralités plausibles.

## La solution

```
=== Avec RAG ===
Reponse: Un rollback de déploiement doit être possible à partir de 10 minutes.
Sources citees: ['rollback.pdf', 'sauvegardes.pdf']
Score de confiance: 0.755
```

La bonne réponse (« 10 minutes », la vraie valeur du runbook), avec ses sources citées.

## Savoir dire « je ne sais pas »

```
=== Question hors domaine ===
Question: Quelle est la politique de remboursement des billets d'avion ?
Reponse: Cette question semble sortir de la documentation disponible.
Hors domaine detecte: True
Score: 0.377
```

Un score de similarité de 0,377 (contre 0,755 pour une question réellement couverte) déclenche
un refus explicite **avant même de charger le modèle de génération** — voir
`tests/test_generation.py::test_out_of_domain_question_never_loads_the_llm`.

## Pipeline

```
src/runbook_rag/
├── extraction.py  # pypdf : extraction + nettoyage en-tete/pied de page
├── retrieval.py   # sentence-transformers : embeddings + recherche par similarite
└── generation.py  # transformers : LLM local + assemblage RAG + seuil hors-domaine
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

8 tests couvrent l'extraction (suppression réelle de l'en-tête/pied de page générés), la
recherche sémantique, et le pipeline RAG — dont un test qui **mock** le modèle de génération
pour rester rapide et déterministe en CI, et un test qui garantit qu'une question hors domaine
ne déclenche jamais le chargement du LLM.

```
============================= 8 passed in 33.54s ==============================
```

## Installation

```bash
conda create -n runbook-rag python=3.11
conda activate runbook-rag
pip install -r requirements-dev.txt
python examples/generate_runbooks.py   # genere les PDF de demo
python examples/rag_demo.py
```

## Limites assumées

- Un document = un chunk : convient à des runbooks courts, un corpus plus long demanderait un
  découpage plus fin (par section, avec chevauchement).
- Un petit modèle local (Qwen2.5-0.5B) : suffisant pour ce prototype, un système de production
  arbitrerait entre un modèle local plus grand et une API, selon le compromis
  qualité/coût/confidentialité.
- Base vectorielle « maison » (une simple matrice NumPy) : adaptée à 5 documents, une base
  dédiée (FAISS, Chroma) serait nécessaire à plus grande échelle.

## Licence

MIT — voir [`LICENSE`](LICENSE). Projet à but pédagogique et de démonstration.
