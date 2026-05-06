import nbformat

def fix_seaborn_warnings(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == 'code':
            lines = cell.source.splitlines()
            new_lines = []
            for line in lines:
                # Fix barplot for salaries
                if "sns.barplot(data=df_salaires, x='salaire_median_moyen', y='profil', palette=\"viridis\")" in line:
                    line = line.replace("palette=\"viridis\")", "hue='profil', palette=\"viridis\", legend=False)")
                # Fix barplot for concurrents
                elif "sns.barplot(data=df_concurrents, x='nb_offres_publiees', y='entreprise', palette=\"magma\")" in line:
                    line = line.replace("palette=\"magma\")", "hue='entreprise', palette=\"magma\", legend=False)")
                # Fix boxplot for profiles
                elif "sns.boxplot(data=df_box, x='salaire_median_mad', y='profil', palette='Set3')" in line:
                    line = line.replace("palette='Set3')", "hue='profil', palette='Set3', legend=False)")
                new_lines.append(line)
            cell.source = '\n'.join(new_lines)

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

if __name__ == "__main__":
    fix_seaborn_warnings('Livrables/Étape 3 — Analyse DuckDB.ipynb')
    print("Notebook updated successfully.")
