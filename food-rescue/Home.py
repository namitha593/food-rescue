import streamlit as st
from app import db

st.set_page_config(page_title="🥗 Food Rescue – Reduce Food Wastage", layout="wide")

st.title("🥗 Food Rescue – Reduce Food Wastage")
st.markdown(
    "This app connects food providers with receivers. Use the left sidebar to navigate: "
    "manage providers, receivers, listings, and claims."
)

# Show total food quantity metric
total_food = db.get_total_food_quantity()
st.metric("Total Food Quantity (all listings)", f"{total_food} kg")

# Optional: Show provider types by quantity chart
st.subheader("Provider Types by Total Quantity")
df_chart = db.get_provider_types_by_quantity()
if not df_chart.empty:
    st.bar_chart(df_chart.set_index("provider_type"))
else:
    st.info("No data available for provider types.")