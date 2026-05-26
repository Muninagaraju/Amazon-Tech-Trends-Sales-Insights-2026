# ==========================================
# AMAZON E-COMMERCE DASHBOARD
# ==========================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------
# Page Config
# ------------------------------------------

st.set_page_config(
    page_title="Amazon Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------
# Custom CSS Styling
# ------------------------------------------

st.markdown("""
<style>

.main{
background: linear-gradient(
135deg,
#0F172A,
#1E293B,
#334155
);
color:white;
}

.stMetric {
background-color:#1E293B;
padding:15px;
border-radius:15px;
box-shadow:0px 0px 15px rgba(0,255,255,0.4);
}

h1{
color:#38BDF8;
text-align:center;
}

[data-testid="stSidebar"]{
background-color:#111827;
}

</style>
""",unsafe_allow_html=True)

# ------------------------------------------
# Load Dataset
# ------------------------------------------

@st.cache_data
def load_data():

    df=pd.read_csv("amazon_sales.csv")

    df['purchase_date']=pd.to_datetime(
        df['purchase_date'],
        errors='coerce'
    )

    df=df.drop_duplicates()

    return df


df=load_data()

# ------------------------------------------
# Dashboard Title
# ------------------------------------------

st.title("🛒 Amazon E-Commerce Dashboard")

st.write("Interactive Sales Analysis Dashboard")

# ------------------------------------------
# Sidebar Filters
# ------------------------------------------

st.sidebar.header("Filters")

category=st.sidebar.multiselect(
"Select Category",
df['category'].unique(),
default=df['category'].unique()
)

device=st.sidebar.multiselect(
"Select Device",
df['device'].unique(),
default=df['device'].unique()
)

payment=st.sidebar.multiselect(
"Payment Method",
df['payment_method'].unique(),
default=df['payment_method'].unique()
)

filtered_df=df[
(df['category'].isin(category))&
(df['device'].isin(device))&
(df['payment_method'].isin(payment))
]

# ------------------------------------------
# KPI CARDS
# ------------------------------------------

total_revenue=filtered_df['final_price'].sum()

orders=len(filtered_df)

best_category=(
filtered_df.groupby(
'category'
)['final_price']
.sum()
.idxmax()
)

returns=filtered_df[
filtered_df['is_returned']==1
].shape[0]


col1,col2,col3,col4=st.columns(4)

col1.metric(
"💰 Revenue",
f"₹{total_revenue:,.0f}"
)

col2.metric(
"📦 Orders",
orders
)

col3.metric(
"🏆 Best Category",
best_category
)

col4.metric(
"↩ Returns",
returns
)

st.divider()

# ------------------------------------------
# TABS
# ------------------------------------------

tab1,tab2,tab3,tab4=st.tabs([
"Sales",
"Brands",
"Customers",
"Insights"
])

# =====================================
# SALES TAB
# =====================================

with tab1:

    col1,col2=st.columns(2)

    with col1:

        category_sales=filtered_df.groupby(
        'category'
        )['final_price'].sum().reset_index()

        fig=px.bar(
        category_sales,
        x='category',
        y='final_price',
        color='final_price',
        title="Sales by Category"
        )

        st.plotly_chart(
        fig,
        use_container_width=True
        )


    with col2:

        monthly=filtered_df.copy()

        monthly['month']=monthly[
        'purchase_date'
        ].dt.month

        monthly_sales=monthly.groupby(
        'month'
        )['final_price'].sum().reset_index()

        fig=px.line(
        monthly_sales,
        x='month',
        y='final_price',
        markers=True,
        title="Monthly Sales Trend"
        )

        st.plotly_chart(
        fig,
        use_container_width=True
        )


# =====================================
# BRAND TAB
# =====================================

with tab2:

    brand_sales=filtered_df.groupby(
    'brand'
    )['final_price'].sum().reset_index()

    brand_sales=brand_sales.sort_values(
    by='final_price',
    ascending=False
    ).head(10)

    fig=px.bar(
    brand_sales,
    x='final_price',
    y='brand',
    orientation='h',
    color='final_price',
    title='Top 10 Brands'
    )

    st.plotly_chart(
    fig,
    use_container_width=True
    )


# =====================================
# CUSTOMER TAB
# =====================================

with tab3:

    col1,col2=st.columns(2)

    with col1:

        payment_data=filtered_df.groupby(
        'payment_method'
        )['final_price'].sum().reset_index()

        fig=px.pie(
        payment_data,
        names='payment_method',
        values='final_price',
        hole=0.5,
        title="Payment Methods"
        )

        st.plotly_chart(
        fig,
        use_container_width=True
        )



    with col2:

        device_data=filtered_df.groupby(
        'device'
        )['final_price'].sum().reset_index()

        fig=px.bar(
        device_data,
        x='device',
        y='final_price',
        color='device',
        title='Device Sales'
        )

        st.plotly_chart(
        fig,
        use_container_width=True
        )



# =====================================
# INSIGHTS TAB
# =====================================

with tab4:

    st.subheader(
    "Business Insights"
    )

    st.success(
    f"""
    Total Revenue Generated:
    ₹{total_revenue:,.0f}
    """
    )

    st.info(
    f"""
    Best Category:
    {best_category}
    """
    )

    st.warning(
    f"""
    Most Used Device:
    {filtered_df['device'].mode()[0]}
    """
    )

    st.error(
    f"""
    Highest Sales City:
    {
    filtered_df.groupby(
    'location'
    )['final_price']
    .sum()
    .idxmax()
    }
    """
    )


st.divider()

st.caption(
"Created by Muninagaraju 🚀"
)