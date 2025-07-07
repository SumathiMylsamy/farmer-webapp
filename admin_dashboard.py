def show_admin_dashboard():
    import streamlit as st
    if st.session_state.get("role") != "admin":
        st.error("⛔ Access denied. This page is for admin users only.")
        return
    import streamlit as st
    import os
    import json
    import pandas as pd
    import sqlite3

    st.markdown("""
        <style>
        .admin-title {
            color: white;
            font-size: 30px;
            text-align: center;
            margin-bottom: 20px;
        }
        .application-box {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
        }
        .application-box p {
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🛠️ Admin Dashboard - Scheme Manager")

    # ---------------------- SCHEME MANAGEMENT ----------------------
    if "scheme_data.json" in os.listdir():
        with open("scheme_data.json", "r") as f:
            schemes = json.load(f)
    else:
        schemes = []

    st.subheader("📋 Existing Schemes")
    for i, scheme in enumerate(schemes):
        with st.expander(f"{scheme['title']}"):
            scheme['title'] = st.text_input(f"Title {i}", scheme['title'])
            scheme['eligibility'] = st.text_area(f"Eligibility {i}", scheme['eligibility'])
            scheme['benefits'] = st.text_area(f"Benefits {i}", scheme['benefits'])

    if st.button("💾 Save Changes"):
        with open("scheme_data.json", "w") as f:
            json.dump(schemes, f, indent=4)
        st.success("✅ Schemes updated successfully.")

    st.subheader("➕ Add New Scheme")
    new_title = st.text_input("New Scheme Title")
    new_eligibility = st.text_area("New Eligibility")
    new_benefits = st.text_area("New Benefits")

    if st.button("➕ Add Scheme"):
        if new_title and new_eligibility and new_benefits:
            schemes.append({
                "title": new_title,
                "eligibility": new_eligibility,
                "benefits": new_benefits
            })
            with open("scheme_data.json", "w") as f:
                json.dump(schemes, f, indent=4)
            st.success("✅ New scheme added.")
        else:
            st.warning("Please fill all fields.")

    # ---------------------- DISEASE PREDICTION LOGS ----------------------
    st.markdown("---")
    st.title("📊 Disease Prediction Logs & Insights")

    try:
        conn = sqlite3.connect("predictions.db")
        logs = conn.execute("SELECT * FROM predictions ORDER BY timestamp DESC").fetchall()
        if logs:
            df = pd.DataFrame(logs, columns=["Timestamp", "Image Name", "Prediction"])

            st.subheader("📋 Log Table")
            st.dataframe(df)

            # Filter by disease
            disease_filter = st.selectbox("Filter by disease", ["All"] + df["Prediction"].unique().tolist())
            if disease_filter != "All":
                df = df[df["Prediction"] == disease_filter]

            # Summary Chart
            st.subheader("📈 Disease Frequency Chart")
            disease_counts = df["Prediction"].value_counts()
            st.bar_chart(disease_counts)

            # Download Logs
            st.download_button("⬇️ Download Logs as CSV", df.to_csv(index=False), file_name="prediction_logs.csv", mime="text/csv")

            # Clear Logs Button
            if st.button("🧹 Clear All Logs"):
                conn.execute("DELETE FROM predictions")
                conn.commit()
                st.warning("All logs have been cleared.")
        else:
            st.info("No prediction logs found.")
        conn.close()

    except Exception as e:
        st.error(f"Error loading logs: {e}")
