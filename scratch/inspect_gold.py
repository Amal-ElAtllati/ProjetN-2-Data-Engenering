import duckdb
con = duckdb.connect()
print("--- offres_par_ville ---")
print(con.execute("SELECT * FROM 'mexora_rh_lake/data_lake/gold/offres_par_ville.parquet' LIMIT 5").df())
print("\n--- salaires_par_profil ---")
print(con.execute("SELECT * FROM 'mexora_rh_lake/data_lake/gold/salaires_par_profil.parquet' LIMIT 5").df())
print("\n--- tendances_mensuelles ---")
print(con.execute("SELECT * FROM 'mexora_rh_lake/data_lake/gold/tendances_mensuelles.parquet' LIMIT 5").df())
