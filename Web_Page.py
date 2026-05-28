# ==========================================
# AMAZON E-COMMERCE DASHBOARD
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
# CSS
# ==========================================

st.markdown("""
<style>

.main{
padding-top:20px;
}

[data-testid="stSidebar"]{
background-color:#111827;
}

div[data-testid="metric-container"]{
background:#1E293B;
padding:20px;
border-radius:15px;
border:1px solid #38BDF8;
box-shadow:0px 0px 15px rgba(56,189,248,.3);
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# ICON FUNCTIONS
# ==========================================

@st.cache_data
def get_icon(icon_name,color):

    url=f"https://cdn.jsdelivr.net/npm/lucide-static/icons/{icon_name}.svg"

    response=requests.get(url)

    if response.status_code==200:

        svg=response.text

        svg=svg.replace(
            'stroke="currentColor"',
            f'stroke="{color}"'
        )

        return base64.b64encode(
            svg.encode()
        ).decode()

    return None


def st_lucide(icon_name,size=35,color=None):

    if color is None:
        color=ICON_COLOR

    b64=get_icon(
        icon_name,
        color
    )

    if b64:

        st.markdown(
        f"""
        <img src="data:image/svg+xml;base64,{b64}"
        width="{size}">
        """,
        unsafe_allow_html=True
        )


# ==========================================
# LOAD DATA
# ==========================================
import pandas as pd
import streamlit as st
import os


@st.cache_data
def load_data():

    BASE_DIR = os.path.dirname(__file__)

    file_path = os.path.join(
        BASE_DIR,
        "amazon_sales.csv"
    )

    try:
        df = pd.read_csv(file_path)

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
        )

        df["purchase_date"] = pd.to_datetime(
            df["purchase_date"],
            errors="coerce",
            dayfirst=True
        )

        return df

    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()


df = load_data()

filtered_df = df.copy()
# ==========================================
# HEADER
# ==========================================

col1,col2=st.columns([1,6])

with col1:

    st_lucide(
    "shopping-cart",
    70
    )

with col2:

    st.title(
    "Amazon E-Commerce Dashboard"
    )

    st.caption(
    "Interactive Sales Analysis Dashboard"
    )

st.divider()


# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Dashboard Filters")

# CATEGORY (SAFE)
if "category" in df.columns:
    category_options = sorted(df["category"].dropna().unique())
else:
    category_options = []

category = st.sidebar.multiselect(
    "Category",
    category_options,
    default=category_options
)

# DEVICE (SAFE)
if "device" in df.columns:
    device_options = sorted(df["device"].dropna().unique())
else:
    device_options = []

device = st.sidebar.multiselect(
    "Device",
    device_options,
    default=device_options
)

# PAYMENT (SAFE)
if "payment_method" in df.columns:
    payment_options = sorted(df["payment_method"].dropna().unique())
else:
    payment_options = []

payment = st.sidebar.multiselect(
    "Payment Method",
    payment_options,
    default=payment_options
)
# ==========================================
# FILTER DATA (ADD THIS HERE)
# ==========================================

filtered_df = df.copy()

if category:
    filtered_df = filtered_df[filtered_df["category"].isin(category)]

if device:
    filtered_df = filtered_df[filtered_df["device"].isin(device)]

if payment:
    filtered_df = filtered_df[filtered_df["payment_method"].isin(payment)]

# ==========================================
# KPI
# ==========================================
st.write(filtered_df.columns)
st.write(filtered_df)
st.write(filtered_df.columns)
st.write(type(filtered_df))
total_revenue = filtered_df["final_price"].sum()
total_revenue = filtered_df["final_price"].sum()

orders=len(filtered_df)

best_category=(
filtered_df.groupby(
"category"
)["final_price"]
.sum()
.idxmax()
)

returns=filtered_df[
filtered_df[
"is_returned"
]==1
].shape[0]


# ==========================================
# KPI ICON
# ==========================================

def metric_icon(icon,bg_color):

    b64=get_icon(
    icon,
    "white"
    )

    st.markdown(
    f"""
    <div style="
    width:50px;
    height:50px;
    border-radius:50%;
    background:{bg_color};
    display:flex;
    align-items:center;
    justify-content:center;
    margin-bottom:10px;">
    <img src="data:image/svg+xml;base64,{b64}" width="24">
    </div>
    """,
    unsafe_allow_html=True
    )


# ==========================================
# KPI DISPLAY
# ==========================================

col1,col2,col3,col4=st.columns(4)

with col1:

    metric_icon(
    "indian-rupee",
    "#10B981"
    )

    st.metric(
    "Revenue",
    f"₹{total_revenue:,.0f}"
    )


with col2:

    metric_icon(
    "package",
    "#3B82F6"
    )

    st.metric(
    "Orders",
    orders
    )


with col3:

    metric_icon(
    "award",
    "#F59E0B"
    )

    st.metric(
    "Best Category",
    best_category
    )


with col4:

    metric_icon(
    "rotate-ccw",
    "#EF4444"
    )

    st.metric(
    "Returns",
    returns
    )


# ==========================================
# TABS
# ==========================================

tab1,tab2,tab3,tab4=st.tabs(
[
"Sales",
"Brands",
"Customers",
"Insights"
]
)


# ==========================================
# SALES TAB
# ==========================================

with tab1:

    col1,col2=st.columns(2)

    with col1:

        category_sales=(
        filtered_df.groupby(
        "category"
        )["final_price"]
        .sum()
        .reset_index()
        )

        fig=px.bar(
        category_sales,
        x="category",
        y="final_price",
        color="final_price",
        template=PLOT_THEME
        )

        st.plotly_chart(
        fig,
        use_container_width=True
        )


    with col2:

        monthly=filtered_df.copy()

        monthly["month"]=(
        monthly[
        "purchase_date"
        ].dt.month
        )

        monthly_sales=(
        monthly.groupby(
        "month"
        )["final_price"]
        .sum()
        .reset_index()
        )

        fig=px.line(
        monthly_sales,
        x="month",
        y="final_price",
        markers=True,
        template=PLOT_THEME
        )

        st.plotly_chart(
        fig,
        use_container_width=True
        )


# ==========================================
# BRANDS
# ==========================================

with tab2:

    brand_sales=(
    filtered_df.groupby(
    "brand"
    )["final_price"]
    .sum()
    .reset_index()
    )

    fig=px.bar(
    brand_sales.head(10),
    x="brand",
    y="final_price",
    color="final_price",
    template=PLOT_THEME
    )

    st.plotly_chart(
    fig,
    use_container_width=True
    )


# ==========================================
# CUSTOMER
# ==========================================

with tab3:

    col1,col2=st.columns(2)

    with col1:

        payment_data=(
        filtered_df.groupby(
        "payment_method"
        )["final_price"]
        .sum()
        .reset_index()
        )

        fig=px.pie(
        payment_data,
        names="payment_method",
        values="final_price",
        hole=.5,
        template=PLOT_THEME
        )

        st.plotly_chart(
        fig,
        use_container_width=True
        )


    with col2:

        device_data=(
        filtered_df.groupby(
        "device"
        )["final_price"]
        .sum()
        .reset_index()
        )

        fig=px.bar(
        device_data,
        x="device",
        y="final_price",
        color="device",
        template=PLOT_THEME
        )

        st.plotly_chart(
        fig,
        use_container_width=True
        )


# ==========================================
# INSIGHTS
# ==========================================

with tab4:

    st.subheader(
    "Business Insights"
    )

    st.success(
    f"💰 Revenue : ₹{total_revenue:,.0f}"
    )

    st.info(
    f"🏆 Best Category : {best_category}"
    )

    st.warning(
    f"🔄 Returns : {returns:,}"
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

col1,col2=st.columns([1,8])

with col1:

    img=Image.open(
    "muninagaraju.png"
    )

    st.image(
    img,
    width=60
    )

with col2:

    st.markdown("""
**Created by Muninagaraju 👨‍💻**
Data Analyst | Python | SQL | Streamlit
""")
