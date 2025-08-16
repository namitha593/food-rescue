# pages/3_Food_Listings.py

import streamlit as st
from app import db

st.title("Food Listings")

with st.expander("Filters"):
    f = {}
    f["provider_id"] = st.text_input("Provider ID")
    f["provider_type"] = st.selectbox("Provider Type", ["", "restaurant", "store", "bakery", "caterer", "other"])
    f["location"] = st.text_input("Location (City)")
    f["food_type"] = st.text_input("Food Type")
    f["meal_type"] = st.text_input("Meal Type")

rows = db.list_listings({k: v for k, v in f.items() if v})

# Corrected
if not rows.empty:
    st.dataframe(rows)
else:
    st.warning("No food listings found for selected filters.")

st.subheader("Create / Update / Delete")

tab1, tab2, tab3 = st.tabs(["Create/Update", "Delete", "Lookup"])

with tab1:
    with st.form("listing_form", clear_on_submit=True):
        args = {
            "food_id": st.text_input("Food ID *"),
            "food_name": st.text_input("Food Name *"),
            "quantity": st.number_input("Quantity *", min_value=0, step=1),
            "expiry_date": st.date_input("Expiry Date *").strftime("%Y-%m-%d"),
            "provider_id": st.text_input("Provider ID *"),
            "provider_type": st.selectbox("Provider Type", ["restaurant", "store", "bakery", "caterer", "other"]),
            "location": st.text_input("Location (City)"),
            "food_type": st.text_input("Food Type"),
            "meal_type": st.text_input("Meal Type"),
        }

        action = st.selectbox("Action", ["Create", "Update"])

        submit = st.form_submit_button("Submit")

        if submit:
            if action == "Create":
                db.create_listing(**args)
                st.success(f"Created listing {args['food_id']}")
            else:
                _id = args.pop("food_id")
                db.update_listing(_id, **args)
                st.success(f"Updated listing {_id}")

with tab2:
    fid = st.text_input("Food ID to delete")
    if st.button("Delete"):
        if fid:
            db.delete_listing(fid)
            st.success(f"Deleted listing {fid}")
        else:
            st.error("Please enter a Food ID to delete.")

with tab3:
    fid = st.text_input("Food ID to view")
    if st.button("Get"):
        r = db.get_listing(fid)
        if r:
            st.write(dict(r))
        else:
            st.warning("Listing not found.")
