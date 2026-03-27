# app.py
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import joblib
import requests

# ----------------------
# Constants & API
# ----------------------
API_KEY = "c3b3ebe85bf4e803a516d5c4f9863f51"
CITY = "Marseille"

# ----------------------
# Functions
# ----------------------
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if "main" in data:
        return {
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["main"]
        }
    else:
        return {"temperature": 20, "weather": "Clear"}  # fallback

# ----------------------
# Load data & model
# ----------------------
df = pd.read_csv("ventes.csv")
model = joblib.load("model.pkl")
le_produit = joblib.load("le_produit.pkl")
le_region = joblib.load("le_region.pkl")
le_weather = joblib.load("le_weather.pkl")

# ----------------------
# Initialize app
# ----------------------
app = dash.Dash(__name__, external_stylesheets=["/assets/style.css"])
app.title = "Dashboard Ventes & Prédiction"

# ----------------------
# Layout
# ----------------------
app.layout = html.Div(className="container", children=[

    # Header
    html.Div(className="header", children=[
        html.Img(src="/assets/logo.png", className="logo"),
        html.H1("📊 Dashboard Ventes & Prédiction", className="title")
    ]),

    # Filtres
    html.Div(className="row", children=[
        html.Div(className="card", children=[
            html.H3("Sélection Produit"),
            dcc.Dropdown(
                id="dropdown-produit",
                options=[{"label": p, "value": p} for p in df["produit"].unique()],
                value=df["produit"].unique()[0]
            )
        ]),
        html.Div(className="card", children=[
            html.H3("Sélection Région"),
            dcc.Dropdown(
                id="dropdown-region",
                options=[{"label": r, "value": r} for r in df["region"].unique()],
                value=df["region"].unique()[0]
            )
        ])
    ]),

    # Graphiques + prédiction
    html.Div(className="row", children=[
        html.Div(className="card", children=[
            html.H3("Graphique Ventes"),
            dcc.Graph(id="graph-ventes", className="graph")
        ]),
        html.Div(className="card", children=[
            html.H3("Prédiction Quantité"),
            html.Div(id="prediction-output", className="prediction")
        ])
    ])
])

# ----------------------
# Callbacks interactifs
# ----------------------
@app.callback(
    Output("graph-ventes", "figure"),
    Output("prediction-output", "children"),
    Input("dropdown-produit", "value"),
    Input("dropdown-region", "value")
)
def update_dashboard(produit, region):
    # Filter dataset
    df_filtered = df[(df["produit"]==produit) & (df["region"]==region)]
    
    # Graphique : Ventes par jour
    fig = px.line(df_filtered, x="date", y="quantite", title=f"Ventes de {produit} - {region}")
    
    # Récupération météo actuelle
    weather_data = get_weather()
    
    # Préparer les features pour prédiction
    last_row = df_filtered.iloc[-1]
    X_pred = pd.DataFrame([{
        "mois": pd.to_datetime(last_row["date"]).month,
        "jour": pd.to_datetime(last_row["date"]).day,
        "produit_enc": le_produit.transform([produit])[0],
        "region_enc": le_region.transform([region])[0],
        "prix": last_row["prix"],
        "temperature": weather_data["temperature"],
        "weather_enc": le_weather.transform([weather_data["weather"]])[0]
    }])
    
    # Prédiction ML
    prediction = model.predict(X_pred)[0]
    
    return fig, f"Quantité prévue aujourd'hui : {prediction:.0f} unités"

# ----------------------
# Run server
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)