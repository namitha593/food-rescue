import streamlit as st
import pandas as pd
from app import db


def show_provider_types_chart():
    df = db.get_provider_types_by_quantity()
    if not df.empty:
        st.bar_chart(df.set_index("provider_type"))
    else:
        st.info("No data available")


def city_filter_options(table="providers"):
    """Get unique city list for dropdowns."""
    if table == "providers":
        df = db.list_providers()
    elif table == "receivers":
        df = db.list_receivers()
    else:
        return []

    if "city" in df.columns:
        return sorted(df["city"].dropna().unique())
    return []
