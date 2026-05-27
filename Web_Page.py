# ==========================================
# AMAZON E-COMMERCE DASHBOARD (FIXED VERSION)
# ==========================================

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import requests
import base64
import os

# ==========================================
# PAGE CONFIG
# ==========================================

icon = Image.open("OIP.jpg")

st.set_page_config(
    page_title="Amazon Sales Dashboard",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# THEME
# ==========================================

theme = st.get_option("theme.base")

if theme == "dark":
    ICON_COLOR = "white"
    PLOT_THEME = "plotly_dark"
else:
    ICON_COLOR = "#1B06BD"
    PLOT_THEME = "plotly_white"

# ==========================================
# LOAD DATA (FIXED)
# ==========================================

@st.cache_data
def load_data():

    file_path = "amazon_sales.csv"

    if os.path.exists(file_path):

        df = pd.read_csv(file_path)

        df = df.dropna()
        df = df.drop_duplicates()

        df["purchase_date"] = pd.to_datetime(
            df["purchase_date"],
            format="%d-%m-%Y",
            errors="coerce"
        )

        df = df.dropna(subset=["purchase_date"])

        df["is_returned"] = (
            df["is_returned"]
            .astype(str)
            .str.lower()
            .map({"true": 1, "false": 0})
        )

        return df

    st.error("amazon_sales.csv not found")
    return pd.DataFrame()

# IMPORTANT: CREATE DF HERE
df = load_data()

# SAFETY CHECK
if df is None or df.empty:
    st.stop()

# ==========================================
# HEADER
# ==========================================

col1, col2 = st.columns([1, 6])

with col1:
    st.image("OIP.jpg", width=60)

with col2:
    st.title("Amazon E-Commerce Dashboard")
    st.caption("Interactive Sales Analysis Dashboard")

st.divider()

# ==========================================
# SIDEBAR FILTERS (FIXED)
# ==========================================

st.sidebar.header("Dashboard Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
)

device = st.sidebar.multiselect(
    "Device",
    sorted(df["device"].dropna().unique()),
    default=sorted(df["device"].dropna().unique())
)

payment = st.sidebar.multiselect(
    "Payment Method",
    sorted(df["payment_method"].dropna().unique()),
    default=sorted(df["payment_method"].dropna().unique())
)

filtered_df = df[
    (df["category"].isin(category)) &
    (df["device"].isin(device)) &
    (df["payment_method"].isin(payment))
]

# ==========================================
# KPI
# ==========================================

total_revenue = filtered_df["final_price"].sum()
orders = len(filtered_df)

best_category = filtered_df.groupby("category")["final_price"].sum().idxmax()

returns = filtered_df[filtered_df["is_returned"] == 1].shape[0]

# ==========================================
# KPI DISPLAY
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Revenue", f"₹{total_revenue:,.0f}")

with col2:
    st.metric("Orders", f"{orders:,}")

with col3:
    st.metric("Best Category", best_category)

with col4:
    st.metric("Returns", f"{returns:,}")

# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3, tab4 = st.tabs(
    ["Sales", "Brands", "Customers", "Insights"]
)

# ==========================================
# SALES TAB
# ==========================================

with tab1:

    category_sales = filtered_df.groupby("category")["final_price"].sum().reset_index()

    fig = px.bar(
        category_sales,
        x="category",
        y="final_price",
        template=PLOT_THEME
    )

    st.plotly_chart(fig, use_container_width=True)

    monthly = filtered_df.copy()
    monthly["month"] = monthly["purchase_date"].dt.month

    monthly_sales = monthly.groupby("month")["final_price"].sum().reset_index()

    fig2 = px.line(
        monthly_sales,
        x="month",
        y="final_price",
        markers=True,
        template=PLOT_THEME
    )

    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# BRANDS TAB
# ==========================================

with tab2:

    brand_sales = filtered_df.groupby("brand")["final_price"].sum().reset_index()

    fig = px.bar(
        brand_sales.head(10),
        x="brand",
        y="final_price",
        template=PLOT_THEME
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# CUSTOMER TAB
# ==========================================

with tab3:

    payment_data = filtered_df.groupby("payment_method")["final_price"].sum().reset_index()

    fig = px.pie(
        payment_data,
        names="payment_method",
        values="final_price",
        hole=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# INSIGHTS TAB
# ==========================================

with tab4:

    st.success(f"Revenue: ₹{total_revenue:,.0f}")
    st.info(f"Best Category: {best_category}")
    st.warning(f"Returns: {returns:,}")

# ==========================================
# FOOTER
# ==========================================

st.divider()

col1, col2 = st.columns([1, 8])

with col1:
    st.image("muninagaraju.png", width=60)

with col2:
    st.markdown("""
**Created by Muninagaraju 👨‍💻**  
Data Analyst | Python | SQL | Streamlit
""")
