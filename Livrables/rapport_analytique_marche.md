# RAPPORT : Analyse du Marché de l'Emploi IT au Maroc
**Mexora RH Intelligence — Novembre 2024**
────────────────────────────────────────────────────

## 1. RÉSUMÉ EXÉCUTIF

Voici les principales conclusions de notre analyse du marché marocain de l'emploi IT, visant à éclairer la politique de recrutement de Mexora pour les 6 prochains mois.

**5 Chiffres Clés :**
1. Plus de **5 000 offres d'emploi IT** ont été analysées sur la période Janvier 2023 - Novembre 2024.
2. **Casablanca domine le marché** avec environ 60% des offres, contre seulement 5 à 10% pour Tanger.
3. Les **Data Engineers** et **Data Scientists** sont des profils pénuriques avec des salaires médians dans la fourchette haute (supérieurs à 18 000 MAD selon les années d'expérience).
4. Près de **30% des nouvelles offres** IT mentionnent désormais une forme de télétravail (hybride ou remote).
5. **Python et SQL** dominent le top 3 des compétences les plus demandées sur le marché global, particulièrement pour les profils Data.

**3 Recommandations Prioritaires pour Mexora :**
1. **Adopter le Télétravail (Hybride/Remote) :** Étant donné la faible densité d'offres à Tanger, Mexora doit s'ouvrir au télétravail pour attirer les talents basés à Casablanca ou Rabat, en particulier pour les Data Scientists.
2. **Alignement Salarial :** Proposer un salaire médian supérieur de 5% à 10% à la médiane de Tanger pour les profils Data afin de contrer la concurrence des grandes SSII et banques.
3. **Formation Interne (Upskilling) :** Certains outils très demandés en Data Engineering (Spark, Airflow) sont rares. Il est conseillé de recruter des profils juniors prometteurs en Python/SQL et de les former en interne à l'architecture Cloud/Big Data.

**Horizon de mise en œuvre :** Immédiat (pour l'ouverture des 5 postes prévus d'ici 6 mois).

---

## 2. MÉTHODOLOGIE

**Sources des données :**
Les données proviennent de 5 000 offres collectées par scraping sur **Rekrute**, **MarocAnnonce** et **LinkedIn Maroc**.

**Période couverte :**
Janvier 2023 à Novembre 2024.

**Limites et biais identifiés :**
- **Bruit dans les données** : Les offres contiennent beaucoup de texte libre, avec des intitulés souvent non standardisés (ex: "Dev Data").
- **Manque de transparence salariale** : Un grand nombre d'offres ne mentionnent pas le salaire ("Confidentiel", "Selon profil"), ce qui biaise légèrement les médianes à la hausse, les entreprises affichant plus volontiers les salaires compétitifs.

**Architecture Data Lake utilisée :**
Le système repose sur un **Data Lake en 3 zones** :
1. **Bronze (Raw)** : Stockage JSON immuable des données scrappées.
2. **Silver (Cleaned)** : Nettoyage en Python (Pandas/Regex/NLP) et stockage en Parquet (orienté colonnes, fortement typé). Extraction automatique des compétences via NLP sur la description des offres.
3. **Gold (Curated)** : Agrégation métier générée dynamiquement via DuckDB.

---

## 3. ÉTAT DU MARCHÉ IT AU MAROC

**Volume d'offres par profil :**
Le marché est largement dominé par la demande en **Développeurs Full Stack** et **Backend**. Toutefois, la demande pour les profils Data (Data Engineer, Data Analyst, Data Scientist) a connu une croissance soutenue de plus de 15% entre 2023 et 2024.

**Répartition géographique :**
- **Casablanca** : Cœur battant de la tech marocaine (sièges des banques, grandes ESN).
- **Rabat** : Pôle technologique fort, notamment grâce au secteur public et aux télécoms.
- **Tanger** : Marché de taille moyenne mais en croissance, porté par l'offshoring et la logistique.

**Télétravail :**
L'hybride est devenu la norme. 30% des annonces permettent au moins 2 jours de télétravail par semaine. Le 100% remote reste minoritaire mais est un argument de poids pour débaucher des talents.

**Types de contrats :**
Le **CDI** reste prépondérant (> 80%). Le Freelance (Auto-entrepreneur) est en hausse pour les profils experts (Architectes, Data Scientists Seniors) qui préfèrent l'indépendance.

---

## 4. COMPÉTENCES LES PLUS DEMANDÉES

**Top compétences globales :**
1. **Python** (Développement, IA, Data)
2. **SQL** (Incontournable pour tout projet lié aux bases de données)
3. **Java** / **JavaScript** (Très présents dans le web/backend)

**Compétences spécifiques aux profils data :**
- **Data Analyst** : SQL, Power BI, Tableau, Excel, Python.
- **Data Engineer** : Python, SQL, Spark, Airflow, AWS/GCP, dbt.
- **Data Scientist** : Python, R, Machine Learning, Scikit-learn, TensorFlow.

**Émergence de nouvelles compétences :**
L'année 2024 a vu une forte augmentation des requêtes liées au **Cloud (AWS, Azure)** et à **l'Intelligence Artificielle (LLM, NLP)**, ainsi que des outils de modélisation comme **dbt** (Data Build Tool).

---

## 5. ANALYSE SALARIALE

**Salaires médians par profil au Maroc :**
*(À titre indicatif, basé sur les annonces avec salaires connus, en MAD net/brut ajusté)*
- **Data Analyst Junior/Mid** : ~10 000 - 15 000 MAD
- **Data Engineer Junior/Mid** : ~14 000 - 20 000 MAD
- **Data Scientist / Architect** : > 22 000 MAD

**Comparaison Tanger vs Médiane Nationale :**
Historiquement, les salaires à Tanger sont environ 10% à 15% inférieurs à ceux de Casablanca. Cependant, avec l'essor du télétravail, cet écart tend à se réduire, les talents tangérois pouvant facilement postuler à Casablanca en remote.

**Corrélation Expérience / Salaire :**
La progression n'est pas purement linéaire. On observe des "paliers". Le saut le plus significatif se produit au passage "Senior" (généralement après 5 ans d'expérience), où le salaire peut augmenter de 30% à 50%.

---

## 6. RECOMMANDATIONS POUR MEXORA

Au vu de l'analyse, voici le plan d'action RH pour le recrutement des 5 nouveaux profils :

**Profils prioritaires à recruter :**
1. **2 Data Engineers (Mid-Level, 3-5 ans exp)** : Ce sont eux qui construiront l'infrastructure permettant à la marketplace de supporter les 50 000 commandes/mois.
2. **2 Data Analysts (Junior/Mid)** : Pour créer les dashboards métiers et assister les différentes équipes (Marketing, Produit).
3. **1 Data Scientist (Senior)** : Pour mener les chantiers avancés (prédiction des ventes, NLP sur les retours clients).

**Fourchettes salariales recommandées (Tanger) :**
Pour être compétitif sans exploser le budget :
- Data Analyst : 12 000 - 16 000 MAD
- Data Engineer : 16 000 - 22 000 MAD
- Data Scientist (Lead) : 25 000 - 30 000 MAD

**Stratégie de recrutement et de fidélisation :**
1. **Ouvrir le recrutement au niveau national** : Si le candidat parfait est à Agadir ou Casablanca, proposez-lui un contrat **Full Remote** avec prise en charge des déplacements à Tanger 1 fois par mois.
2. **Cultiver la Marque Employeur** : Mexora doit se positionner non pas comme une SSII classique, mais comme une **entreprise Produit** technologique innovante, ce qui attire fortement les profils d'ingénieurs en quête de sens.
