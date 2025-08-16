# pages/1_Providers.py

import streamlit as st
from app import db

st.title("Providers")

city = st.text_input("Filter by city (optional)")

# Display providers using correct columns and DataFrame (no list/dict conversion needed)
rows = db.list_providers(city=city if city else None)
st.dataframe(rows, use_container_width=True)  # Correct: DataFrame used directly

st.divider()
st.subheader("Add / Update Provider")

with st.form("provider_form", clear_on_submit=True):

    pid = st.text_input("Provider ID *")
    name = st.text_input("Name *")
    ptype = st.selectbox(
        "Type",
        ["restaurant", "store", "bakery", "caterer", "other"],
        format_func=lambda x: {
            "restaurant": "Restaurant",
            "store": "Grocery Store",
            "bakery": "Bakery",
            "caterer": "Catering Service",
            "other": "Other"
        }.get(x, x.capitalize())
    )
    addr = st.text_input("Address")
    city_val = st.text_input("City *")
    phone = st.text_input("Contact Phone")
    email = st.text_input("Contact Email")
    mode = st.selectbox("Action", ["Create/Replace"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        from app.db import get_conn
        with get_conn() as c:
            c.execute("""
                INSERT OR REPLACE INTO providers
                (provider_id, name, provider_type, address, city, contact_phone, contact_email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (pid, name, ptype, addr, city_val, phone, email))
        st.success(f"Upserted provider {pid}")
