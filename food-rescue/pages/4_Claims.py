# pages/4_Claims.py

import streamlit as st
from datetime import datetime
from app import db

st.title("Claims")

st.subheader("Create Claim")
with st.form("claim_form", clear_on_submit=True):
    claim_id = st.text_input("Claim ID *")
    food_id = st.text_input("Food ID *")
    receiver_id = st.text_input("Receiver ID *")
    status = st.selectbox("Status", ["pending", "approved", "completed", "canceled"])
    ts = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    qty = st.number_input("Quantity Claimed *", min_value=0, step=1)

    if st.form_submit_button("Submit"):
        db.create_claim(claim_id, food_id, receiver_id, status, ts, qty)
        st.success(f"Claim {claim_id} created")

st.subheader("Update Claim Status")
with st.form("claim_update", clear_on_submit=True):
    cid = st.text_input("Claim ID *")
    new_status = st.selectbox("New Status", ["pending", "approved", "completed", "canceled"])
    if st.form_submit_button("Update"):
        db.update_claim(cid, status=new_status)
        st.success(f"Claim {cid} → {new_status}")

st.subheader("All Claims")
status_filter = st.selectbox("Filter by status", ["", "pending", "approved", "completed", "canceled"])
rows = db.list_claims(status_filter if status_filter else None)
# Corrected
if not rows.empty:
    st.dataframe(rows)
else:
    st.warning("No claims found for the selected filter.")
