# yield_prediction.py

def predict_yield(crop, temp, hum, rain, soil):
    # Placeholder: use simple formula or ML model here
    base_yield = {
        "Rice": 30, "Wheat": 28, "Maize": 25, "Sugarcane": 50, "Groundnut": 20
    }
    factor = (temp * 0.2 + hum * 0.1 + rain * 0.05)
    soil_factor = {"Loamy": 1.0, "Clay": 0.9, "Sandy": 0.8}
    return base_yield.get(crop, 25) * soil_factor.get(soil, 1) * factor / 100

def generate_yield_trend(crop, soil):
    # Simulate yield data from 2018 to 2024
    import random
    base = {"Rice": 25, "Wheat": 22, "Maize": 20, "Sugarcane": 45, "Groundnut": 18}
    soil_adj = {"Loamy": 1.0, "Clay": 0.9, "Sandy": 0.85}
    return [{"year": year, "yield": base[crop] * soil_adj[soil] + random.uniform(-2, 2)} for year in range(2018, 2025)]
