import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv('ventes.csv')

# ==============================
# FEATURE ENGINEERING
# ==============================
df['date'] = pd.to_datetime(df['date'])
df['mois'] = df['date'].dt.month
df['jour'] = df['date'].dt.day

# ==============================
# ENCODAGE
# ==============================
le_produit = LabelEncoder()
df['produit_enc'] = le_produit.fit_transform(df['produit'])

le_region = LabelEncoder()
df['region_enc'] = le_region.fit_transform(df['region'])

# ==============================
# 🔥 AJOUT METEO (SIMULATION)
# ==============================
df['temperature'] = [random.uniform(10, 30) for _ in range(len(df))]
df['weather'] = [random.choice(['Clear', 'Rain']) for _ in range(len(df))]

le_weather = LabelEncoder()
df['weather_enc'] = le_weather.fit_transform(df['weather'])

# ==============================
# FEATURES / TARGET
# ==============================
X = df[['mois', 'jour', 'produit_enc', 'region_enc', 'prix', 'temperature', 'weather_enc']]
y = df['quantite']

# ==============================
# TRAIN
# ==============================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ==============================
# EVAL
# ==============================
y_pred = model.predict(X_test)

print("R2 score:", r2_score(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))

# ==============================
# SAVE
# ==============================
joblib.dump(model, 'model.pkl')
joblib.dump(le_produit, 'le_produit.pkl')
joblib.dump(le_region, 'le_region.pkl')
joblib.dump(le_weather, 'le_weather.pkl')

print("✅ Modèle et encoders sauvegardés.")