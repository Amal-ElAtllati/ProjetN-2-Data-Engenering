# Mexora RH Intelligence - Projet Data Engineering

Ce projet implémente un Data Lake complet (Bronze, Silver, Gold) pour l'analyse du marché de l'emploi IT au Maroc.

## Comment reproduire le pipeline

1. **Prérequis :** Python 3.10+, DuckDB, Pandas, Seaborn.
2. **Installation :**
   ```bash
   pip install duckdb pandas seaborn matplotlib spacy nbformat
   python -m spacy download fr_core_news_sm
   ```
3. **Exécution du pipeline :**
   Les scripts doivent être lancés dans l'ordre suivant :
   *   `python mexora_rh_lake/pipeline/bronze_ingestion.py` : Ingestion des JSON bruts.
   *   `python mexora_rh_lake/pipeline/silver_transform.py` : Nettoyage et typage Parquet.
   *   `python mexora_rh_lake/pipeline/silver_nlp.py` : Extraction des compétences.
   *   `python mexora_rh_lake/pipeline/gold_aggregation.py` : Création des tables analytiques.
4. **Visualisation :**
   Ouvrez le notebook `Livrables/Étape 3 — Analyse DuckDB.ipynb` pour voir les graphiques.

##  Contributeurs
Projet réalisé par **Amal & Hanane**.
