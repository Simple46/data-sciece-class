import streamlit as st
import pandas as pd
import plotly.express as px


# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Jiji Car Market",
    page_icon="🚗",
    layout="wide"
)


# -------------------------
# LOAD DATA
# -------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("New_clean_jiji_automobile.csv")
    return df


df = load_data()


# -------------------------
# TITLE
# -------------------------

st.title("🚗 Jiji Car Market Analysis")

st.markdown(
    "Explore pricing trends, brands, models and vehicle characteristics "
    "in the Nigerian car market."
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Filters")


# Make filter
makes = sorted(df["Make"].dropna().unique())

selected_makes = st.sidebar.multiselect(
    "Car Make",
    options=makes,
    default=[]
)


# Condition filter
conditions = sorted(df["Condition"].dropna().unique())

selected_conditions = st.sidebar.multiselect(
    "Condition",
    options=conditions,
    default=[]
)


# Transmission filter
transmissions = sorted(df["Transmission"].dropna().unique())

selected_transmissions = st.sidebar.multiselect(
    "Transmission",
    options=transmissions,
    default=[]
)


# Year filter
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_year = st.sidebar.slider(
    "Year",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


# Price filter
min_price = float(df["Price"].min())
max_price = float(df["Price"].max())

selected_price = st.sidebar.slider(
    "Price Range (₦)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    step=100000.0,
    format="₦%0.0f"
)


# Reset filters
if st.sidebar.button("Reset Filters"):
    st.rerun()


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_makes:
    filtered_df = filtered_df[
        filtered_df["Make"].isin(selected_makes)
    ]


if selected_conditions:
    filtered_df = filtered_df[
        filtered_df["Condition"].isin(selected_conditions)
    ]


if selected_transmissions:
    filtered_df = filtered_df[
        filtered_df["Transmission"].isin(selected_transmissions)
    ]


filtered_df = filtered_df[
    filtered_df["Year"].between(
        selected_year[0],
        selected_year[1]
    )
]


filtered_df = filtered_df[
    filtered_df["Price"].between(
        selected_price[0],
        selected_price[1]
    )
]


# =========================================================
# KPI SECTION
# =========================================================

total_cars = len(filtered_df)


average_price = (
    filtered_df["Price"].mean()
    if not filtered_df.empty
    else 0
)


if not filtered_df.empty:
    most_common_make = filtered_df["Make"].mode()[0]
else:
    most_common_make = "N/A"


if not filtered_df.empty:
    foreign_used_percentage = (
        (filtered_df["Condition"] == "Foreign Used").mean()
        * 100
    )
else:
    foreign_used_percentage = 0


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Listings",
        f"{total_cars:,}"
    )


with col2:
    st.metric(
        "Average Price",
        f"₦{average_price:,.0f}"
    )


with col3:
    st.metric(
        "Most Common Brand",
        most_common_make
    )


with col4:
    st.metric(
        "Foreign Used",
        f"{foreign_used_percentage:.1f}%"
    )


st.divider()


# =========================================================
# CHECK IF DATA EXISTS
# =========================================================

if filtered_df.empty:

    st.warning(
        "No cars match the selected filters. Try adjusting the filters."
    )

    st.stop()


# =========================================================
# CARS BY MAKE
# =========================================================

st.subheader("🚘 Most Common Car Brands")


make_counts = (
    filtered_df["Make"]
    .value_counts()
    .head(15)
    .reset_index()
)

make_counts.columns = ["Make", "Listings"]


fig = px.bar(
    make_counts,
    x="Make",
    y="Listings",
    title="Number of Listings by Brand",
    text="Listings"
)


fig.update_layout(
    xaxis_title="Car Make",
    yaxis_title="Number of Listings"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# AVERAGE PRICE BY MAKE
# =========================================================

st.subheader("💰 Average Price by Brand")


avg_prices = (
    filtered_df
    .groupby("Make")["Price"]
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)


fig = px.bar(
    avg_prices,
    x="Make",
    y="Price",
    title="Average Price by Brand",
    text_auto=".2s"
)


fig.update_yaxes(
    tickprefix="₦",
    tickformat=","
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CONDITION VS PRICE
# =========================================================

st.subheader("📊 Price Distribution by Condition")


fig = px.box(
    filtered_df,
    x="Condition",
    y="Price",
    color="Condition",
    points="outliers",
    title="Price Distribution by Condition",
    hover_data=["Make", "Model", "Year"]
)


fig.update_yaxes(
    tickprefix="₦",
    tickformat=","
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# YEAR DISTRIBUTION
# =========================================================

st.subheader("📅 Distribution of Car Years")


fig = px.histogram(
    filtered_df,
    x="Year",
    nbins=20,
    title="Distribution of Vehicle Years"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# YEAR VS PRICE
# =========================================================

st.subheader("📈 Year vs Price")


fig = px.scatter(
    filtered_df,
    x="Year",
    y="Price",
    color="Condition",
    hover_data=[
        "Make",
        "Model",
        "Transmission"
    ],
    title="Vehicle Year vs Price"
)


fig.update_yaxes(
    tickprefix="₦",
    tickformat=","
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CORRELATION
# =========================================================

st.subheader("🔥 Correlation Heatmap")


numeric_cols = [
    "Year",
    "Price"
]


corr = filtered_df[numeric_cols].corr()


fig = px.imshow(
    corr,
    text_auto=".2f",
    title="Correlation Between Year and Price"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# TRANSMISSION ANALYSIS
# =========================================================

st.subheader("⚙️ Transmission Analysis")


transmission_summary = (
    filtered_df
    .groupby("Transmission")["Price"]
    .agg(
        Listings="count",
        Average_Price="mean",
        Median_Price="median"
    )
    .reset_index()
)


transmission_summary["Average_Price"] = (
    transmission_summary["Average_Price"]
    .round(0)
)


transmission_summary["Median_Price"] = (
    transmission_summary["Median_Price"]
    .round(0)
)


st.dataframe(
    transmission_summary,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# TOP MODELS
# =========================================================

st.subheader("🏆 Top Models")


model_summary = (
    filtered_df
    .groupby(["Make", "Model"])
    .agg(
        Listings=("Price", "count"),
        Average_Price=("Price", "mean"),
        Median_Price=("Price", "median")
    )
    .sort_values(
        "Listings",
        ascending=False
    )
    .reset_index()
)


model_summary["Average_Price"] = (
    model_summary["Average_Price"]
    .round(0)
)


model_summary["Median_Price"] = (
    model_summary["Median_Price"]
    .round(0)
)


st.dataframe(
    model_summary.head(20),
    use_container_width=True,
    hide_index=True
)
