import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Inactive Items Dashboard", layout="wide")

# --- Load Data ---
file_path = "Active and Inactive Items Report.xlsx"  # replace with your file name
df = pd.read_excel(file_path)

# --- Clean Columns ---
df.columns = df.columns.str.strip()

# --- Calculations ---
df["Unsold_Value"] = df["Stock"] * df["Cost Price"]

# --- Insights Title ---
st.title("📊 Inactive Items (September)")

# --- Show Key Metrics ---
total_unsold_value = df["Unsold_Value"].sum()
low_selling_items = df[df["Qty Sold"] == 0].shape[0]

st.markdown(f"""
### Key Insights:
- 💰 **Total Value of Unsold Stock:** {total_unsold_value:,.2f}
- 📦 **Completely Unsold Items:** {low_selling_items}
- 🛑 Focus on these items for clearance or better marketing.
""")

# --- Horizontal Bar Chart (Top Low Selling Items) ---
top_low = df.sort_values(by="Qty Sold", ascending=True).head(15)  # 15 lowest sellers

fig = px.bar(
    top_low,
    x="Qty Sold",
    y="Item Name",
    orientation="h",
    text="Qty Sold",
    title="🚨 Lowest Selling Items (September)",
    color="Qty Sold",
    color_continuous_scale="Reds"
)

# Better readability
fig.update_layout(
    yaxis=dict(title="Item", automargin=True),
    xaxis=dict(title="Quantity Sold"),
    plot_bgcolor="white",
    margin=dict(l=120, r=20, t=60, b=40)
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

# --- Show Table for Reference ---
st.subheader("📋 Data Table of Lowest Sellers")
st.dataframe(top_low[["Item Code", "Item Name", "Qty Sold", "Stock", "Unsold_Value"]])
