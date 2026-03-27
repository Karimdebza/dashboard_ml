import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

n_clients = 100
n_produits = 10
n_jours = 180  # environ 6 mois

clients = [f"C{str(i).zfill(3)}" for i in range(1, n_clients+1)]
produits = [f"Produit_{i}" for i in range(1, n_produits+1)]
regions = ['Nord', 'Sud', 'Est', 'Ouest']

dataset = []

for _ in range(n_jours * 10):
    date = fake.date_between(start_date='-6M', end_date='today')
    client = random.choice(clients)
    produit = random.choice(produits)
    prix = round(random.uniform(10, 100), 2)
    quantite = random.randint(1, 5)
    region = random.choice(regions)
    
    dataset.append([date, client, produit, prix, quantite, region])

df = pd.DataFrame(dataset, columns=['date', 'client_id', 'produit', 'prix', 'quantite', 'region'])
df['ca'] = df['prix'] * df['quantite']
df.to_csv('ventes.csv', index=False)

print("Données de ventes générées et sauvegardées dans 'ventes.csv'")