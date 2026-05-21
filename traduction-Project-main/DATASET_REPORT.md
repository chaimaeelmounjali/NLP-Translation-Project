# DATASET_REPORT.md
## Projet R&D — Traduction Automatique Darija (MT)
### Module Text Mining · Université · Année universitaire 2025–2026
### Encadrant : Pr. Imad HAFIDI

---

> **Note aux groupes 1 et 3 :** Les sections marquées `[GROUPE X — À COMPLÉTER]` sont réservées à votre contribution. Remplacez chaque placeholder par vos propres informations en suivant le même format que le Groupe 2. Ne modifiez pas les sections des autres groupes.

---

## Table des matières

1. [Sources des Données](#41--sources-des-données)
2. [Collecte & Nettoyage](#42--collecte--nettoyage)
3. [Annotation du Gold Dataset](#43--annotation-du-gold-dataset)
4. [Labellisation Semi-Automatique avec IA](#44--labellisation-semi-automatique-avec-ia)
5. [Vérification et Validation](#45--vérification-et-validation)
6. [Analyse des Erreurs de l'IA](#46--analyse-des-erreurs-de-lia)
7. [Statistiques de Performance](#47--statistiques-de-performance)
8. [Correction des Erreurs](#48--correction-des-erreurs)
9. [Statistiques du Dataset](#49--statistiques-du-dataset)
10. [Limites](#410--limites)
11. [Améliorations](#411--améliorations)

---

# 4.1 🌍 Sources des Données

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Décrivez ici vos propres sources (sites web, réseaux sociaux, forums, datasets publics, etc.). Répondez aux points suivants :
> - Quelles sources avez-vous utilisées ? (Noms, URLs si applicable)
> - Pourquoi avez-vous choisi ces sources ?
> - Description des données collectées
> - Date de collecte
> - Type de langue : Arabe / Darija / Arabizi / Mixte
> - Observations sur la qualité des données à la réception
> - Problèmes rencontrés dès la collecte
> - Avantages de vos sources par rapport à d'autres alternatives

**Sources utilisées :**
Notre corpus repose sur un "Silver Standard" fourni au démarrage du projet, qui consiste en un pack de données pré-alignées (via des modèles d'IA tels que Atlas ou Gemini et des bases existantes). Il est structuré en deux fichiers :
- `silver_shard_1.csv` (~9 000 lignes) — Set d'entraînement (Training Set).
- `gold_shard_1.csv` (~1 000 lignes) — Set de test (Holdout Test).

**Pourquoi ces sources ?**
Ce corpus s'inscrit dans une démarche pédagogique et scientifique pour passer d'un "Silver Standard" bruité à un "Gold Standard" de haute qualité dédié à l'entraînement du modèle de traduction AraT5v2.

**Type de langue :**
Les données sont multilingues :
- **Darija (Script Arabe)** : `darija_arabic`
- **Darija (Arabizi)** : `darija_arabizi` (translittération latine avec chiffres phonétiques)
- **Anglais** et **Arabe Standard Moderne (MSA)**

**Date de collecte :**
Corpus fourni au début du projet, Année universitaire 2025–2026.

**Qualité des données à la réception et Problèmes rencontrés :**
La qualité initiale montrait de nombreux défauts inhérents aux générations "Silver" automatisées (IA) :
1. **Arabizi incorrect (73,6%)** : L'IA d'origine réalisait souvent de la translittération "lettre-à-lettre" depuis l'arabe, perdant l'authenticité de la prononciation rwapa/marocaine (ex: *al-maghrib* au lieu du terme naturel *lmeghrib*).
2. **Erreurs syntaxiques** : Omissions de particules temporelles fondamentales de la Darija (ex: non-utilisation de "Rah" pour le présent continu.
3. **Bruit Textuel** : Fuites de script (Script leakage) et erreurs d'alignement.

**Avantage :** 
L'avantage principal réside dans le volume préexistant (10 000 lignes alignées), éliminant la phase fastidieuse de crawling/scraping, et permettant de se concentrer sur l'audit, la validation et l'expertise linguistique.

---

## 🟡 Groupe 2 — Yassine Boumhand & Abdourazak Akillou Illa

**Sources utilisées :**
Le corpus du Groupe 2 repose sur des données brutes pré-fournies dans le cadre du projet, structurées en deux shards :
- `unified_shard_2.csv` (~9 005 lignes) — Silver Standard
- `gold_shard_2.csv` (~1 003 lignes) — Gold Standard

**Pourquoi ces sources ?**
Ces shards constituent la portion assignée au groupe dans le cadre d'un découpage coordonné entre tous les groupes participants. L'objectif est de construire un corpus parallèle Darija–Anglais–MSA représentatif et de haute qualité, utilisable pour l'entraînement et l'évaluation du modèle AraT5v2.

**Type de langue :**
- Darija marocaine en script arabe (`darija_arabic`) — zéro caractère latin
- Darija en translittération latine phonétique (`darija_arabizi`) — sons arabes notés avec chiffres phonétiques (7, 9, 3)
- Traductions en anglais et en arabe standard moderne (MSA)

**Date de collecte :** Données brutes reçues au démarrage du projet — Année universitaire 2025–2026 (traitement réalisé en avril 2026).

**Qualité des données à la réception :**
Les données brutes présentaient plusieurs artefacts issus de pipelines NLP antérieurs : tokens `<unk>`, séquences `@@` et `@-@` (tokenisation BPE), espaces doubles, et cas de code-switching avec des fragments Wikipedia en français ou en anglais insérés dans du texte arabe. Une analyse exploratoire préalable (EDA) a permis de quantifier ces anomalies avant toute annotation :

| Issue | Description | Lignes | % |
|---|---|---|---|
| 1 | Arabe dans colonne Arabizi | 183 | 1,83% |
| 2 | Latin dans colonne Darija Arabic | 37 | 0,37% |
| 3 | Arabe dans colonne English | 2 | 0,02% |
| 4 | Champs vides (English / MSA) | 0 | 0,00% |
| **Total anomalies** | | **222** | **2,22%** |

> **Note sur l'Issue 2** : Les 37 lignes contenant des caractères latins dans `darija_arabic` sont en grande partie acceptables — elles contiennent des formules mathématiques (ex. : `x = 78`, `E = mc²`), des codes ISBN, ou des scores sportifs universels qui n'ont pas de translittération arabe standard. Cette exception est documentée dans le guide d'annotation.

**Avantages de cette source :**
- Données déjà segmentées et catégorisées par classe de longueur (A, B, C, D)
- Distribution équilibrée entre les 4 classes (A : 25,7%, B : 24,5%, C : 25,7%, D : 24,1%), garantissant un entraînement uniforme du modèle AraT5v2
- Structure tabulaire cohérente avec 9 colonnes définies
- Volume suffisant (10 008 lignes) pour constituer un training set représentatif

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

Nous travaillons sur le **shard 3** du projet, c’est-à-dire la portion qui nous a été assignée dans le découpage global. Concrètement, nous sommes partis des fichiers suivants : le silver brut `shards/silver_9k_shards/silver_shard_3.csv` (élargi à **9 000 lignes** selon les nouvelles directives), le gold de référence `shards/gold_1k_shards/gold_shard_3.csv` (**1 000 lignes**), ainsi que les corrections gold partielles.

Le corpus est **parallèle** : pour chaque exemple, on dispose de la Darija en arabe (`darija_arabic`), de la même phrase en arabizi (`darija_arabizi`), puis des traductions en anglais (`english`) et en arabe standard (`modern_standard_arabic`). Les données ont été reçues dans le cadre de l’année 2025–2026, et notre traitement (nettoyage + corrections + contrôles) a été finalisé en avril 2026 pour atteindre le seuil de 9 000 lignes silver.

À l’arrivée, ce qui nous a le plus marqué, c’est l’**hétérogénéité** des statuts initiaux (`GENERATED`, `PARTIALLY VALIDATED`) et la présence d'artefacts machine (`<unk>`, `@-@`). Notre objectif a été de **re-stabiliser** la cohérence entre les colonnes tout en augmentant le volume, en veillant à ce que le nettoyage ne supprime pas de données sémantiques essentielles (conservation des stop words).

**Observations sur la qualité initiale (Shard 3) :**
| Issue | Description | Observation |
|---|---|---|
| Artefacts machine | Présence de `<unk>` et `@-@` | ~80% des lignes |
| Statuts hétérogènes | Mélange de statuts | 6 801 `GENERATED`, 2 199 `PARTIALLY VALIDATED` |
| Longueurs variables | Phrases de A à D | Distribution équilibrée (moyenne 108 chars en Darija) |
| Alignement Gold | Mismatch IDs | Corrigé par script de fusion avec fallback |

---

# 4.2 🧹 Collecte & Nettoyage

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Décrivez votre pipeline de collecte et de nettoyage :
> - Méthode de collecte : scraping / API / collecte manuelle ?
> - Outils utilisés (BeautifulSoup, Scrapy, Selenium, etc.)
> - Étapes de nettoyage réalisées : suppression du bruit, doublons, normalisation, encodage
> - Difficultés spécifiques à votre collecte

**Méthode de collecte :**
Le dataset a été fourni sous forme de fichiers CSV prêts à être ingérés, ne nécessitant pas de scraping web.

**Étapes de nettoyage :**
L'Analyse Exploratoire des Données (EDA) de la Phase 1 (via les notebooks `EDA.ipynb` et `nettoyage.ipynb`) a validé l'intégrité globale (0 doublon trouvé). Le processus de nettoyage s'est déroulé comme suit :
1. **Nettoyage par expressions régulières (Regex) en Python** : Un script de normalisation a été appliqué aux quatre colonnes textuelles.
2. **Identification des anomalies (DQA)** : Audit systématique de la longueur des phrases, des statuts initiaux (`GENERATED`, `PARTIALLY VALIDATED`) et des distributions de mots pour cibler les nettoyages. 

**Difficultés spécifiques :**
Il a fallu concevoir des regex robustes pour gérer les "fuites de script", sans détériorer les mots d'origine étrangère ("emprunts") fortement présents en Darija. Le résultat du nettoyage a donné lieu à la scission propre de `silver_shard_1_clean.csv` et `gold_shard_1_clean.csv`.

---

## 🟡 Groupe 2

**Méthode de collecte :**
Les données ont été reçues directement sous forme de fichiers CSV pré-structurés. Aucun scraping ni appel API externe n'a été nécessaire pour l'acquisition des données brutes.

**Analyse exploratoire préalable (EDA) :**
Avant toute annotation, les deux datasets bruts (Silver et Gold) ont été concaténés pour une analyse globale. Cette étape a permis de visualiser la distribution des classes, l'état des statuts initiaux, et de détecter les anomalies DQA de manière systématique (cf. section 4.1).

**Étapes de nettoyage (DQA — Data Quality Assurance) :**
Un protocole DQA strict a été appliqué manuellement pour le Gold Standard et intégré au prompt IA pour le Silver Standard :

1. **Suppression du bruit** : suppression des tokens `<unk>`, `@@`, `@-@` et normalisation des espaces doubles. Lorsque `<unk>` apparaît, le modèle est instruit de le remplacer par le mot logique selon le contexte.
2. **Traitement des phrases tronquées** : simplification pour conserver un sens complet
3. **Contrainte script arabe** : le champ `darija_arabic` ne doit contenir aucun caractère latin — les mots étrangers y sont translittérés en arabe (ex. : Xbox One → أكس بوكس ون) ; exception tolérée pour les formules mathématiques universelles
4. **Normalisation de l'arabizi** : le champ `darija_arabizi` respecte la convention phonétique marocaine avec chiffres (ح → 7, ق → 9, ع → 3) ; mots étrangers conservés dans leur alphabet d'origine
5. **Fidélité sémantique** : traductions anglaises et MSA au registre naturel de locuteur natif, sans traduction littérale ni sur-formalisation
6. **Conservation des noms propres** : les noms propres sont maintenus en anglais dans toutes les colonnes
7. **Code-switching** : géré naturellement, sans forcer une « pureté » linguistique artificielle

**Normalisation de la structure :**
Chaque ligne du livrable final respecte les 9 colonnes définies (`data_id`, `id`, `classe`, `darija_arabic`, `darija_arabizi`, `english`, `modern_standard_arabic`, `status`, `dataset_type`). Les lignes ne respectant pas ce schéma ont été corrigées ou écartées.

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

Nous n’avons pas collecté le corpus par scraping : nous sommes repartis des **CSV fournis** dans le cadre du projet. Notre travail a consisté à **nettoyer, harmoniser et contrôler** le shard 3.

**Pipeline de nettoyage technique :**
Pour traiter les 9 000 lignes du silver, nous avons développé un pipeline Python robuste (`clean_silver_shard_3_corrected.py`) intégrant les règles suivantes :
1. **Normalisation Unicode** : Unescape HTML, suppression des artefacts globaux (`<unk>`, `@-@`), et normalisation des espaces.
2. **Conservation Sémantique (`--skip-stopwords`)** : Contrairement aux approches NLP classiques, nous avons désactivé la suppression des *stop words* pour préserver la structure naturelle des phrases Darija, essentielle pour les modèles de type T5.
3. **Normalisation Script** : Application de règles spécifiques pour l'arabe (Alef variants, Ta Marbuta) et l'arabizi (réduction des répétitions de caractères).

Techniquement, nous avons utilisé Python (pandas + regex), l’API OpenAI (GPT-4o-mini), et des notebooks d’EDA comparatifs pour valider chaque étape.

---

# 4.3 🏷️ Annotation du Gold Dataset

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Décrivez votre processus d'annotation manuelle du Gold dataset :
> - Combien de lignes constituent votre Gold Standard ?
> - Qui a annoté (noms des membres) ?
> - Quel outil avez-vous utilisé (Label Studio, Google Sheets, autre) ?
> - Quelles règles d'annotation avez-vous suivies ?
> - Quelles difficultés avez-vous rencontrées ?

**Volume annoté :**
1 000 échantillons (`gold_shard_1_clean.csv`).

**Qui a annoté ?**
Ikram EL MENHI et Abderrahim AZEROUAL.

**Outil utilisé :**
L'interface **Label Studio**, configurée spécifiquement pour le projet avec des blocs XML adaptatifs et du CSS personnalisé (polices Poppins et Noto Sans Arabic, codes couleurs distincts).

**Règles linguistiques d'annotation :**
1. **Racines Sémitiques** : Vérification systématique des racines trilitères.
2. **Articles Définis** : Assimilation correcte en Darija .
3. **Pronoms et Particules temporelles** : Obligation d'incorporer les modificateurs de temps comme "Rah" pour restaurer le parler continu authentique.
4. **Arabizi et Transcription Phonétique** : Remplacement de l'orthographe "lettre-à-lettre" par une transcription phonétique exploitant les chiffres standardisés (3, 7, 9, etc.).
5. **Critères de rejet** : Incohérences totales, non-sens linguistique, ou traductions/MSA complètement hors sujet.

**Difficultés rencontrées :**
La restitution du dialecte marocain authentique. L'IA originelle ayant lissé la phonétique, 73,6% de la translittération Arabizi a nécessité un redressement ("oralisation") manuel. Les règles sémitiques n'étaient souvent pas applicables aux racines étrangères (emprunts linguistiques).

---

## 🟡 Groupe 2

**Méthode d'annotation :**
L'annotation du Gold Standard est **100% manuelle**, sans aucune intervention d'IA. Ce parti pris est fondamental : le Gold Standard constitue la vérité terrain (ground truth) utilisée pour l'évaluation finale du modèle AraT5v2, et toute contamination par un modèle de langage compromettrait la validité de cette évaluation.

**Outil utilisé :** Label Studio (interface web d'annotation)

**Qui a annoté ?**
L'intégralité de l'annotation manuelle du Gold Standard a été réalisée par **Yassine Boumhand**, locuteur natif de la Darija marocaine. Abdourazak Akillou Illa, membre du groupe originaire du Niger, n'est pas locuteur natif de la Darija et n'a donc pas participé à cette phase d'annotation — une tâche qui exige une maîtrise fine des nuances dialectales, des registres oraux, et des conventions de translittération arabizi propres au Maroc.

**Règles d'annotation appliquées :**
Les règles DQA détaillées en section 4.2 ont été appliquées de manière stricte lors de la saisie manuelle dans Label Studio. En particulier :
- Aucun caractère latin dans `darija_arabic` (exception : formules mathématiques universelles)
- Chiffres phonétiques obligatoires dans `darija_arabizi`
- Traductions naturelles, non littérales, au registre de locuteur natif
- Noms propres conservés en anglais

**Difficultés rencontrées :**
- L'annotation manuelle de ~1 003 lignes représente un travail chronophage et solitaire, nécessitant une concentration soutenue pour maintenir la cohérence des conventions sur toute la durée — particulièrement exigeant lorsqu'un seul annotateur natif est disponible
- Certaines phrases de classe D (très longues) présentent des structures complexes où plusieurs lectures sémantiques coexistent, rendant le choix de traduction MSA non trivial
- Les cas de code-switching intensif (darija + français + anglais dans une même phrase) ont requis un arbitrage sur la langue dominante de la traduction cible

**Résultat :**

| Métrique | Valeur |
|---|---|
| Lignes annotées manuellement | 1 003 |
| Statut final | 100% VALIDATED |
| Intervention IA | Aucune |
| Valeurs manquantes | 0 |
| Doublons | 0 |

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

Sur le gold, nous avons effectué une **correction 100% manuelle** de l'intégralité du shard 3 (**1 000 lignes**). Ce choix méthodologique garantit que le Gold Standard, qui sert de vérité terrain pour l'évaluation, n'a été contaminé par aucun processus automatisé ou script de fusion complexe.

Les corrections ont été réalisées par **Yahya Sahnoun** et **Chaimae El Monjali**. Le processus a consisté en une relecture attentive de chaque segment pour assurer la cohérence entre les quatre colonnes (Darija Arabe, Arabizi, Anglais, MSA).

Nos règles étaient strictes : fidélité absolue au sens original, respect des conventions orthographiques pour l'arabe standard, et translittération arabizi naturelle utilisant les chiffres phonétiques (7, 9, 3).

La difficulté principale a été de traiter les phrases longues (Classe D) et les expressions idiomatiques de la Darija, nécessitant parfois des arbitrages manuels fins pour conserver la nuance culturelle tout en assurant une traduction anglaise fluide.

---

# 4.4 🤖 Labellisation Semi-Automatique avec IA

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Détaillez votre approche de labellisation semi-automatique :
> - Nom **exact** du modèle utilisé (ex. : `gpt-4o`, `claude-3-5-sonnet-20241022`, `llama-3.3-70b`) — **OBLIGATOIRE d'être précis**
> - API utilisée ou modèle local ?
> - Type de prompt utilisé (zero-shot, few-shot, avec rôle ?)
> - Paramètres clés (température, max_tokens, batch size)
> - Comment les résultats ont-ils été intégrés à votre workflow ?

**Modèle utilisé :**
`GPT-4.1-mini` via l'API OpenAI.

**API ou Modèle Local ?**
API REST OpenAI. (Le modèle local `Atlas-Chat-2B` a aussi été évalué pour sa capacité brute, mais a révélé des lacunes sans fine-tuning).

**Type de prompt utilisé :**
Prompt ultra-structuré envoyé au modèle avec les segments suivants :
- **Rôle expert** : *"You are an expert Moroccan linguist. Correct, normalize, and validate this Darija entry."*
- **Règles Strictes (STRICT RULES)** : Pour contraindre la génération (Darija arabic only, Arabizi avec chiffres, fidélité sémantique).
- **GOLD EXAMPLES** : Formatage d'exemple forçant l'IA à renvoyer un objet JSON standardisé (`darija_arabic`, `darija_arabizi`, `english`, `msa`).

**Paramètres clés et architecture du pipeline :**
Le traitement par l'API s'est fait sur ~9000 lignes (`silver_shard_1_clean.csv`) dans un script (`correction_silver.ipynb`).
- **Gestion des limites (Rate Limit)** : `DELAI_ENTRE_REQUETES = 1` seconde (environ 60 req/min).
- **Robustesse (Retry mechanism)** : Boucle jusqu'à 3 tentatives (MAX_RETRIES) par ligne.
- **Auto-Sauvegarde** : Exportation itérative dans un fichier tampon `EN_COURS.csv`.

**Comment les résultats ont été intégrés :**
Une fois le résultat JSON renvoyé et testé par un "Regex Fallback" validant la structure, les lignes ont été mises à jour dans le Dataframe avec un nouveau statut `AI_REVIEWED`.

---

## 🟡 Groupe 2

**Modèle utilisé :** `gpt-4o-mini` — OpenAI API (version commerciale payante)

**Pourquoi ce modèle ?**
Dans un premier temps, nous avons testé **LLaMA 3.1 8B** puis **LLaMA 3.3 70B** via l'API gratuite Groq. Cette approche a été abandonnée pour trois raisons cumulées :
1. Qualité insuffisante sur les phrases complexes en Darija (classes C et D)
2. Quotas journaliers trop limités (500K tokens/compte), imposant la création de 4 comptes et une rotation manuelle des clés API
3. Débit effectif très lent (~5h) en raison des pauses forcées entre appels

La migration vers GPT-4o-mini a résolu ces trois problèmes : qualité nettement supérieure sur la Darija et le code-switching, absence totale de contrainte de quota, intégration directe avec Label Studio via API REST, et durée d'exécution réduite à ~2h (~$1,80 USD pour les 9 005 lignes).

| Critère | LLaMA/Groq (testé, abandonné) | GPT-4o-mini (retenu) |
|---|---|---|
| Coût | Gratuit | Payant (~$1,80 pour 9 005 lignes) |
| Qualité Darija | Correcte | Excellente |
| Code-switching | Partiel | Robuste |
| Gestion des quotas | Rotation de 4 clés | Aucune rotation nécessaire |
| Intégration Label Studio | Non (script externe) | Oui (API REST native) |
| Débit effectif | ~5h (rate limit) | ~2h |

**Type de prompt utilisé :** Role + Structured Output Prompt, combinant trois techniques :
- **Role Prompting** : `"Tu es un expert en linguistique marocaine et traducteur professionnel Darija vers Anglais et MSA..."` — ancre le registre attendu et améliore la qualité des sorties
- **Instruction Chaining** : règles de nettoyage numérotées guidant le modèle étape par étape sur les cas limites (artefacts, phrases tronquées, `<unk>`)
- **Constrained Generation** : format strict en 4 lignes préfixées (`DARIJA_ARABIC:`, `DARIJA_ARABIZI:`, `ENGLISH:`, `MSA:`) garantissant un parsing automatique fiable

**Paramètres de configuration du pipeline :**

| Paramètre | Valeur | Rôle |
|---|---|---|
| `model` | `gpt-4o-mini` | Identifiant du modèle |
| `temperature` | `0,1` | Quasi-déterminisme — sorties stables et reproductibles |
| `max_tokens` | `500` | Suffisant pour 4 lignes courtes |
| `BATCH_SIZE` | `20` | Lignes traitées par lot |
| `SLEEP_BETWEEN` | `0,5s` | Pause entre appels (respect des rate limits) |
| `MAX_RETRIES` | `3` | Tentatives automatiques en cas d'erreur réseau |

**Intégration avec Label Studio :**
L'architecture du pipeline évite tout import/export manuel de CSV grâce à l'API REST de Label Studio :
1. **Chargement** : récupération de toutes les tâches du projet via `ls.tasks.list(project=PROJECT_ID)`
2. **Appel API** : GPT-4o-mini génère les 4 colonnes cibles pour chaque tâche
3. **Push automatique** : création d'une prédiction via `ls.predictions.create(task=task.id, result=result)`
4. **Validation en masse** : *Retrieve Annotations from Predictions* bascule toutes les prédictions au statut `VALIDATED` en un seul clic

Paramètres de connexion : Access Token généré depuis `Settings → Access Token`, URL projet `http://localhost:8080` (Project ID : 12).

**Résilience du pipeline :**
En cas d'interruption, le script implémente une reprise automatique : il identifie les lignes déjà traitées et reprend exactement là où il s'est arrêté. Une sauvegarde intermédiaire est effectuée toutes les 10 lignes.

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

Nous utilisons l’API OpenAI, avec `gpt-4o-mini` comme modèle principal pour les passes de correction “à gros volume”. Pour la partie **contrôle sémantique hybride** (embeddings + décision / correction LLM), le script `hybrid_semantic_consistency.py` s’appuie sur `text-embedding-3-small` (dimension 1536) et sur `gpt-4o-mini` lorsqu’il faut creuser un cas ambigu.

**Configuration du Pipeline IA :**
- **Modèle de correction** : `gpt-4o-mini`
- **Modèle d'Embeddings** : `text-embedding-3-small`
- **Stratégie** : Zero-shot avec instructions de formatage strictes (JSON/PREFIX).
- **Paramètres** : Température `0.1`, Top-P `1.0`, Max Tokens `4096`.
- **Système de Reprise** : Checkpointing par ligne pour gérer les erreurs d'API (Rate Limits).

Côté prompting, nous restons sur une logique **très guidée** : consignes claires sur la préservation du sens dialectal, sortie structurée pour pouvoir la parser proprement, et température basse pour limiter la variabilité inutile. L'IA n'est pas utilisée comme un simple traducteur, mais comme un agent de nettoyage intelligent capable de détecter si une correction est réellement nécessaire (flag `CORRECTED` vs `CONSISTENT`).

---

# 4.5 🔍 Vérification et Validation

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Décrivez votre méthode de vérification des labels générés par l'IA :
> - Avez-vous fait une relecture manuelle complète, un échantillonnage, ou une autre méthode ?
> - Combien de lignes ont été vérifiées manuellement ?
> - Qui a vérifié (noms) ?
> - Quel outil ou interface avez-vous utilisé pour la validation ?

**Méthode de vérification :**
Pour le Silver Set corrigé par l'API (9 000 lignes), une relecture exhaustive étant impraticable, nous avons opté pour une **Validation ciblée par échantillonnage (Spot-Checking sur Label Studio)**.

**Focus de l'échantillonnage :**
Nous avons priorisé la vérification des entrées :
1. Dont le texte cible divergeait trop sémantiquement de l'original.
2. Ayant une très forte complexité de translittération.

**Qui a vérifié :**
Un sous-échantillon ciblé a été importé dans Label Studio et vérifié par l'équipe (Ikram EL MENHI et Abderrahim AZEROUAL) afin de combattre les biais résiduels.

**Outil utilisé :**
L'interface de validation **Label Studio**. L'objectif clé de cette passe humaine post-API était de contrecarrer le phénomène de l'"hyper-correction" où l'IA tend parfois à normaliser la Darija vers l'Arabe Classique (MSA) perdant ainsi l'authenticité de la langue parlée.

---

## 🟡 Groupe 2

**Méthode de validation : Spot-Checking Stratifié par classe (1%/classe)**

Relire manuellement les 9 005 lignes du Silver Standard est statistiquement inutile et pratiquement impossible sans introduire de la fatigue annotateur — phénomène documenté en NLP où la qualité des corrections diminue significativement après environ 500 lignes consécutives. De plus, le Silver dataset étant ordonné aléatoirement, un échantillonnage positionnel (début/milieu/fin) aurait produit une distribution de classes imprévisible, sous-représentant potentiellement les phrases les plus complexes (classe D).

**Pourquoi stratifier par classe ?**
En triant d'abord par classe puis en prélevant **1% de chaque strate séparément**, on garantit une représentation équilibrée de chaque niveau de complexité linguistique (20 lignes par classe), indépendamment de la distribution aléatoire du corpus.

**Justification statistique du taux de 1% :**
Le taux de 1% est justifié par un raisonnement statistique formel. Avec n = 20 lignes par classe et une qualité observée p ≈ 0,98, l'intervalle de confiance à 95% est :

> IC₉₅% = 0,98 ± 1,96 × √(0,98 × 0,02 / 20) = **[91,8% ; 100%]**

La borne inférieure reste largement au-dessus du seuil acceptable (BLEU 30). Augmenter l'échantillon à 5% ou 10% n'aurait pas modifié cette conclusion.

**Protocole d'échantillonnage :**

| Sonde | Classe | Lignes totales | Échantillonnées (1%) |
|---|---|---|---|
| Sonde A | Classe A (phrases courtes) | 2 323 | 20 |
| Sonde B | Classe B (phrases moyennes) | 2 202 | 20 |
| Sonde C | Classe C (phrases longues) | 2 319 | 20 |
| Sonde D | Classe D (très longues) | 2 161 | 20 |
| **Total** | | **9 005** | **80 lignes** |

**Qui a vérifié ?**
La vérification humaine des 80 lignes a été réalisée par **Yassine Boumhand**, seul locuteur natif de la Darija marocaine dans le groupe, garantissant la pertinence linguistique des jugements de qualité. Abdourazak Akillou Illa, originaire du Niger et non-locuteur de la Darija, n'est pas intervenu dans cette phase de validation.

**Métriques d'évaluation utilisées :**
Deux métriques complémentaires ont été calculées sur les 80 lignes spot-checkées, en comparant les sorties GPT-4o-mini aux corrections humaines :

- **BLEU** (*Bilingual Evaluation Understudy*) : mesure la précision des n-grammes — standard de l'industrie MT. Appliqué sur les colonnes `english` et `modern_standard_arabic`.
- **chrF++** : métrique basée sur les caractères, plus adaptée aux langues morphologiquement riches comme la Darija et l'Arabe Standard. Appliqué sur toutes les colonnes (`english`, `modern_standard_arabic`, `darija_arabic`, `darija_arabizi`).

> **Note :** BLEU n'est pas appliqué sur la Darija car c'est la langue *source* — GPT effectue du nettoyage et non une traduction. chrF++ reste valide car il mesure la similarité caractère par caractère, adaptée à l'évaluation de corrections orthographiques.

**Résultats globaux du spot-checking :**

| Métrique | Score global | Classe A | Classe B | Classe C/D |
|---|---|---|---|---|
| BLEU English | **97,3** | 72,5 | 99,6 | ~99 |
| chrF++ English | **98,5** | 80,6 | 100,0 | ~99–100 |
| BLEU MSA | **97,2** | 68,6 | 98,8 | ~99 |
| chrF++ MSA | **98,3** | 76,7 | 99,8 | ~100 |

> **Interprétation :** Les scores légèrement inférieurs en Classe A (BLEU ~72) ne reflètent pas une erreur de qualité — ils s'expliquent par la **variabilité naturelle des traductions courtes** : pour une phrase de 3 mots, plusieurs formulations correctes coexistent (*"Thank you"* vs *"Thanks a lot"* vs *"Many thanks"*), ce qui pénalise mécaniquement le score BLEU sans que la traduction GPT soit incorrecte. Tous les scores dépassent largement le seuil bonne qualité (50 BLEU) pour une langue low-resource.

**Décision de validation :**
Les résultats du spot-checking confirment statistiquement que GPT-4o-mini produit des traductions de haute qualité sur l'ensemble du Silver Standard. La validation en masse via **"Retrieve Annotations from Predictions"** dans Label Studio a été appliquée, basculant l'intégralité des 9 005 prédictions au statut `VALIDATED`.

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

Notre validation repose sur un **contrôle hybride** : une analyse statistique via EDA, doublée d'un QC sémantique automatisé.

**Métriques de validation (Gold - 1 000 lignes) :**
| Catégorie | Count | % |
|---|---|---|
| `CONSISTENT` | 270 | 27.0% |
| `CORRECTED` | 728 | 72.8% |
| `SUSPICIOUS` | 2 | 0.2% |
*Similarité moyenne : 0.3727*

**Métriques de validation (Silver - 9 000 lignes) :**
Sur l'échantillon complet traité par `hybrid_semantic_consistency.py` :
| Catégorie | Count | % |
|---|---|---|
| `CONSISTENT` | 2,367 | 26.3% |
| `CORRECTED` | 6,318 | 70.2% |
| `SUSPICIOUS` | 315 | 3.5% |
*Similarité moyenne : 0.3582*

Nous avons vérifié manuellement les lignes marquées `SUSPICIOUS` pour s'assurer qu'elles ne contenaient pas de bruit bloquant pour l'entraînement. L'analyse montre que la majorité des "corrections" apportées par l'IA concernent la normalisation des artefacts et l'alignement MSA/Darija.

---

# 4.6 📊 Analyse des Erreurs de l'IA

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Listez et illustrez les types d'erreurs observées dans les labels produits par votre modèle IA :
> - Erreurs de classification (si applicable)
> - Erreurs de traduction (sens, registre, fidélité)
> - Cas d'ambiguïté ou de sarcasme mal interprétés
> - Exemples concrets (au moins 2–3 exemples réels tirés de vos données)

Dans le cadre de notre vérification (notebook `final_analysis.ipynb`), l'analyse des outputs a révélé les points suivants sur notre dataset final :

**1. Zéro Anomalie Critique (Data Quality) :**
Les vérifications par expressions régulières (Regex) exécutées sur le Dataset Final prouvent une absence totale de corruption critique  :
- **Arabe dans la colonne English** : 0 cas détecté.
- **Traductions manquantes (Darija, English, MSA)** : 0 cas.
- **Fuite de script (Non-Arabic Darija ou Arabic in Arabizi)** : 0 cas.

**2. Type d'erreur résiduelle (avant correction finale) :**
Bien que la première passe d'IA ait lissé le Silver dataset, un cas (1 seul) a nécessité une correction manuelle ultime identifiée par notre script de comparaison d'évolution.
- **Erreur typographique / Espace superflu** : 
  - *Généré par l'IA* : `ب تعديل قوانین...`
  - *Corrigé manuellement en* : `بتعديل قوانین...` (suppression de l'espace après la préposition `ب`).
Cela démontre la très haute fidélité du pipeline, ne laissant passer qu'une infime erreur d'espacement.

---

## 🟡 Groupe 2

Lors du spot-checking des 80 lignes (1%/classe), plusieurs catégories d'erreurs récurrentes ont été identifiées et corrigées par Yassine Boumhand :

**1. Artefacts non supprimés :**
Quelques lignes sources contenant des tokens résiduels (`<unk>`, `@-@`, `@@`) n'avaient pas été entièrement filtrées malgré les instructions du prompt. Ces cas ont nécessité une correction manuelle ciblée.

*Exemple :* Un token `<unk>` conservé dans `darija_arabizi` alors que la règle DQA impose son remplacement par le terme contextuel logique.

**2. Code-switching Wikipedia :**
Les phrases issues de fragments Wikipedia en français ou en anglais insérés dans le flux Darija ont occasionnellement donné lieu à des traductions hybrides ou incohérentes — GPT-4o-mini ayant parfois du mal à identifier la langue source réelle et la langue cible de la traduction.

*Exemple :* Une phrase mélangeant darija et terminologie technique française traduite partiellement en anglais plutôt qu'en MSA.

**3. Sur-formalisation en MSA :**
Le modèle a parfois produit des formulations MSA trop littéraires ou soutenues par rapport au registre oral de la Darija source. Ce type d'erreur subtil ne peut être détecté que par un locuteur natif disposant d'une sensibilité linguistique fine — ce qui justifie que la validation ait été confiée exclusivement à Yassine Boumhand.

**4. Caractères latins résiduels dans `darija_arabic` :**
Quelques cas isolés où des mots étrangers (marques, noms propres techniques) ont été laissés en script latin au lieu d'être translittérés en arabe, en violation de la contrainte DQA — exception faite des formules mathématiques universelles qui sont tolérées.

**5. Variabilité des traductions courtes (Classe A) :**
Pour les phrases très courtes, plusieurs formulations correctes coexistent. GPT-4o-mini produisait des sorties valides mais différentes des corrections humaines, ce qui impactait mécaniquement le score BLEU sans constituer une erreur réelle de traduction.

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

Les erreurs les plus fréquentes que nous avons vues ne sont pas des “fautes de frappe” isolées, mais plutôt des **décalages de sens** entre la Darija source et les colonnes cibles, surtout quand la phrase est longue ou mélange plusieurs registres. À cela s’ajoutent des **artefacts** résiduels (`<unk>`, morceaux encyclopédiques) et des statuts qui ne reflètent pas encore un état final homogène (`GENERATED`, `PARTIALLY VALIDATED`).

Côté gold, nous avons aussi eu un problème plus “administratif” mais critique : un fichier de correction (`the_first_500.corrected.csv`) **n’était pas aligné** sur les bons `data_id` pour la moitié attendue, ce qui nous a forcés à documenter un fallback propre sur le gold de référence.

En pratique, nos corrections ressemblent souvent à : réécrire l’anglais / le MSA pour coller au sens darija, lisser une ligne trop “wiki”, ou stabiliser le gold via merge sans perdre des lignes.

Ce que la **comparaison sémantique** nous apprend, c’est surtout comment prioriser : sur le gold, les cas `SUSPICIOUS` restent rares (0,2%), donc le signal est rassurant ; sur le silver, il y a plus de `SUSPICIOUS` (3,5%), ce qui est normal sur un shard plus bruité — pour nous, ça veut dire “**relire d’abord ces lignes**”, pas “jeter le dataset”.

L’IA nous a fait gagner beaucoup de temps sur le volume, mais sur la Darija il reste des cas où seule une relecture humaine permet de trancher sans déformer le sens.

---

# 4.7 📈 Statistiques de Performance

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Renseignez vos métriques de performance, **avant** et **après** correction :
> - Nombre total de données labellisées automatiquement
> - Nombre d'erreurs détectées
> - Taux d'erreur (erreurs / total)
> - Après correction : nombre de lignes corrigées et qualité estimée du dataset final

**Données labellisées automatiquement (Silver Set) :**
- Volume traité : **9 005 lignes**.
- Appels API (Auto-Correction IA) révisant les lignes : **8 652 lignes modifiées**.
- Taux d'intervention de l'IA : **96,08%**.
- Correction Manuelle finale : **1 seule ligne modifiée**.

**Analyse Gold Set (Après Validation Manuelle) :**
- Total des lignes Gold : **1 003 lignes**.
- Nombre de lignes corrigées manuellement : **282 lignes**.
- Taux de correction manuelle : **28,12%**.

**Qualité estimée finale :**
Le Dataset Final (10 008 lignes) est déclaré sain à **100%**. L'analyse DQA (Section 5 du notebook) a rapporté *0 cas* de fuite de script ou de valeur manquante. Cette base solide servira de _Ground Truth_ (via ses statistiques de longueur harmonieuses, Section 4) et de corpus d’entraînement robuste.

---

## 🟡 Groupe 2

### Avant correction (Silver Standard brut — évalué sur l'échantillon spot-check)

| Métrique | Valeur |
|---|---|
| Lignes labellisées automatiquement | 9 005 |
| Lignes spot-checkées (1%/classe) | 80 |
| BLEU English (global) | 97,3 |
| chrF++ English (global) | 98,5 |
| BLEU MSA (global) | 97,2 |
| chrF++ MSA (global) | 98,3 |
| Taux de qualité estimé (IC 95%) | **[91,8% ; 100%]** |

> **Note méthodologique :** Le taux d'erreur exact sur la totalité des 9 005 lignes n'est pas calculable sans relecture exhaustive. Les métriques BLEU et chrF++ calculées sur les 80 lignes spot-checkées constituent l'estimateur statistiquement fondé de la qualité générale du corpus.

### Après correction (Silver Standard final)

| Métrique | Valeur |
|---|---|
| Statut final | 100% VALIDATED |
| Corrections manuelles appliquées | Ciblées sur les erreurs détectées lors du spot-checking |
| Qualité finale (BLEU English) | > 97 |
| Qualité finale (chrF++ toutes colonnes) | > 98 |

Ces résultats sont **exceptionnellement élevés pour une langue low-resource** comme la Darija marocaine, validant statistiquement et méthodologiquement la décision de validation en masse.

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

### Analyse Comparative EDA (Avant / Après)

Cette section détaille l'impact du nettoyage sur le Shard 3.

#### 📊 Statistiques Silver (9 000 lignes)
L'analyse montre un taux de modification quasi-total, signifiant que chaque ligne a été normalisée ou corrigée pour garantir la cohérence.

| Colonne | Lignes Comparées | Lignes Modifiées | Taux de Changement |
|---|---|---|---|
| `english` | 9,000 | 9,000 | **100.00%** |
| `modern_standard_arabic` | 9,000 | 8,998 | **99.98%** |
| `darija_arabic` | 9,000 | 8,975 | **99.73%** |
| `darija_arabizi` | 9,000 | 8,590 | **95.45%** |

**Distribution des longueurs (Moyenne de caractères) :**
- `darija_arabic` : 108.4 (Source) → 88.2 (Cleaned)
- `english` : 122.1 (Source) → 105.5 (Cleaned)

#### 📊 Statistiques Gold (1 000 lignes)
| Colonne | Lignes Comparées | Lignes Modifiées | Taux de Changement |
|---|---|---|---|
| `english` | 979 | 979 | **100.00%** |
| `darija_arabic` | 979 | 972 | **99.28%** |
| `modern_standard_arabic` | 979 | 969 | **98.98%** |
| `darija_arabizi` | 979 | 905 | **92.44%** |

### Rapport de Consistance Sémantique (Hybrid QC)
Le run final sur le Silver dataset a généré les métriques suivantes :
- **Lignes traitées** : 9 000
- **Appels LLM (GPT-4o-mini)** : 8,650
- **Similarité Sémantique Moyenne** : 0.82 (après correction)
- **Status Cleaned** : `VALIDATED` (8,985), `REVIEW_REQUIRED` (15)

### Avant correction (état initial des fichiers de livraison Groupe 3)

| Métrique | Valeur |
|---|---|
| Silver traité | 9 000 lignes |
| Gold traité | 1 000 lignes |
| Statuts initiaux dominants (Silver) | GENERATED / PARTIALLY VALIDATED |
| Problèmes identifiés | Artefacts textuels, incohérences ponctuelles, hétérogénéité de statuts |

### Après correction / consolidation

| Métrique | Valeur |
|---|---|
| Export final Gold | `shards/gold/gold_shard_3.csv` |
| Export final Silver | `shards/silver/silver_shard_3.csv` |
| Lignes Gold finales | 1 000 |
| Lignes Silver finales | 9 000 |
| Champs requis vides (contrôle final) | 0 |

**Qualité finale estimée :**
Au moment de rendre le dossier, nos exports sont **cohérents structurellement** (pas de champs critiques vides sur les fichiers finaux shard 3) et prêts à être fusionnés avec les autres groupes. La qualité “linguistique maximale” reste une cible : sur le silver, la passe sémantique sert surtout à **mettre en évidence** les lignes à revoir en priorité.

---

# 4.8 🔧 Correction des Erreurs

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Expliquez votre processus de correction des erreurs identifiées :
> - Comment avez-vous corrigé les erreurs (manuellement, via script, combiné) ?
> - Quel outil ou interface avez-vous utilisé ?
> - Quelles difficultés avez-vous rencontrées lors de la correction ?

**Processus de correction :**
Le pipeline a été décomposé en deux approches distinctes (hybride) :
1. **Outil API/Script pour le volume** : L'utilisation itérative de la fonction `get_smart_correction()` requêtant GPT-4.1-mini. Cette passe automatisée a géré le Silver Set (9 000 lignes).
2. **Interface Label Studio pour la précision** : L'échantillon Gold (1 000 lignes) a été repassé manuellement. L'outil a permis un ciblage colorimétrique et conditionnel.

**Difficultés :**
- L'instabilité des API : le système renvoyait parfois autre chose qu'un JSON complet ou tombait en erreur réseau. Cela a imposé l'ajout de mécanismes de résilience majeurs (fallback RegEx, 3 Retries, backup asynchrone).
- Le challenge humain ("Oralisation") : Forcer une restitution phonétique marocaine sur 73% de l'Arabizi. Ce processus s'est révélé incroyablement chronophage et demandait un niveau de dextérité dialectique très précis.

---

## 🟡 Groupe 2

**Comment les erreurs ont-elles été corrigées ?**
Les erreurs identifiées lors du spot-checking ont été corrigées directement dans Label Studio par Yassine Boumhand. Le workflow était le suivant :

1. Identification de la ligne erronée lors de la relecture de la sonde
2. Correction manuelle du ou des champs concernés (`darija_arabic`, `darija_arabizi`, `english`, ou `modern_standard_arabic`)
3. Basculement du statut de la ligne en `VALIDATED`

Les livrables du spot-checking sont tracés dans deux fichiers distincts : `spot_check/spot_check_par_classe.csv` (sorties GPT brutes) et `spot_check/human_corrige_propre.csv` (corrections humaines), permettant le calcul des métriques BLEU/chrF++ par jointure sur la colonne `id`.

**Difficultés rencontrées :**
- L'interface Label Studio ne permet pas de filtrer facilement les lignes par type d'erreur — la navigation dans les tâches est manuelle
- La colonne `english_word_count` requise par le XML de configuration Label Studio pour l'import du spot-check a dû être ajoutée dynamiquement avant import via un script pandas
- La correspondance exacte entre lignes GPT et lignes humaines pour le calcul des métriques a nécessité une jointure soigneuse sur la colonne `id`, en raison d'un alignement non garanti par défaut
- Les ambiguïtés linguistiques propres à la Darija (registres oraux régionaux, mots à plusieurs translittérations arabizi valides) ne disposent pas de « bonne réponse » unique — Yassine a dû trancher seul, sans contre-validation possible par un second locuteur natif

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

Nous avons enchaîné les corrections de manière très pragmatique : d’abord des scripts pour traiter le volume du silver (`correct_silver.py`, `correct_all_4_mt_fields.py`), puis une passe plus “semantic-aware” avec `hybrid_semantic_consistency.py`. Pour le gold, nous avons privilégié une correction manuelle exhaustive ligne par ligne pour garantir une fiabilité totale du jeu de test.

Les outils sont classiques (Python + API OpenAI + notebooks pour le silver, relecture humaine pour le gold), mais l’important pour nous était surtout la **traçabilité** : à chaque étape, on peut expliquer ce qui a changé et pourquoi.

Les difficultés principales restent quelques lignes extrêmement bruitées dans le silver où une correction automatique risquerait de dénaturer le sens : dans ces cas, on préfère être conservateurs et laisser une trace claire (`SUSPICIOUS`, notes QC) plutôt que “forcer” une traduction incorrecte.

---

# 4.9 📊 Statistiques du Dataset

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Renseignez les statistiques de votre dataset :
> - Nombre total d'exemples (Gold + Silver)
> - Répartition des classes (si applicable : classes de longueur, de sentiment, etc.)
> - Y a-t-il un déséquilibre entre les classes ? Comment l'avez-vous traité ou documenté ?

**Nombre total d'exemples :**
~10 005 lignes au total, découpées entre le Silver Shard et le Gold Shard.
- Fichier Silver (IA) : `silver_shard_1_clean_corrected_final.csv` (9 005 lignes).
- Fichier Gold (Modifié manuellement) : `gold_shard_1_clean_validated_final.csv` (1 000 lignes).

**Statistiques des colonnes :**
La fusion avec Label Studio a fait passer la structure de la vérité terrain (Gold Set) de 9 colonnes en entrée à **21 colonnes**, augmentées de toutes les traçabilités sémantiques annotateur.

**Équilibre et Intégrité :**
Aucun doublon n'a été détecté lors de la validation (`0 doublon` dans la phase EDA). Les valeurs aberrantes de mots (longueur) ont pu être rectifiées, assurant la cohérence structurelle du set final voué à l'entraînement de l'AraT5v2.

---

## 🟡 Groupe 2

| Livrable | Fichier | Lignes | Statut |
|---|---|---|---|
| Gold Standard | `deliverables/gold_final.csv` | 1 003 | 100% VALIDATED |
| Silver Standard | `deliverables/silver_final.csv` | 9 005 | 100% VALIDATED |
| Export LS Gold | `deliverables/gold_final_annotation_history.json` | 1 003 | Export brut |
| Export LS Silver | `deliverables/silver_final_annotation_history.json` | 9 005 | Export brut |
| Spot-check GPT | `spot_check/spot_check_par_classe.csv` | 80 | Référence GPT |
| Spot-check Human | `spot_check/human_corrige_propre.csv` | 80 | Corrections humaines |
| Métriques | `spot_check/metriques_spot_check.csv` | — | BLEU / chrF++ |
| **Total corpus Groupe 2** | — | **10 008** | **100% VALIDATED** |

**Répartition par classe de longueur :**

| Classe | Description | Lignes | % |
|---|---|---|---|
| A | Phrases courtes | 2 573 | 25,7% |
| B | Phrases moyennes | 2 452 | 24,5% |
| C | Phrases longues | 2 569 | 25,7% |
| D | Très longues | 2 411 | 24,1% |
| **Total** | | **10 008** | **100%** |

**Observations sur l'équilibre des classes :**
La distribution est remarquablement équilibrée entre les 4 classes (~25% chacune), garantissant un entraînement uniforme du modèle AraT5v2 sans biais lié à la longueur des phrases. Aucun rééchantillonnage n'a été nécessaire.

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

Ci-dessous, les fichiers que nous considérons comme **nos livrables** pour le shard 3 : une version “nettoyée / corrigée”, une version silver avec **QC sémantique** (scores + flags), puis les exports attendus dans `shards/` pour la fusion globale.

| Livrable | Fichier | Lignes | Statut |
|---|---|---|---|
| Gold final Groupe 3 | `group_3/deliverables/gold_shard_3.cleaned.corrected.csv` | 1 000 | Nettoyé |
| Silver final Shard 3 | `group_3/deliverables/silver_shard_3.cleaned.corrected.csv` | 9 000 | Final |
| Silver + QC Sémantique | `group_3/deliverables/silver_shard_3.semantic.hybrid.csv` | 9 000 | QC Validated |
| Export shard Gold | `shards/gold/gold_shard_3.csv` | 1 000 | Final |
| Export shard Silver | `shards/silver/silver_shard_3.csv` | 9 000 | Fusion Ready |
| **Total corpus Groupe 3** | — | **10 000** | **Livrable Final** |

**Répartition par classes (Gold) :**

| Classe | Lignes |
|---|---|
| A | 250 |
| B | 250 |
| C | 250 |
| D | 250 |
| **Total** | **1 000** |

**Répartition par classes (Silver) :**

| Classe | Lignes |
|---|---|
| A | 2,250 |
| B | 2,250 |
| C | 2,250 |
| D | 2,250 |
| **Total** | **9 000** |

---

# 4.10 ⚠️ Limites

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Identifiez et documentez honnêtement les limites de votre travail :
> - Biais potentiels dans vos données (sources surreprésentées, démographies, thèmes)
> - Limites linguistiques spécifiques à votre sous-corpus
> - Limites du modèle IA que vous avez utilisé
> - Limites de votre processus de validation

1. **Limites de l'IA (Correction) :** Bien que puissant, GPT-4.1-mini n'est pas nativement calibré sur les subtilités bédouines marocaines. L'IA a donc systématiquement tendance à effectuer de l'"hyper-correction" sémantique se rapprochant du MSA, aplatissant le ton dialectal propre à la Darija.
2. **Complexité du Dialecte (Limites linguistiques) :** Le corpus initial ne distingue probablement pas bien les influences régionales de la Darija (Marrakech, Chamal, Oriental..). De surcroît, le défi du code-switching (présence d'emprunts francophones, amazighs ou hispaniques) brouille l'emploi des racines orthographiques trilitères.
3. **Limites du modèle alternatif :** La validation de la baseline `Atlas-Chat-2B` testée "Zero-Shot" (hors fine-tuning) a prouvé ses lacunes sévères pour restituer la véritable phonétique Arabizi de la langue ciblée.
4. **Validation volumétrique :** Inspecter exhaustivement un pack "Silver" de 9000 lignes est temporellement complexe face aux ressources, justifiant un compromis d'échantillonnage ciblé sur ce segment.

---

## 🟡 Groupe 2

**Limites de la validation par échantillonnage :**
La validation du Silver Standard repose sur un spot-checking à 1%/classe (80 lignes au total). Bien que statistiquement fondé (IC 95% : [91,8% ; 100%]), ce protocole ne garantit pas une qualité uniforme sur la totalité des 9 005 lignes — des erreurs isolées peuvent subsister dans les 99% non échantillonnés.

**Limites liées à l'annotateur unique :**
L'annotation du Gold Standard et la validation humaine du spot-checking ont été réalisées par un seul annotateur natif (Yassine Boumhand). L'absence d'un second locuteur natif de la Darija pour le calcul d'un accord inter-annotateurs (IAA / score Kappa) est une limite méthodologique réelle : les décisions sur les cas ambigus (translittérations arabizi, registre MSA, gestion du code-switching) n'ont pas pu être contre-validées de manière indépendante. Ce choix est contraint par la composition du groupe — Abdourazak Akillou Illa, originaire du Niger, ne maîtrise pas la Darija marocaine.

**Limites linguistiques :**
- La Darija marocaine présente une forte variation régionale (Casablanca, Marrakech, Fès, etc.). Le corpus ne distingue pas ces sous-variétés, ce qui peut introduire une inconsistance dans les conventions de translittération arabizi.
- Les cas de code-switching intensif (darija + français + anglais + amazigh dans une même phrase) restent un défi pour GPT-4o-mini, malgré ses performances globales excellentes.
- La Darija est une langue essentiellement orale, peu standardisée à l'écrit — plusieurs translittérations arabizi sont valides pour un même mot, sans qu'il y ait d'erreur objective.

**Limites du modèle IA :**
- GPT-4o-mini n'est pas nativement spécialisé sur la Darija marocaine — ses performances sont inférieures à celles d'un locuteur natif expert sur les registres très familiers ou argotiques.
- La température de 0,1 garantit la stabilité mais peut réduire la diversité des formulations, créant un corpus légèrement homogène dans son style.
- La limite de `max_tokens=500` pourrait être insuffisante pour des phrases de classe D très longues — des troncatures sont possibles sur ces cas limites.

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

Nous assumons clairement une limite importante : nous n’avons pas relu “mot à mot” tout le silver comme on le ferait pour un gold 100% manuel. Notre compromis, c’est une combinaison **QC automatique + sémantique + relecture ciblée**, ce qui est réaliste pour un binôme, mais ce n’est pas équivalent à une validation exhaustive.

La darija reste une langue **orale** et variable : deux translittérations arabizi peuvent être acceptables, et le “bon” MSA peut dépendre du registre choisi. Sur des phrases techniques ou encyclopédiques, même une bonne IA peut se tromper sur ce qu’il faut privilégier.

Enfin, nous avons porté une attention particulière à la cohérence du Gold Standard : l'intégralité des 1 000 lignes a été revue manuellement pour s'assurer qu'aucun artefact technique ou décalage sémantique ne subsiste dans le jeu de test final.

---

# 4.11 🚀 Améliorations

---

## 🔵 Groupe 1 — Ikram EL MENHI & Abderrahim AZEROUAL

> **Instructions :** Proposez des améliorations concrètes et réalistes pour votre pipeline :
> - Que changeriez-vous dans votre collecte de données ?
> - Comment amélioreriez-vous votre annotation ?
> - Quel modèle IA ou quels paramètres testeriez-vous en priorité ?
> - Y a-t-il des étapes de votre pipeline qui mériteraient d'être automatisées ?

1. **Automatisation prédictive des anomalies (Script leakage) :** Pousser plus loin les filtres Regex pour diagnostiquer et intercepter 100% des contaminations arabes/latines avant tout appel API, économisant des requêtes et fiabilisant la boucle.
2. **Lexique Standard de l'Arabizi :** Coder une base de règles phonétiques formelle  lors des générations futures de datasets synthétiques pour baisser la marge d'erreur en correction automatisée qui s'est avérée massive (73,6%).
3. **Optimiser le modèle de base :** L'enjeu est l'utilisation future de ce Gold Standard pour Fine-Tuner l'**AraT5v2** ou le modèle **Atlas-Chat-2B**, afin que les versions ultérieures du pipeline dépendent de modèles qui "connaissent" déjà les inflexions temporelles et lexicales de la Darija, minimisant l'intervention de l'API GPT-4, voire de l'annotateur.

---

## 🟡 Groupe 2

**Améliorations sur la validation humaine :**
- Recruter un second locuteur natif de la Darija pour mettre en place un vrai accord inter-annotateurs (IAA) avec calcul du score Kappa — cela permettrait de quantifier objectivement la consistance des jugements et d'identifier les cas réellement ambigus
- Augmenter le taux de spot-checking à 5%/classe pour une couverture statistique encore plus robuste, sans que cela remette en cause la validité des résultats actuels

**Améliorations sur l'annotation du Gold Standard :**
- Définir un guide d'annotation écrit, versionné et partagé entre tous les groupes, pour harmoniser les conventions arabizi à l'échelle du corpus global fusionné
- Constituer un lexique de référence des translittérations arabizi marocaines pour les mots les plus fréquents, afin de réduire la variabilité inter-annotateurs lors de la fusion des shards

**Améliorations sur le modèle IA :**
- Tester des modèles fine-tunés sur la Darija (ex. : DarijaBERT, AraT5v2 lui-même en mode zero-shot) en remplacement ou en complément de GPT-4o-mini
- Augmenter `max_tokens` à 800 pour prévenir les troncatures sur les phrases de classe D
- Expérimenter avec un prompt few-shot (2–3 exemples annotés manuellement dans le prompt) pour améliorer la fidélité sur les cas de code-switching complexes
- Mettre en place une validation automatique post-génération par regex (vérifier l'absence de caractères latins dans `darija_arabic`, détecter les `<unk>` résiduels) avant la phase de validation humaine, afin de cibler le spot-checking sur les lignes les plus à risque

---

## 🟢 Groupe 3 — Yahya Sahnoun & Chaimae El Monjali

Si nous devions continuer, nous ferions d’abord un **spot-check stratifié** sur le silver (par classe) en partant surtout des lignes `SUSPICIOUS`. Ensuite, nous ajouterions des contrôles automatiques simples après génération (regex sur artefacts, caractères inattendus dans `darija_arabic`, statuts incohérents). Nous harmoniserions aussi nos conventions arabizi dans un mini guide interne pour assurer une consistance parfaite sur de plus gros volumes. Enfin, un petit calcul BLEU/chrF++ sur un échantillon validé à deux nous semble utile pour rendre la partie “performance” plus comparable à un vrai protocole d’évaluation.

---

*Ce rapport a été produit dans le cadre du Projet R&D — Traduction Automatique Darija (MT), Module Text Mining, Année universitaire 2025–2026.*
*Encadrant : Pr. Imad HAFIDI*
*GitHub : [Traduction-Automatique-Darija](https://github.com/Yboumhand/Traduction-Automatique-Darija)*
