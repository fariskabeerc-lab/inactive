import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

# --- Page Config ---
st.set_page_config(page_title="Inactive Items Dashboard", layout="wide", page_icon="📊")

# --- Load Data ---
file_path = "Active and Inactive Items Report.xlsx"  # Replace with your actual file
df = pd.read_excel(file_path)

# --- Clean Columns ---
df.columns = df.columns.str.strip()

# --- Calculations ---
df["Unsold_Value"] = df["Stock"] * df["Cost Price"]

# --- Filter: Low Sold, High Stock (Top 30) ---
df_inactive = df.sort_values(by=["Qty Sold", "Stock"], ascending=[True, False]).head(30)

# --- KPI / Big Insights ---
total_unsold_value = df["Unsold_Value"].sum()
top30_unsold_value = df_inactive["Unsold_Value"].sum()
completely_unsold = df[df["Qty Sold"] == 0].shape[0]

st.title("📊 Inactive Items Dashboard - September")

# Big KPI cards
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Unsold Value", f"{total_unsold_value:,.2f}")
col2.metric("📦 Completely Unsold Items", f"{completely_unsold}")
col3.metric("🔥 Top 30 Low-Sold High-Stock Value", f"{top30_unsold_value:,.2f}")

st.markdown("---")

# --- Horizontal Bar Chart (Dark Theme) ---
fig = px.bar(
    df_inactive,
    x="Stock",
    y="Item Name",
    orientation="h",
    text="Qty Sold",
    color="Unsold_Value",
    color_continuous_scale="reds",
    title="🚨 Top 30 Low-Selling Items with High Stock",
    hover_data={
        "Stock": True,
        "Qty Sold": True,
        "Cost Price": True,
        "Unsold_Value": True,
        "Item Name": False
    },
    template="plotly_dark"
)

fig.update_layout(
    yaxis=dict(title="Item", automargin=True),
    xaxis=dict(title="Stock (Units)"),
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    font=dict(color="white"),
    margin=dict(l=200, r=20, t=70, b=40)
)

fig.update_traces(texttemplate="Sold: %{text}", textposition="outside")

st.plotly_chart(fig, use_container_width=True)

# --- Interactive Table for Top 30 ---
st.subheader("📋 Top 30 Inactive Items (Interactive)")
gb_top30 = GridOptionsBuilder.from_dataframe(df_inactive[["Item Code", "Item Name", "Stock", "Qty Sold", "Cost Price", "Unsold_Value"]])
gb_top30.configure_default_column(sortable=True, filter=True, resizable=True)
gb_top30.configure_grid_options(enableRangeSelection=True)
gridOptions_top30 = gb_top30.build()

AgGrid(
    df_inactive[["Item Code", "Item Name", "Stock", "Qty Sold", "Cost Price", "Unsold_Value"]],
    gridOptions=gridOptions_top30,
    height=400,
    width='100%',
    allow_unsafe_jscode=True,
    theme='dark'
)

# --- Interactive Table for Full Dataset ---
st.subheader("📂 Full Dataset (Interactive)")
gb_full = GridOptionsBuilder.from_dataframe(df)
gb_full.configure_default_column(sortable=True, filter=True, resizable=True)
gb_full.configure_grid_options(enableRangeSelection=True)
gridOptions_full = gb_full.build()

AgGrid(
    df,
    gridOptions=gridOptions_full,
    height=400,
    width='100%',
    allow_unsafe_jscode=True,
    theme='dark'
)
