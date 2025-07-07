def suggest_crops(temperature, humidity, soil_type):
    suggestions = []

    if soil_type == "Loamy":
        if 20 <= temperature <= 35 and 50 <= humidity <= 80:
            suggestions.extend(["Wheat", "Rice", "Sugarcane"])
        if 25 <= temperature <= 40:
            suggestions.append("Maize")

    elif soil_type == "Clay":
        if temperature < 30 and humidity > 60:
            suggestions.extend(["Paddy", "Cotton"])
        if 18 <= temperature <= 28:
            suggestions.append("Lentil")

    elif soil_type == "Sandy":
        if temperature > 30:
            suggestions.extend(["Millet", "Groundnut"])
        if humidity < 40:
            suggestions.append("Bajra")

    # Remove duplicates and return
    return list(set(suggestions))
