# pages/2_Receivers.py

import streamlit as st
from app import db
from app import utils  # Correct utility import for city_filter_options

st.set_page_config(page_title="Receivers", layout="wide")

st.title("Receivers")

st.markdown("Browse and filter the list of receivers.")

# City filter
cities = [""] + utils.city_filter_options("receivers")

city = st.selectbox("Filter by city (optional)", cities)

# Get receiver data
rows = db.list_receivers(city if city else None)

if not rows.empty:
    # Rename columns for display if desired, but preserve original names from your database/CSV:
    # receiver_id, name, receiver_type, city, contact_phone, (contact_email if present in table)
    st.dataframe(rows, use_container_width=True)
else:
    st.warning("No receivers found for the selected filter.")
