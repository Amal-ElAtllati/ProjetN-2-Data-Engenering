# Document de Conception de l'Architecture Data Lake - Mexora RH Intelligence

## 1. Justification des Formats de Stockage

| Zone | Format Choisi | Pourquoi ce format ? | Pourquoi pas les autres ? |
| :--- | :--- | :--- | :--- |
| **Bronze** | JSON | Permet de stocker les données semi-structurées et imbriquées (ex: listes de compétences, métadonnées variables) exactement telles qu'elles ont été reçues ("Schema-less"). C'est idéal pour des données issues de scraping. | Pas Parquet : Parquet nécessite un schéma strict. S'il y a un changement inattendu dans la structure d'une offre scrappée, l'ingestion Parquet échouera. Pas CSV : Impossible de gérer facilement les listes imbriquées (comme `langue_requise`). |
| **Silver** | Parquet | Format de stockage orienté colonne, fortement typé et compressé (ex: Snappy). Les requêtes sont beaucoup plus rapides car seules les colonnes nécessaires sont lues. Il impose un schéma, ce qui garantit la qualité des données à ce stade. | Pas JSON : JSON est lent à lire pour des requêtes analytiques et prend beaucoup d'espace disque. Pas CSV : CSV n'a pas de types de données stricts, ce qui oblige à re-typer les données à chaque lecture. |
| **Gold** | Parquet | Les mêmes avantages que pour la zone Silver. De plus, Parquet est nativement et très efficacement supporté par le moteur analytique DuckDB utilisé pour l'analyse finale. | Pas CSV/JSON : Mêmes raisons. Pas de base de données relationnelle lourde : Un fichier Parquet permet une analyse locale via DuckDB, sans nécessiter d'infrastructure complexe (Serverless analytics). |

## 2. Questions de Conception

### Pourquoi conserver les données brutes en zone Bronze sans les modifier ? Quels risques si on ne le fait pas ?
La zone Bronze doit être **immuable**. Elle sert d'archive de l'état initial des données. 
**Risques si on modifie les données :** Si nous découvrons plus tard qu'une règle de nettoyage appliquée en zone Silver était fausse (par exemple, un mauvais Regex pour les salaires), nous pourrons toujours relancer le pipeline depuis la zone Bronze. Si nous avions écrasé les données brutes, l'information originale serait perdue à jamais. De plus, pour des raisons de conformité et d'auditabilité, il faut pouvoir prouver l'origine des données.

### Qu'est-ce que le "schema-on-read" ? En quoi est-ce différent du DWH ("schema-on-write") ?
Dans une approche **Schema-on-read** (typique d'un Data Lake), les données sont stockées sous leur forme brute sans vérification de schéma (zone Bronze). Le schéma et la structure ne sont appliqués que lorsque les données sont lues pour être transformées vers Silver.
Dans une approche **Schema-on-write** (typique d'un Data Warehouse traditionnel), les données doivent être transformées et structurées *avant* d'être chargées dans la base. Si une nouvelle colonne apparaît, le chargement échoue jusqu'à ce que la table cible soit modifiée. Le Data Lake est donc beaucoup plus agile pour l'ingestion de sources variées.

### Comment définit-on la partition dans chaque zone ?
- **Bronze (par_source / par_mois) :** La partition naturelle d'ingestion. On charge généralement les données depuis une source donnée (ex: LinkedIn) pour une période donnée. Cela facilite les reprises d'ingestion en cas de panne sur une source.
- **Silver (par_ville / par_mois) :** La partition naturelle d'analyse. Les requêtes RH chercheront souvent à isoler les données par ville (ex: le marché à Tanger vs Casablanca). Partitionner par ville permet d'éviter de scanner toutes les données nationales.

### Comment éviter que le Data Lake devienne un "Data Swamp" ?
Un "Data Swamp" (marécage de données) est un Data Lake où l'on déverse des données sans organisation, devenant inexploitable.
Pour l'éviter, il faut :
1. Mettre en place un catalogue de données (Data Catalog) ou un dictionnaire de métadonnées documentant chaque dataset.
2. Appliquer des conventions de nommage strictes et automatisées.
3. Ne donner l'accès aux zones Silver/Gold qu'aux données qui ont passé des tests de qualité (Data Quality checks).
4. Implémenter des cycles de rétention des données (Data Lifecycle Management).
