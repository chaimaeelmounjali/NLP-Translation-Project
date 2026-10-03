# 🇲🇦 End-to-End Moroccan Darija Machine Translation & Corpus Engineering (NLP)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python)](https://www.python.org/)
[![Hugging Face](https://img.shields.io/badge/NLP-Sentence%20Transformers-yellow.svg?logo=huggingface)](https://huggingface.co/)
[![Groq](https://img.shields.io/badge/Groq-Batch%20Inference-orange.svg)](https://groq.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991.svg?logo=openai)](https://openai.com/)
[![Label Studio](https://img.shields.io/badge/Annotation-Label%20Studio-blue.svg)](https://labelstud.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

*Bilingual README: [Français](#-version-française) | [English](#-english-version)*

> 🎓 **Projet R&D - Module Text Mining (2025-2026)**  
> **Encadrant :** Pr. Imad HAFIDI  
> **Auteur & Membre Groupe 3 :** Chaimae EL MOUNJALI

---

## 🇫🇷 Version Française

### 🎯 Objectif
Ce projet collaboratif de recherche et développement (R&D) en Traitement Automatique du Langage Naturel (NLP) vise à concevoir, purifier et évaluer un corpus de traduction automatique trilingue et bimodal de haute qualité reliant l'**Anglais**, l'**Arabe Standard Moderne (MSA)** et la **Darija Marocaine** (en graphie arabe et en Arabizi). Le projet répond au défi des langues à faibles ressources (*low-resource languages*) en structurant un pipeline complet combinant annotation humaine de référence (**Gold Standard**) et génération semi-supervisée par LLMs avec contrôle qualité sémantique (**Silver Standard**).

### 🛠️ Stack Technologique
- **Langages & Traitement NLP** : Python 3.10+, Jupyter Notebooks, Sentence-Transformers (similarité cosinus sémantique multilingue), spaCy, NLTK.
- **Génération & Modèles LLM** : Groq API (Llama 3 70B), OpenAI API (`gpt-4o-mini`), traitement asynchrone par batch, stratégies de backoff et de reprise sur checkpoint.
- **Plateforme d'Annotation** : Label Studio (configuration XML personnalisée `Labeling_Interface.xml`).
- **Analyse & Validation Statistique** : Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn.
- **Livrables Scientifiques** : LaTeX / Beamer pour les rapports méthodologiques et présentations.

### 👩‍💻 Mon Rôle & Contributions (Groupe 3)
Au sein de ce projet collaboratif structuré en trois groupes d'ingénierie, j'ai assuré la responsabilité technique du **Groupe 3** (Lead sur le Shard 3) :
- **Pipeline de Correction Automatisée du Silver Shard 3** :
  - Conception et automatisation des scripts batch (`correct_silver.py`, `correct_all_4_mt_fields.py`) pour éliminer les erreurs syntaxiques et lexicales.
  - Implémentation d'un système robuste de reprise sur erreur avec persistance d'états (`.jsonl`).
- **Contrôle Qualité Sémantique Hybride (`hybrid_semantic_consistency.py`)** :
  - Développement de l'algorithme de calcul de similarité vectorielle pour détecter les hallucinations et faux alignements entre la langue source et cible.
  - Visualisation des distributions de confiance et seuillage adaptatif (`Hybrid_Semantic_QC_Visualization.ipynb`).
- **Analyses Exploratoires Comparatives (EDA)** :
  - Conception des études statistiques (`EDA_gold_shard_3_comparatif.ipynb`, `EDA_silver_shard_3_comparatif.ipynb`) mesurant la longueur des phrases, la distribution lexicale et les disparités graphiques (arabe vs arabizi).
- **Rapports Scientifiques & Soutenance** :
  - Rédaction intégrale du rapport technique de validation (`Rapport_QC_Cleaning_MT.pdf`) et élaboration du support de présentation de soutenance (`Presentation_Projet_Traduction.pdf`).

### 📊 Résultats & Métriques Clés
- **Corpus massif et nettoyé** : Plus de 20 000 segments textuels alignés et qualifiés répartis sur les shards Gold et Silver.
- **Filtrage sémantique rigoureux** : Suppression systématique des anomalies de traduction automatique avec un gain significatif sur la fidélité sémantique (> 95%).
- **Prêt pour le fine-tuning** : Dataset prêt à l'emploi ayant directement servi à l'entraînement et au déploiement du modèle T5 de l'application de traduction Darija.

---

## 🇬🇧 English Version

### 🎯 Objective
This collaborative NLP Research & Development project establishes an end-to-end parallel translation benchmark bridging **English, Modern Standard Arabic (MSA), and Moroccan Darija** across dual scripts (Arabic alphabet and Latin Arabizi). The initiative tackles the scarcity of high-quality training corpora for low-resource Arabic dialects by pairing human-validated **Gold Standards** with LLM-augmented, semantically sanitized **Silver Standards**.

### 🛠️ Tech Stack
- **NLP & Deep Learning**: Python 3.10+, Jupyter Notebooks, Sentence-Transformers (cross-lingual semantic similarity), NLTK, spaCy.
- **LLM Pipeline**: Groq API (Llama 3), OpenAI API (`gpt-4o-mini`), resilient batch ingestion, exponential backoff retries, JSONL state serialization.
- **Annotation & Human-in-the-Loop**: Label Studio with custom XML UI configs (`Labeling_Interface.xml`).
- **Data Analytics**: Pandas, NumPy, Scikit-Learn, Seaborn, Matplotlib.
- **Reporting**: LaTeX / Beamer document compilation.

### 👩‍💻 My Role & Key Contributions (Group 3)
As the lead contributor for **Group 3** (handling Shard 3 curation and validation):
- **Automated Silver Shard Refinement Pipeline**:
  - Developed end-to-end Python batch processing scripts to sanitize conversational Moroccan Darija pairs.
  - Integrated persistent fault-tolerant checkpoints to safely orchestrate high-volume API transformations.
- **Hybrid Semantic Quality Gate**:
  - Built an automated semantic filtering pipeline comparing multilingual vector embeddings to flag semantic drift and translation hallucinations.
  - Generated confidence threshold visualizations and pruning rules (`Hybrid_Semantic_QC_Visualization.ipynb`).
- **Comparative Exploratory Data Analysis (EDA)**:
  - Authored rigorous statistical notebooks comparing token length distributions, out-of-vocabulary frequencies, and script transliteration variance.
- **Academic Reporting & Presentation**:
  - Authored the comprehensive evaluation report (`Rapport_QC_Cleaning_MT.pdf`) and created the final slide deck for academic defense (`Presentation_Projet_Traduction.pdf`).

### 📊 Key Results & Impact
- **Curated Multi-Shard Dataset**: Standardized over 20,000 parallel bilingual pairs across Gold and Silver data shards.
- **High Semantic Integrity**: Achieved >95% semantic fidelity through embedding-based quality filtering.
- **Downstream Ready**: Formed the empirical foundation for fine-tuning custom T5 sequence-to-sequence neural translators.

---

### 📂 Repository Structure / Structure du Projet
```text
NLP-Translation-Project/
├── traduction-Project-main/
│   ├── group_1/              # Shard 1 EDA, scripts & cleaning
│   ├── group_2/              # Shard 2 Groq/OpenAI batch scripts & spot check
│   ├── group_3/              # Shard 3 Semantic QC, hybrid filtering & docs
│   ├── shards/               # Gold & Silver raw and cleaned shards
│   ├── DATASET_REPORT.md     # Global dataset analysis report
│   └── GROUPS.md             # Team assignments & project specifications
└── README.md                 # Project root documentation
```