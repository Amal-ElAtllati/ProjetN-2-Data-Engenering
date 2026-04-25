import json
import random
from datetime import datetime, timedelta
import csv

# Constantes
SOURCES = ["rekrute", "marocannonce", "linkedin"]
VILLES_MESSY = ["casa", "CASABLANCA", "Casablanca", "Rabat", "Tanger", "Marrakech", "Fès", "tanger", "RABAT"]
CONTRATS_MESSY = ["CDI", "cdi", "Contrat à durée indéterminée", "Permanent", "Freelance", "CDD", "Stage"]
SALAIRES_MESSY = [
    "15000-20000 MAD", "15K-20K", "Selon profil", None, "Confidentiel",
    "20000-25000 MAD", "10000-15000 MAD", "3000-5000 MAD", "25K-30K", "30000-40000 MAD",
    "1500-2000 EUR", "2000-3000 EUR", "2500-3500 EUR", "5000-6000 EUR",
    "8K-10K", "12K-15K"
]
EXPERIENCES_MESSY = [
    "3-5 ans", "3 à 5 ans", "min 3 ans", "Débutant accepté", None,
    "1-2 ans", "5-7 ans", "Senior (7+ ans)", "10+ ans", "Stage", "Junior"
]
PROFILS_BRUTS = [
    "Dev Data", "Ingénieur Big Data", "Data Eng.", "Développeur BI", "Data Engineer Junior",
    "Développeur Full Stack React/Node.js", "Data Scientist", "Analyste Data", "DevOps",
    "Cloud Engineer", "SysAdmin", "Chef de projet IT", "Architecte Cloud", "Backend Dev",
    "Frontend Angular", "Machine Learning Eng", "BI Analyst", "React JS Developer"
]
SECTEURS = ["Informatique / Télécom", "Banque / Finance", "Conseil", "Autre"]
TELETRAVAIL = ["Hybride", "Total (100% remote)", "Non", "Télétravail partiel"]

# Compétences extraites du référentiel pour les injecter dans le texte
COMPETENCES_MESSY = [
    "React, Node.js, PostgreSQL", "Python, SQL, AWS", "Java, Spring Boot, Oracle",
    "Python, Spark, Kafka, Airflow", "Power BI, SQL, Tableau", "JavaScript, Angular",
    "AWS, GCP, Azure, Docker", "Machine Learning, Python, R, NLP",
    "Python / Django / Git", "• SQL\n• Metabase\n• dbt", "Hadoop, Spark, Python",
    "C++, C#, .NET", "Ruby on Rails, PostgreSQL"
]

def generate_date_between(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def load_companies(filepath):
    companies = []
    with open(filepath, 'r', encoding='utf-8') as f:
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
        # Générer des dates (parfois inversées pour simuler l'erreur intentionnelle)
        date_pub = generate_date_between(start_date, end_date)
        date_exp = date_pub + timedelta(days=random.randint(15, 60))
        
        # 2% des offres ont une date incohérente
        if random.random() < 0.02:
            date_pub_str = date_exp.strftime('%Y-%m-%d')
            date_exp_str = date_pub.strftime('%Y-%m-%d')
        else:
            date_pub_str = date_pub.strftime('%Y-%m-%d')
            date_exp_str = date_exp.strftime('%Y-%m-%d')
            
        # Parfois la date est dans un autre format
        if random.random() < 0.05:
            date_pub_str = date_pub.strftime('%d/%m/%Y')
            
        offre = {
            "id_offre": f"RK-202{random.choice(['3', '4'])}-{random.randint(10000, 99999)}",
            "source": random.choice(SOURCES),
            "titre_poste": random.choice(PROFILS_BRUTS),
            "description": f"Nous recherchons un candidat pour le poste de {random.choice(PROFILS_BRUTS)}. Vous devrez maîtriser {random.choice(COMPETENCES_MESSY)}. Le candidat devra travailler en méthode Agile avec une équipe de {random.randint(3, 10)} personnes. " + " ".join(["bla"] * random.randint(10, 50)),
            "competences_brut": random.choice(COMPETENCES_MESSY) if random.random() < 0.8 else None,
            "entreprise": random.choice(companies),
            "ville": random.choice(VILLES_MESSY),
            "type_contrat": random.choice(CONTRATS_MESSY),
            "experience_requise": random.choice(EXPERIENCES_MESSY),
            "salaire_brut": random.choice(SALAIRES_MESSY),
            "niveau_etudes": random.choice(["Bac+5", "Bac+3", "Bac+2", "Autodidacte", None]),
            "secteur": random.choice(SECTEURS),
            "date_publication": date_pub_str,
            "date_expiration": date_exp_str,
            "nb_postes": random.randint(1, 5),
            "teletravail": random.choice(TELETRAVAIL),
            "langue_requise": random.sample(["Français", "Anglais", "Arabe", "Espagnol"], random.randint(1, 3))
        }
        offres.append(offre)
        
    return {"offres": offres}

if __name__ == "__main__":
    print("Génération de 5000 offres d'emploi IT en cours...")
    data = generate_fake_offers(5000)
    with open('offres_emploi_it_maroc.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Génération terminée : offres_emploi_it_maroc.json créé.")
