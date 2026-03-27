import requests

API_KEY = "c3b3ebe85bf4e803a516d5c4f9863f51"  # ta clé valide

def get_weather(city="Marseille"):
    """Retourne la météo actuelle d'une ville (temperature et weather)"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    # Vérification sécurité
    if "main" in data and "weather" in data:
        return {
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["main"]
        }
    else:
        print("⚠️ Problème météo :", data)
        # fallback
        return {"temperature": 20, "weather": "Clear"}