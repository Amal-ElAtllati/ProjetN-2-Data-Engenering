import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Setup
sns.set_theme(style="whitegrid")
con = duckdb.connect()
output_dir = 'Livrables/images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Exporting real plots from Step 3 data...")

# Figure 1 - Map
print("Generating Map...")
query_map = """
SELECT ville, SUM(nb_offres) as total_offres 
FROM read_parquet('mexora_rh_lake/data_lake/gold/offres_par_ville.parquet')
GROUP BY ville
"""
df_map = con.execute(query_map).df()
coords = {
    'Casablanca': (33.5731, -7.5898), 'Rabat': (34.0209, -6.8416), 
    'Tanger': (35.7595, -5.8340), 'Marrakech': (31.6295, -7.9811),
    'Fès': (34.0331, -5.0003), 'Agadir': (30.4278, -9.5981)
}
df_map['lat'] = df_map['ville'].map(lambda x: coords.get(x, (np.nan, np.nan))[0])
df_map['lon'] = df_map['ville'].map(lambda x: coords.get(x, (np.nan, np.nan))[1])
df_map = df_map.dropna(subset=['lat'])

plt.figure(figsize=(8, 10))
plt.scatter(df_map['lon'], df_map['lat'], s=df_map['total_offres']*2, alpha=0.6, c='royalblue', edgecolors='white')
for i, row in df_map.iterrows():
    plt.text(row['lon']+0.15, row['lat'], f"{row['ville']} ({int(row['total_offres'])})", fontsize=10, fontweight='bold')
plt.title('Figure 1 — Répartition géographique des offres IT au Maroc', fontsize=14)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'map_real.png'), dpi=150)
plt.close()

# Figure 2 - Boxplot
print("Generating Boxplot...")
# Note: salaires_par_profil has columns: profil, ville, salaire_median_mad, etc.
query_boxplot = """
SELECT profil, salaire_median_mad 
FROM read_parquet('mexora_rh_lake/data_lake/gold/salaires_par_profil.parquet')
"""
df_box = con.execute(query_boxplot).df()
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_box, x='salaire_median_mad', y='profil', palette='viridis')
plt.title('Figure 2 — Distribution des salaires par profil IT', fontsize=14)
plt.xlabel('Salaire Médian (MAD)')
plt.ylabel('Profil')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'boxplot_real.png'), dpi=150)
plt.close()

# Figure 3 - Trends
print("Generating Trends...")
query_evo = """
SELECT annee || '-' || mois as date_str, profil, nb_offres
FROM read_parquet('mexora_rh_lake/data_lake/gold/tendances_mensuelles.parquet')
WHERE profil IN ('Data Engineer', 'Data Analyst', 'Data Scientist')
ORDER BY annee, mois
"""
df_evo = con.execute(query_evo).df()
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_evo, x='date_str', y='nb_offres', hue='profil', marker='o', linewidth=2.5)
plt.title('Figure 3 — Évolution mensuelle des offres Data (2023-2024)', fontsize=14)
plt.xlabel('Période')
plt.ylabel('Nombre d\'offres')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'trends_real.png'), dpi=150)
plt.close()

# Figure 4 - Top 15 des compétences IT
print("Generating Top Skills...")
query_skills = """
SELECT competence, famille, SUM(nb_offres_mentionnent) as total_mentions
FROM read_parquet('mexora_rh_lake/data_lake/gold/top_competences.parquet')
GROUP BY competence, famille
ORDER BY total_mentions DESC
LIMIT 15;
"""
df_skills = con.execute(query_skills).df()
plt.figure(figsize=(10, 6))
sns.barplot(data=df_skills, x='total_mentions', y='competence', hue='famille', dodge=False)
plt.title('Figure 4 — Top 15 des compétences les plus demandées', fontsize=14)
plt.xlabel('Nombre d\'offres')
plt.ylabel('Compétence')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_skills_real.png'), dpi=150)
plt.close()

print("All plots exported successfully to Livrables/images/")
