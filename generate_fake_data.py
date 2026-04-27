import json
import random
import csv
from datetime import datetime, timedelta
import os

# Configuration
SOURCES = ["Rekrute", "MarocAnnonce", "LinkedIn"]
PROFILS_BRUTS = [
    "Data Engineer", "Data Scientist", "Data Analyst", "Développeur Full Stack",
    "Ingénieur Big Data", "Consultant BI", "Expert IA", "Analyste de Données",
    "Dev Data", "Architecte Big Data", "ML Engineer", "Business Intelligence Specialist",
    "Data Architect", "Analyste Reporting", "Ingénieur Cloud & Data"
]
COMPETENCES_MESSY = [
    "Python, SQL, Spark", "Java, AWS, Docker", "R, Statistiques, Tableau",
    "Azure, ETL, SQL Server", "Pandas, Scikit-learn, ML", "Airflow, dbt, Snowflake",
    "NoSQL, MongoDB, Kafka", "Power BI, DAX, SQL", "React, Node.js, JS",
    "Hadoop, Hive, Scala", "Excel, SQL, VBA", "Google Cloud, BigQuery",
    "NLP, TensorFlow, Keras", "Oracle, PL/SQL, Informatica", "Kubernetes, CI/CD, DevOps"
]
CONTRATS_MESSY = ["CDI", "CDD", "Freelance", "Indéterminée", "C.D.I", "Freelance / Indépendant", "Stage"]
EXPERIENCES_MESSY = ["2-5 ans", "Junior (0-2 ans)", "Senior (> 5 ans)", "3 ans exp", "Confirmé", "Débutant", "Expert"]
SALAIRES_MESSY = ["15000 MAD", "12k-18k", "Confidentiel", "25000", "Selon profil", "1800 EUR", "8000 - 12000 DH", "20000 MAD"]
VILLES_MAPPING = {
    "Casablanca": ["casa", "CASABLANCA", "Casablanca"],
    "Rabat": ["Rabat", "RABAT", "rabat"],
    "Tanger": ["Tanger", "tanger"],
    "Marrakech": ["Marrakech"],
    "Fès": ["Fès", "fes"]
}
VILLES_LIST = list(VILLES_MAPPING.keys())
VILLES_WEIGHTS = [0.60, 0.20, 0.08, 0.07, 0.05] # Distribution réaliste : Casa à 60%

def generate_date_between(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def load_companies(csv_path):
    companies = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row['nom_entreprise'])
    return companies

def generate_fake_offers(num_offers=5000):
    companies = load_companies('entreprises_it_maroc.csv')
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 11, 30)
    
    offres = []
    for i in range(1, num_offers + 1):
        # Sélection pondérée de la ville
        ville_choisie = random.choices(VILLES_LIST, weights=VILLES_WEIGHTS, k=1)[0]
        ville_messy = random.choice(VILLES_MAPPING[ville_choisie])
        
        # Dates
        date_pub = generate_date_between(start_date, end_date)
        date_exp = date_pub + timedelta(days=random.randint(15, 60))
        
        if random.random() < 0.02:
            date_pub_str, date_exp_str = date_exp.strftime('%Y-%m-%d'), date_pub.strftime('%Y-%m-%d')
        else:
            date_pub_str, date_exp_str = date_pub.strftime('%Y-%m-%d'), date_exp.strftime('%Y-%m-%d')
            
        if random.random() < 0.05:
            date_pub_str = date_pub.strftime('%d/%m/%Y')
            
        offre = {
            "id_offre": f"RK-202{random.choice(['3', '4'])}-{random.randint(10000, 99999)}",
            "source": random.choice(SOURCES),
            "titre_poste": random.choice(PROFILS_BRUTS),
            "description": f"Nous recherchons un candidat pour le poste de {random.choice(PROFILS_BRUTS)}. Vous devrez maîtriser {random.choice(COMPETENCES_MESSY)}.",
            "competences_brut": random.choice(COMPETENCES_MESSY) if random.random() < 0.8 else None,
            "entreprise": random.choice(companies),
            "ville": ville_messy,
            "type_contrat": random.choice(CONTRATS_MESSY),
            "experience_requise": random.choice(EXPERIENCES_MESSY),
            "salaire_brut": random.choice(SALAIRES_MESSY),
            "date_publication": date_pub_str,
            "date_expiration": date_exp_str,
            "teletravail": random.choice(["Oui", "Non", "Hybride", "Télétravail possible", "100% remote", None])
        }
        offres.append(offre)
    return offres

if __name__ == "__main__":
    print("Génération de 5000 offres d'emploi IT au Maroc...")
    data = {"metadata": {"total": 5000, "date_generation": datetime.now().isoformat()}, "offres": generate_fake_offers(5000)}
    with open('offres_emploi_it_maroc.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Fichier 'offres_emploi_it_maroc.json' généré avec succès.")
