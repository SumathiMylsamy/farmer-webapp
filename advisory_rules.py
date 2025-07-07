def get_advisory(data):
    temp = data["temp"]
    humidity = data["humidity"]
    precip = data["precip"]
    wind = data["wind"]

    tips = []

    if temp > 35:
        tips.append("🔆 High temperature! Irrigate crops early morning or late evening.")
    elif temp < 10:
        tips.append("❄️ Low temperature! Protect seedlings with mulch or cover.")
    else:
        tips.append("🌤️ Normal temperature. Maintain regular watering schedule.")

    if precip > 10:
        tips.append("🌧️ Heavy rain forecast! Ensure proper drainage in fields.")
    elif precip > 0:
        tips.append("🌦️ Light rain expected. Reduce irrigation accordingly.")
    else:
        tips.append("☀️ No rain. Plan irrigation accordingly.")

    if humidity > 80:
        tips.append("💧 High humidity. Monitor for fungal diseases like mildew.")
    elif humidity < 30:
        tips.append("🔥 Dry conditions. Increase watering frequency.")
    else:
        tips.append("🧪 Ideal humidity range. No special action needed.")

    if wind > 20:
        tips.append("🌪️ High wind speeds! Protect tender crops with windbreaks.")
    else:
        tips.append("🍃 Calm winds. Normal farming conditions.")

    return tips
