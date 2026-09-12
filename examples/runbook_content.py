"""Contenu des 5 runbooks DevOps fictifs utilises comme base documentaire du
RAG. Chaque entree : (titre_fichier, titre_affiche, paragraphes de contenu).
"""

RUNBOOKS = [
    (
        "astreinte",
        "Procedure d'astreinte",
        [
            "L'astreinte technique est assuree 24/7 par un ingenieur de garde, "
            "selon un planning tournant sur 4 personnes, chacune couvrant une "
            "semaine complete du lundi 9h au lundi suivant 9h.",
            "En cas d'alerte de criticite P1 (indisponibilite totale d'un "
            "service en production), l'ingenieur de garde doit accuser "
            "reception dans les 5 minutes via l'outil de paging, et ouvrir un "
            "incident dans le systeme de suivi dans les 15 minutes.",
            "Pour une alerte de criticite P2 (degradation partielle sans "
            "indisponibilite totale), le delai d'accuse de reception est "
            "porte a 30 minutes, sans obligation de reveil nocturne entre "
            "22h et 7h sauf aggravation.",
            "L'ingenieur de garde dispose d'un acces direct au compte AWS de "
            "production via un role IAM dedie ASTREINTE_ONCALL, valable 12 "
            "heures et journalise integralement par CloudTrail.",
        ],
    ),
    (
        "escalade",
        "Matrice d'escalade des incidents",
        [
            "Un incident P1 non resolu au bout de 30 minutes doit etre "
            "escalade au responsable technique d'astreinte (niveau 2), "
            "joignable par telephone selon le planning publie sur l'intranet.",
            "Un incident P1 non resolu au bout de 90 minutes declenche "
            "automatiquement une notification au directeur technique "
            "(niveau 3) et l'ouverture d'une cellule de crise si l'incident "
            "affecte plus de 10% des utilisateurs actifs.",
            "Les incidents de niveau P3 et P4 (bugs mineurs, degradations "
            "cosmetiques) ne suivent pas cette matrice d'escalade : ils sont "
            "traites selon le processus de ticketing standard, sans astreinte.",
            "Toute escalade doit etre tracee dans le systeme de suivi "
            "d'incidents, avec horodatage et justification, pour permettre "
            "un post-mortem complet une fois l'incident resolu.",
        ],
    ),
    (
        "sauvegardes",
        "Politique de rotation des sauvegardes",
        [
            "Les sauvegardes de base de donnees sont effectuees toutes les "
            "6 heures, avec une retention de 7 jours glissants pour les "
            "sauvegardes horaires et de 90 jours pour une sauvegarde "
            "quotidienne consolidee.",
            "Une sauvegarde complete mensuelle est conservee pendant 3 ans, "
            "sur un stockage distinct (compte AWS separe) pour se proteger "
            "d'une compromission du compte de production principal.",
            "Un test de restauration complet est realise chaque trimestre "
            "sur un environnement isole, avec verification automatisee de "
            "l'integrite des donnees restaurees avant validation du test.",
            "Le delai de restauration cible (RTO) pour la base de donnees "
            "principale est de 2 heures ; la perte de donnees maximale "
            "acceptable (RPO) est de 15 minutes.",
        ],
    ),
    (
        "rollback",
        "Procedure de rollback de deploiement",
        [
            "Tout deploiement en production doit pouvoir etre annule "
            "(rollback) en moins de 10 minutes, via la reactivation "
            "automatique de la version precedente du pipeline CI/CD.",
            "Un rollback est declenche manuellement par l'ingenieur "
            "d'astreinte des qu'un taux d'erreur applicatif depasse 5% "
            "pendant plus de 3 minutes consecutives apres un deploiement.",
            "Avant tout rollback de base de donnees (annulation d'une "
            "migration de schema), une validation du responsable technique "
            "d'astreinte est obligatoire, la reversibilite d'une migration "
            "n'etant jamais garantie automatiquement.",
            "Chaque rollback, qu'il reussisse ou echoue, doit faire l'objet "
            "d'une entree dans le journal de deploiement, consultable par "
            "toute l'equipe technique.",
        ],
    ),
    (
        "failover-bdd",
        "Playbook de bascule (failover) de base de donnees",
        [
            "En cas de panne du serveur de base de donnees primaire, une "
            "bascule automatique vers un serveur standby est declenchee par "
            "l'outil de supervision si l'indisponibilite depasse 30 secondes.",
            "La bascule automatique ne concerne que les pannes materielles "
            "ou reseau du serveur primaire ; une corruption de donnees "
            "detectee necessite une intervention manuelle et ne doit jamais "
            "declencher de bascule automatique, au risque de propager la "
            "corruption au serveur standby.",
            "Apres toute bascule, une verification manuelle de l'integrite "
            "des dernieres transactions est obligatoire avant de considerer "
            "l'incident clos, meme si le service est techniquement de "
            "nouveau disponible.",
            "Le nouveau serveur standby (l'ancien primaire, une fois "
            "reconstruit) doit etre resynchronise avant d'etre reintegre "
            "au cluster ; le reintegrer sans resynchronisation complete "
            "est strictement interdit par cette procedure.",
        ],
    ),
]
