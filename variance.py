import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Inactive Items Dashboard", layout="wide")

# --- Load Data ---
file_path = "Active and Inactive Items Report.xlsx"  # replace with your actual file name
df = pd.read_excel(file_path)

# --- Clean Columns ---
df.columns = df.columns.str.strip()

# --- Calculations ---
df["Unsold_Value"] = df["Stock"] * df["Cost Price"]

# --- Filter: low sold but high stock ---
df_inactive = df.sort_values(by=["Qty Sold", "Stock"], ascending=[True, False]).head(30)

# --- KPI / Big Insights ---
total_unsold_value = df["Unsold_Value"].sum()
top30_unsold_value = df_inactive["Unsold_Value"].sum()
completely_unsold = df[df["Qty Sold"] == 0].shape[0]

st.title("📊 Inactive Items (September)")

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Unsold Value", f"{total_unsold_value:,.2f}")
col2.metric("📦 Completely Unsold Items", f"{completely_unsold}")
col3.metric("🔥 Unsold Value (Top 30 Low-Sold High-Stock)", f"{top30_unsold_value:,.2f}")

st.markdown("---")

# --- Horizontal Bar Chart ---
fig = px.bar(
    df_inactive,
    x="Stock",
    y="Item Name",
    orientation="h",
    text="Qty Sold",
    title="🚨 Top 30 Low-Selling Items with High Stock",
    color="Unsold_Value",
    color_continuous_scale="Reds",
    hover_data={
        "Stock": True,
        "Qty Sold": True,
        "Cost Price": True,
        "Unsold_Value": True,
        "Item Name": False,  # already shown on y-axis
    }
)

# Layout improvements
fig.update_layout(
    yaxis=dict(title="Item", automargin=True),
    xaxis=dict(title="Stock (Units)"),
    plot_bgcolor="white",
    margin=dict(l=150, r=20, t=60, b=40)
)

fig.update_traces(texttemplate="Sold: %{text}", textposition="outside")

st.plotly_chart(fig, use_container_width=True)

# --- Table for reference ---
st.subheader("📋 Data Table (Top 30 Inactive Items)")
st.dataframe(
    df_inactive[["Item Code", "Item Name", "Stock", "Qty Sold", "Cost Price", "Unsold_Value"]]
)
