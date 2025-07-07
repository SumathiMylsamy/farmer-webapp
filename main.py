# main.py – Farmer Support WebApp with Role-Based Login (Farmer & Admin)
import streamlit as st
import requests
import json
import os
import pandas as pd
import plotly.express as px
from advisory_rules import get_advisory
from crop_suggestion import suggest_crops
from yield_prediction import predict_yield, generate_yield_trend
from admin_dashboard import show_admin_dashboard 
import joblib
from plant_disease_detector import show_disease_detector

USER_FILE = "users.json"
API_KEY = "RM9DJWP8LRWRYH7D6K569DBXJ"

# ------------------ Utility Functions ------------------
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ------------------ Login Page ------------------
def login_page():
    users = load_users()

    st.markdown("""
        <div class="login-card">
            <img src="https://cdn-icons-png.flaticon.com/512/3208/3208710.png" class="login-logo" />
            <h2>🌾Login Page</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    username = st.text_input("👤 Username", key="username_input", placeholder="Enter your username")
    password = st.text_input("🔑 Password", type="password", key="password_input", placeholder="Enter your password")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔐 Login", key="login_button"):
            if username in users and users[username]["password"] == password:
                st.session_state["user"] = username
                st.session_state["role"] = users[username]["role"]
                st.session_state["page"] = "dashboard"
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    with col2:
        if st.button("🆕 New User? Register"):
            st.session_state["page"] = "register"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ Register Page ------------------
def register_page():
    users = load_users()

    st.markdown("""
        <div class="login-card">
            <img src="https://cdn-icons-png.flaticon.com/512/2919/2919600.png" class="login-logo" />
            <h2>🆕 <span style='color:white'>Register New User</span></h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Full Name")
        new_user = st.text_input("💼 Choose a Username")
        role = st.selectbox("👥 Select Role", ["farmer", "admin"], key="role_select")

    with col2:
        new_pass = st.text_input("🔑 Choose a Password", type="password")
        confirm_pass = st.text_input("✅ Confirm Password", type="password")

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns([1, 1])
    with col3:
        if st.button("📅 Register"):
            if not name or not new_user or not new_pass or not confirm_pass:
                st.warning("All fields are required.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            elif new_user in users:
                st.error("Username already exists.")
            else:
                users[new_user] = {"password": new_pass, "role": role}
                save_users(users)
                st.success("✅ Registered successfully. Please login.")
                st.session_state["page"] = "login"
                st.rerun()

    with col4:
        if st.button("🔙 Back to Login"):
            st.session_state["page"] = "login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ Styling ------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)),
                    url("https://plus.unsplash.com/premium_photo-1670909649532-d1d68ee475cd?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main .block-container {
        backdrop-filter: blur(3px);
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 12px;
        padding: 2rem;
    }

    .login-card {
        text-align: center;
        margin-top: 30px;
    }

    .login-logo {
        width: 120px;
        margin-bottom: 10px;
    }

    .login-card h2 {
        color:white;
        font-size: 28px;
    }

    .login-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-bottom: 15px;
    }

    .login-box > div[data-testid="stTextInput"] {
        width: 90% !important;
        max-width: 320px;
        margin-bottom: 12px;
    }

    .login-box > div[data-testid="stTextInput"] input {
        height: 38px;
        font-size: 15px;
        border-radius: 8px;
    }
    button[kind="primary"], button[kind="secondary"], .stButton>button {
        display: block;
        margin: 10px auto;
        padding: 10px 25px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
        background-color: #4CAF50;
        color: white;
        border: none;
        transition: background 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
    }
    button[kind="primary"]:hover, button[kind="secondary"]:hover, .stButton>button:hover {
        background-color: #388e3c !important;
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

def show_farmer_dashboard():
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio("Go to", [
        "🌦️ Weather Advisory",
        "📈 Market Prices",
        "🌱 Crop Suggestions",
        "📋 Government Schemes",
        "📉 Yield Prediction",
        "💰 Income & Profit Estimator",
        "🧠 Plant Disease Detection"

    ])

    # 1. Weather Advisory
    if page == "🌦️ Weather Advisory":
        st.subheader("📍 Get Local Weather & Farming Advice")
        location = st.text_input("Enter your City or Village name:")
        if st.button("🔍 Get Weather Advisory"):
            if not location.strip():
                st.warning("Please enter a valid location.")
            else:
                url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=metric&key={API_KEY}&contentType=json"
                try:
                    response = requests.get(url)
                    data = response.json()
                    if "days" not in data:
                        st.error("❌ Location not found or API issue.")
                    else:
                        today = data["days"][0]
                        weather_data = {
                            "temp": today["temp"],
                            "humidity": today["humidity"],
                            "wind": today["windspeed"],
                            "precip": today["precip"]
                        }
                        cols = st.columns(4)
                        cols[0].metric("🌡️ Temp", f"{weather_data['temp']}°C")
                        cols[1].metric("💧 Humidity", f"{weather_data['humidity']}%")
                        cols[2].metric("🌧️ Rainfall", f"{weather_data['precip']} mm")
                        cols[3].metric("💨 Wind", f"{weather_data['wind']} km/h")

                        st.markdown("### ✅ Recommended Actions")
                        for tip in get_advisory(weather_data):
                            st.success(f"✔️ {tip}")
                except Exception as e:
                    st.error("⚠️ Failed to get weather data. Please try again.")

    # 2. Market Prices
    elif page == "📈 Market Prices":
        st.subheader("🤖 AI-based Market Price Prediction")
        crop = st.selectbox("Crop", ["Rice", "Wheat", "Maize"])
        state = st.selectbox("State", ["Tamil Nadu", "Punjab", "Maharashtra"])
        month = st.selectbox("Month", ["January", "March", "June"])
        temp = st.slider("🌡️ Temperature (°C)", 10, 45, 30)
        rain = st.slider("🌧️ Rainfall (mm)", 0, 300, 100)

        if st.button("📊 Predict Price"):
            try:
                model = joblib.load("market_price_model.pkl")
                features = joblib.load("model_features.pkl")
                input_data = {
                    "temp": temp,
                    "rainfall": rain,
                    f"crop_{crop}": 1,
                    f"state_{state}": 1,
                    f"month_{month}": 1
                }
                input_df = pd.DataFrame([{col: input_data.get(col, 0) for col in features}])
                price = model.predict(input_df)[0]
                st.success(f"💰 Predicted Market Price: ₹{price:.2f} per quintal")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    # 3. Crop Suggestions
    elif page == "🌱 Crop Suggestions":
        st.subheader("🌿 Get Smart Crop Recommendations")
        temperature = st.slider("Temperature (°C)", 0, 50, 30)
        humidity = st.slider("Humidity (%)", 0, 100, 60)
        soil = st.selectbox("Soil Type", ["Loamy", "Clay", "Sandy"], key="suggest_soil")
        crops = suggest_crops(temperature, humidity, soil)
        if crops:
            st.success("🌱 Suitable Crops:")
            for crop in crops:
                st.write(f"- {crop}")
        else:
            st.warning("❌ No suggestions available.")

    # 4. Government Schemes
    elif page == "📋 Government Schemes":
        st.subheader("📋 Government Schemes for Farmers")
        try:
            with open("scheme_data.json") as f:
                schemes = json.load(f)

            for idx, scheme in enumerate(schemes):
                with st.expander(f"📌 {scheme['title']}"):
                    st.markdown(f"**Eligibility:** {scheme['eligibility']}")
                    st.markdown(f"**Benefits:** {scheme['benefits']}")

                    form_key = f"form_visible_{idx}"
                    st.session_state.setdefault(form_key, False)

                    if not st.session_state[form_key]:
                        if st.button(f"📝 Apply Now", key=f"apply_{idx}"):
                            st.session_state[form_key] = True
                            st.rerun()

                    if st.session_state[form_key]:
                        with st.form(key=f"form_{idx}"):
                            st.markdown("### 📝 Application Form")
                            name = st.text_input("👤 Full Name", key=f"name_{idx}")
                            aadhar = st.text_input("📇 Aadhar Number", key=f"aadhar_{idx}")
                            mobile = st.text_input("📱 Mobile Number", key=f"mobile_{idx}")
                            address = st.text_area("🏠 Address", key=f"address_{idx}")
                            submit = st.form_submit_button("📤 Submit Application")

                            if submit:
                                if not name or not aadhar or not mobile:
                                    st.warning("⚠️ All fields are required.")
                                else:
                                    application = {
                                        "scheme": scheme.get("title", "Unknown"),
                                        "name": name,
                                        "aadhar": aadhar,
                                        "mobile": mobile,
                                        "address": address
                                    }
                                    if os.path.exists("applications.json"):
                                        with open("applications.json", "r") as f:
                                            existing = json.load(f)
                                    else:
                                        existing = []
                                    existing.append(application)
                                    with open("applications.json", "w") as f:
                                        json.dump(existing, f, indent=4)
                                    st.success("✅ Application submitted successfully!")
                                    st.session_state[form_key] = False
                                    st.rerun()
        except Exception as e:
            st.error(f"❌ Error loading schemes: {e}")

    # 5. Yield Prediction
    elif page == "📉 Yield Prediction":
        st.subheader("📉 Predict Crop Yield")
        crop = st.selectbox("Select Crop", ["Rice", "Wheat", "Maize", "Sugarcane", "Groundnut"], key="yield_crop")
        temp = st.slider("🌡️ Temperature (°C)", 0, 50, 30, key="yield_temp")
        hum = st.slider("💧 Humidity (%)", 0, 100, 60, key="yield_hum")
        rain = st.slider("🌧️ Rainfall (mm)", 0, 300, 100, key="yield_rain")
        soil = st.selectbox("Soil Type", ["Loamy", "Clay", "Sandy"], key="yield_soil")

        if st.button("📊 Predict Yield"):
            yield_val = predict_yield(crop, temp, hum, rain, soil)
            st.success(f"✅ Estimated Yield: {yield_val:.2f} quintals/acre")

        if st.button("📉 Show Yield Trend"):
            trend_data = generate_yield_trend(crop, soil)
            df = pd.DataFrame(trend_data)
            fig = px.line(df, x="year", y="yield", markers=True,
                          title=f"{crop} Yield Trend (Simulated)",
                          labels={"yield": "Yield (quintals/acre)", "year": "Year"})
            fig.update_traces(line=dict(color='green', width=3))
            st.plotly_chart(fig, use_container_width=True)

    # 6. Income Estimator
    elif page == "💰 Income & Profit Estimator":
        st.subheader("💰 Estimate Your Farming Income and Profit")
        crop = st.selectbox("Select Crop", ["Rice", "Wheat", "Maize", "Sugarcane", "Groundnut"], key="income_crop")
        land_area = st.number_input("Enter Land Area (in acres)", min_value=0.0, format="%.2f", step=0.1, key="income_land")
        temp = st.slider("🌡️ Temperature (°C)", 0, 50, 30, key="income_temp")
        hum = st.slider("💧 Humidity (%)", 0, 100, 60, key="income_hum")
        rain = st.slider("🌧️ Rainfall (mm)", 0, 300, 100, key="income_rain")
        soil = st.selectbox("Soil Type", ["Loamy", "Clay", "Sandy"], key="income_soil")
        cost_per_acre = st.number_input("💸 Estimated Cost per Acre (₹)", min_value=0.0, value=10000.0, step=500.0)

        if st.button("📈 Estimate Income & Profit"):
            try:
                yield_val = predict_yield(crop, temp, hum, rain, soil)
                model = joblib.load("market_price_model.pkl")
                features = joblib.load("model_features.pkl")
                input_data = {
                    "temp": temp,
                    "rainfall": rain,
                    f"crop_{crop}": 1,
                    f"state_Tamil Nadu": 1,
                    f"month_June": 1
                }
                input_df = pd.DataFrame([{col: input_data.get(col, 0) for col in features}])
                market_price = model.predict(input_df)[0]
                total_income = yield_val * land_area * market_price
                total_cost = cost_per_acre * land_area
                net_profit = total_income - total_cost

                st.success(f"""
                ✅ **Estimated Yield:** {yield_val:.2f} quintals/acre  
                ✅ **Market Price:** ₹{market_price:.2f}/quintal  
                ✅ **Total Land:** {land_area:.2f} acres  
                💰 **Estimated Income:** ₹{total_income:,.2f}  
                💸 **Estimated Cost:** ₹{total_cost:,.2f}  
                🟢 **Net Profit:** ₹{net_profit:,.2f}
                """)

                if net_profit < 0:
                    st.error("⚠️ Your estimated cost is higher than income. Consider switching crops or improving yield.")
                elif net_profit < total_cost * 0.2:
                    st.warning("⚠️ Profit margin is low. Consider cost optimization or better crop selection.")
                else:
                    st.balloons()
            except Exception as e:
                st.error(f"❌ Error: {e}")
                
    # 7. Plant Disease Detection            
    elif page == "🧠 Plant Disease Detection":
        show_disease_detector()

# ✅ Always initialize session state before using keys
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# 🔐 Routing
if st.session_state["page"] == "login":
    login_page()
elif st.session_state["page"] == "register":
    register_page()
elif st.session_state.get("page") == "dashboard" and st.session_state.get("user"):
    st.sidebar.success(f"Logged in as {st.session_state['user']} ({st.session_state['role']})")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    if st.session_state["role"] == "farmer":
        show_farmer_dashboard()
    elif st.session_state["role"] == "admin":
        show_admin_dashboard()
else:
    st.warning("Unauthorized access. Please login.")
    st.session_state["page"] = "login"
    st.rerun()