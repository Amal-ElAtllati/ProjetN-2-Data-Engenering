import os
from pipeline.bronze_ingestion import ingerer_bronze
from pipeline.silver_transform import charger_depuis_bronze, nettoyer_titres_postes, normaliser_salaires, normaliser_experience, normaliser_villes, normaliser_contrat
from pipeline.silver_nlp import extraire_competences, sauvegarder_silver
from pipeline.gold_aggregation import construire_gold

DATA_LAKE_ROOT = "data_lake"
SOURCE_FILE = "../offres_emploi_it_maroc.json"
REFERENTIEL_FILE = "../referentiel_competences_it.json"

def main():
    print("=== Démarrage du Pipeline Data Lake Mexora ===")
    
    # Étape 1 : Bronze Ingestion
    print("\n--- PHASE BRONZE ---")
    stats_bronze = ingerer_bronze(SOURCE_FILE, DATA_LAKE_ROOT)
    
    # Étape 2 : Silver Transform
    print("\n--- PHASE SILVER (Nettoyage) ---")
    df = charger_depuis_bronze(DATA_LAKE_ROOT)
    df = nettoyer_titres_postes(df)
    df = normaliser_salaires(df)
    df = normaliser_experience(df)
    df = normaliser_villes(df)
    df = normaliser_contrat(df)
    
    # Étape 3 : Silver NLP (Extraction des compétences)
    print("\n--- PHASE SILVER (NLP) ---")
    df_competences = extraire_competences(df, REFERENTIEL_FILE)
    
    # Sauvegarde Silver
    sauvegarder_silver(df, df_competences, DATA_LAKE_ROOT)
    
    # Étape 4 : Gold Aggregation
    print("\n--- PHASE GOLD ---")
    construire_gold(DATA_LAKE_ROOT)
    
    print("\n=== Pipeline terminé avec succès ! ===")

if __name__ == "__main__":
    main()
