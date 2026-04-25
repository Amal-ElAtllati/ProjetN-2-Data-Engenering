# Rapport de Traitement du Pipeline Data Lake

Ce document trace les transformations appliquées entre les zones Bronze, Silver et Gold, conformément aux exigences d'auditabilité du Data Lake.

## 1. Ingestion Bronze (Raw)
- **Source** : `offres_emploi_it_maroc.json` (5000 offres brutes).
- **Règle appliquée** : Aucune modification des données. Séparation par source (Rekrute, LinkedIn, MarocAnnonce) et par mois de publication (`YYYY_MM`).
- **Cas limites traités** :
  - Certaines dates de publication étaient inversées avec la date d'expiration ou dans des formats non standards (`DD/MM/YYYY`). Ces cas ont été mis dans une partition de secours si la date était illisible, ou extraite via un try-catch.
- **Résultat** : 5000 offres sauvegardées dans le dossier `bronze/`.

## 2. Transformation Silver (Cleaned)

### a. Nettoyage des Titres de Postes
- **Règle** : Regex Mapping sur un dictionnaire de 16 familles de métiers IT.
- **Lignes Avant/Après** : 5000 lignes -> 5000 lignes (pas de suppression).
- **Cas limites** : Les offres qui ne matchent aucun profil (ex: "Développeur C++") sont classées dans "Autre IT" pour ne pas perdre la donnée.

### b. Normalisation des Salaires
- **Règle** : Conversion des K en milliers (ex: 15K -> 15000), conversion des Euros en MAD (taux de 10.8), extraction min/max et calcul de la médiane.
- **Cas limites** : Les offres contenant "Confidentiel", "Selon profil" ou `null` reçoivent le flag `salaire_connu = False`. Les salaires aberrants (< 3000 ou > 100000 MAD) ont également été ignorés car probables erreurs de saisie.

### c. Normalisation de l'Expérience
- **Règle** : Extraction du nombre d'années d'expérience minimal et maximal requis.
- **Cas limites** : Traduction des mots-clés "Junior" et "Débutant" vers (0, 2 ans), et "Senior" / "Expert" vers (5, `None` ans).

### d. Normalisation des Villes et Contrats
- **Règle** : Standardisation (ex: "casa" ou "CASABLANCA" -> "Casablanca"). Affectation à la région administrative correspondante. Pour les contrats, regroupement ("Permanent", "Indéterminé" -> "CDI").

### e. Extraction NLP des Compétences
- **Règle** : Matching par mot exact (word boundary `\b`) entre les champs `competences_brut` + `description` et le référentiel JSON fourni.
- **Lignes Avant/Après** : 5000 offres -> N lignes (Une ligne par compétence trouvée par offre).
- **Cas limites** : 
  - Faux positifs évités en cherchant les mots entiers (ex: "r" ne matche pas toutes les lettres 'r' d'un mot).
  - Si une offre n'a aucune compétence détectée, on insère la compétence "non_détecté" pour conserver la trace de l'offre.

## 3. Agrégation Gold (Curated)
- **Outil** : DuckDB via l'API Python interrogant les fichiers Parquet Silver.
- **Tables créées** :
  1. `top_competences` : Classement et pourcentage des compétences les plus demandées.
  2. `salaires_par_profil` : KPI de distribution des salaires (médiane, moyenne, Q1, Q3).
  3. `offres_par_ville` : Volume d'offres et part du télétravail.
  4. `entreprises_recruteurs` : Top des recruteurs et profil chassé.
  5. `tendances_mensuelles` : Évolution temporelle (utilisation des Window functions `LAG()`).
