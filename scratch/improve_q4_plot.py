import nbformat

def improve_correlation_plot(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == 'code' and "scatterplot(data=df_exp" in cell.source:
            # New improved source for the cell
            new_source = """query4 = \"\"\"
SELECT 
    experience_min_ans,
    salaire_median_mad
FROM read_parquet('../mexora_rh_lake/data_lake/silver/offres_clean/offres_clean.parquet')
WHERE salaire_connu = True AND experience_min_ans IS NOT NULL AND experience_min_ans <= 12;
\"\"\"
df_exp = con.execute(query4).df()

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_exp, x='experience_min_ans', y='salaire_median_mad', marker='o', color='teal', linewidth=2.5)
plt.title('Progression du Salaire Médian selon l\\'Expérience', fontsize=14, fontweight='bold')
plt.xlabel('Années d\\'expérience minimales', fontsize=12)
plt.ylabel('Salaire Médian (MAD)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(range(0, 13))
plt.show()"""
            cell.source = new_source

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

if __name__ == "__main__":
    improve_correlation_plot('Livrables/Étape 3 — Analyse DuckDB.ipynb')
    print("Question 4 visualization improved successfully.")
