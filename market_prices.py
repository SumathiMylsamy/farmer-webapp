# market_prices.py

def get_market_price(crop_name):
    prices = {
        "wheat": "₹28/kg",
        "rice": "₹40/kg",
        "maize": "₹22/kg",
        "sugarcane": "₹300/quintal",
        "mustard": "₹60/kg",
        "millets": "₹35/kg"
    }
    return prices.get(crop_name.lower(), "Price not available")
