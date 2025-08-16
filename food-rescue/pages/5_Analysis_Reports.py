# pages/5_Analysis_Reports.py
import streamlit as st
import plotly.express as px
from app.db import run_query

st.title("Analysis & Reports")

def show_table(title, sql):
    st.subheader(title)
    df = run_query(sql)
    st.dataframe(df, use_container_width=True)
    return df

# 1
show_table("Providers per city", "SELECT city, COUNT(*) AS provider_count FROM providers GROUP BY city")
show_table("Receivers per city", "SELECT city, COUNT(*) AS receiver_count FROM receivers GROUP BY city")

# 2
df = show_table("Provider types by total quantity", """
SELECT provider_type, SUM(quantity) AS total_qty
FROM food_listings GROUP BY provider_type ORDER BY total_qty DESC
""")
if not df.empty:
    st.plotly_chart(px.bar(df, x="provider_type", y="total_qty"), use_container_width=True)

# 3
show_table("Provider contacts by city", "SELECT city, name, contact_phone, contact_email FROM providers ORDER BY city, name")

# 4
show_table("Receivers with most claims", """
SELECT r.name, r.city, COUNT(*) AS claims_count
FROM claims c JOIN receivers r ON r.receiver_id = c.receiver_id
GROUP BY r.receiver_id ORDER BY claims_count DESC
""")

# 5
show_table("Total quantity available", "SELECT SUM(quantity) AS total_available FROM food_listings")

# 6
show_table("City with highest food listings", """
SELECT location AS city, COUNT(*) AS listing_count
FROM food_listings GROUP BY location ORDER BY listing_count DESC LIMIT 1
""")

# 7
df7 = show_table("Most common food types", """
SELECT food_type, COUNT(*) AS cnt FROM food_listings GROUP BY food_type ORDER BY cnt DESC
""")
if not df7.empty:
    st.plotly_chart(px.pie(df7, names="food_type", values="cnt"), use_container_width=True)

# 8
show_table("Claims per food item", "SELECT food_id, COUNT(*) AS claims_cnt FROM claims GROUP BY food_id ORDER BY claims_cnt DESC")

# 9
show_table("Provider with highest completed claims", """
SELECT p.name, COUNT(*) AS completed_claims
FROM claims c JOIN food_listings f ON f.food_id=c.food_id
JOIN providers p ON p.provider_id=f.provider_id
WHERE c.status='completed'
GROUP BY p.provider_id ORDER BY completed_claims DESC LIMIT 1
""")

# 10
df10 = show_table("Claim status distribution (%)", """
SELECT status, ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM claims),2) AS pct
FROM claims GROUP BY status
""")
if not df10.empty:
    st.plotly_chart(px.bar(df10, x="status", y="pct"), use_container_width=True)

# 11
show_table("Average quantity claimed per receiver", """
SELECT r.name, ROUND(AVG(c.quantity_claimed),2) AS avg_qty_claimed
FROM claims c JOIN receivers r ON r.receiver_id = c.receiver_id
GROUP BY r.receiver_id ORDER BY avg_qty_claimed DESC
""")

# 12
df12 = show_table("Most claimed meal types (by qty)", """
SELECT f.meal_type, SUM(c.quantity_claimed) AS total_claimed
FROM claims c JOIN food_listings f ON f.food_id=c.food_id
GROUP BY f.meal_type ORDER BY total_claimed DESC
""")
if not df12.empty:
    st.plotly_chart(px.bar(df12, x="meal_type", y="total_claimed"), use_container_width=True)

# 13
df13 = show_table("Total quantity donated by provider", """
SELECT p.name, SUM(f.quantity) AS total_qty_listed
FROM food_listings f JOIN providers p ON p.provider_id = f.provider_id
GROUP BY p.provider_id ORDER BY total_qty_listed DESC
""")
if not df13.empty:
    st.plotly_chart(px.bar(df13, x="name", y="total_qty_listed"), use_container_width=True)
