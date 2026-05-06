# Architecture Data Lake Mexora RH Intelligence

```mermaid
flowchart TD
    %% Sources
    subgraph Sources [Sources de Données]
        A1[Rekrute]
        A2[MarocAnnonce]
        A3[LinkedIn]
    end

    %% Zone Bronze
    subgraph Bronze [ZONE BRONZE (Raw - Immuable)]
        B1[(Fichiers JSON\n/bronze/rekrute/...)]
        B2[(Fichiers JSON\n/bronze/marocannonce/...)]
        B3[(Fichiers JSON\n/bronze/linkedin/...)]
    end

    %% Processus Silver
    subgraph Ingestion_Nettoyage [Nettoyage & Standardisation]
        C1[Script: bronze_ingestion.py]
        C2[Script: silver_transform.py\n(Typage, Nettoyage regex)]
        C3[Script: silver_nlp.py\n(Extraction Compétences NLP)]
    end

    %% Zone Silver
    subgraph Silver [ZONE SILVER (Cleaned - Typé)]
        D1[(offres_clean.parquet)]
        D2[(competences.parquet)]
    end

    %% Processus Gold
    subgraph Aggregation [Agrégation et Enrichissement]
        E1[Script: gold_aggregation.py\n(DuckDB via Python)]
    end

    %% Zone Gold
    subgraph Gold [ZONE GOLD (Curated - Analytique)]
        F1[(top_competences.parquet)]
        F2[(salaires_par_profil.parquet)]
        F3[(offres_par_ville.parquet)]
        F4[(entreprises_recruteurs.parquet)]
        F5[(tendances_mensuelles.parquet)]
    end

    %% Consommateurs
    subgraph Consommateurs [Consommateurs de Données]
        G1[Data Analyst / DRH\n(Dashboard & Reporting)]
        G2[DuckDB Notebook]
    end

    %% Liens
    A1 --> C1
    A2 --> C1
    A3 --> C1
    C1 --> B1 & B2 & B3
    
    B1 & B2 & B3 --> C2
    B1 & B2 & B3 --> C3
    
    C2 --> D1
    C3 --> D2
    
    D1 & D2 --> E1
    
    E1 --> F1 & F2 & F3 & F4 & F5
    
    F1 & F2 & F3 & F4 & F5 --> G2
    G2 --> G1
```

## Description du Flux
1. **Ingestion (Raw)** : Les données brutes issues des 3 sources de scraping sont stockées au format `JSON` en conservant l'intégrité initiale (Zone Bronze).
2. **Standardisation (Cleaned)** : Les scripts Python nettoient les champs (Villes, Contrats, Salaires) et extraient les compétences depuis le texte libre (NLP basique). Le résultat structuré est sauvegardé en format `Parquet` (Zone Silver).
3. **Agrégation (Curated)** : Les tables Silver sont interrogées via le moteur SQL `DuckDB` embarqué dans Python pour créer les tables d'agrégation métiers orientées RH en format `Parquet` (Zone Gold).
4. **Analyse** : Les KPI et le Dashboard sont générés en interrogeant la Zone Gold.
