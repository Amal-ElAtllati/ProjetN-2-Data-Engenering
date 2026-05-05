import json

notebook_path = 'Livrables/analyse_marche_it_maroc.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Dashboard de synthèse\n",
            "Cette section regroupe les indicateurs clés sous forme de dashboard visuel (4.2)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import numpy as np\n",
            "\n",
            "# 1. Carte du Maroc (Bubble Map simplifiée)\n",
            "query_map = \"\"\"\n",
            "SELECT ville, SUM(nb_offres) as total_offres \n",
            "FROM read_parquet('../mexora_rh_lake/data_lake/gold/offres_par_ville.parquet')\n",
            "GROUP BY ville\n",
            "\"\"\"\n",
            "df_map = con.execute(query_map).df()\n",
            "\n",
            "# Coordonnées approximatives pour les villes principales\n",
            "coords = {\n",
            "    'Casablanca': (33.5731, -7.5898), 'Rabat': (34.0209, -6.8416), \n",
            "    'Tanger': (35.7595, -5.8340), 'Marrakech': (31.6295, -7.9811),\n",
            "    'Fès': (34.0331, -5.0003), 'Agadir': (30.4278, -9.5981)\n",
            "}\n",
            "df_map['lat'] = df_map['ville'].map(lambda x: coords.get(x, (np.nan, np.nan))[0])\n",
            "df_map['lon'] = df_map['ville'].map(lambda x: coords.get(x, (np.nan, np.nan))[1])\n",
            "df_map = df_map.dropna(subset=['lat'])\n",
            "\n",
            "plt.figure(figsize=(8, 8))\n",
            "plt.scatter(df_map['lon'], df_map['lat'], s=df_map['total_offres']*2, alpha=0.6, c='blue')\n",
            "for i, row in df_map.iterrows():\n",
            "    plt.text(row['lon']+0.1, row['lat'], row['ville'], fontsize=12)\n",
            "plt.title('Carte du Maroc - Volume d\\'offres IT par ville (Bubble Map)')\n",
            "plt.xlabel('Longitude')\n",
            "plt.ylabel('Latitude')\n",
            "plt.grid(True)\n",
            "plt.show()\n",
            "\n",
            "# 2. Boxplot salaires\n",
            "query_boxplot = \"\"\"\n",
            "SELECT profil, salaire_median_mad \n",
            "FROM read_parquet('../mexora_rh_lake/data_lake/gold/salaires_par_profil.parquet')\n",
            "\"\"\"\n",
            "df_box = con.execute(query_boxplot).df()\n",
            "plt.figure(figsize=(12, 6))\n",
            "sns.boxplot(data=df_box, x='salaire_median_mad', y='profil', palette='Set3')\n",
            "plt.title('Boxplot des salaires - Distribution par Profil IT')\n",
            "plt.xlabel('Salaire Médian (MAD)')\n",
            "plt.show()\n",
            "\n",
            "# 3. Évolution mensuelle\n",
            "query_evo = \"\"\"\n",
            "SELECT annee || '-' || mois as date_str, profil, nb_offres\n",
            "FROM read_parquet('../mexora_rh_lake/data_lake/gold/tendances_mensuelles.parquet')\n",
            "WHERE profil IN ('Data Engineer', 'Data Analyst', 'Data Scientist')\n",
            "ORDER BY annee, mois\n",
            "\"\"\"\n",
            "df_evo = con.execute(query_evo).df()\n",
            "plt.figure(figsize=(12, 6))\n",
            "sns.lineplot(data=df_evo, x='date_str', y='nb_offres', hue='profil', marker='o')\n",
            "plt.title('Évolution mensuelle des offres Data (2023-2024)')\n",
            "plt.xticks(rotation=45)\n",
            "plt.show()"
        ]
    }
]

# Insert after the last cell
nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated with Dashboard section.")
