import streamlit as st

# Dummy user dictionary (replace with real database or JSON later)
VALID_USERS = {
    "farmer": "1234",
    "admin": "admin"
}

def login_page():
    # CSS Styling block
    st.markdown("""
        <style>
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1400&q=80');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .login-card h2 {
            color: white;
            font-size: 30px;
            margin-bottom: 20px;
        }
     
        .login-box label {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }

        .login-links {
            text-align: center;
            margin-top: 15px;
        }

        .login-links a {
            color: white;
            text-decoration: none;
            font-weight: bold;
            font-size: 15px;
        }

        .login-links a:hover {
            text-decoration: underline;
        }

        .login-card {
            text-align: center;
            margin-top: 50px;
        }

        .login-logo {
            width: 100px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Login Heading Section
    st.markdown("""
        <div class="login-card">
            <img src="https://cdn-icons-png.flaticon.com/512/3208/3208710.png" class="login-logo" />
            <h2>🌾 Farmer Login</h2>
        </div>
    """, unsafe_allow_html=True)

    # Login Form Section
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    username = st.text_input("👤 Username", key="username_input")
    password = st.text_input("🔑 Password", type="password", key="password_input")

    if st.button("🔐 Login", key="login_button"):
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state["user"] = username
            st.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

    # Forgot password / New user links
    st.markdown("""
        <div class="login-links">
            <a href="#">🔁 Forgot Password?</a> 
            <a href="#">🆕 New User?  Register</a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
