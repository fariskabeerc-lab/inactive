import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Inactive Items Dashboard", layout="wide")

st.title("📊 Inactive Items Insights - September")

# --- Load Data (Replace with your file path) ---
file_path = "Active and Inactive Items Report.xlsx"  # 👈 change to your Excel/CSV file path
if file_path.endswith(".csv"):
    df = pd.read_csv(file_path)
else:
    df = pd.read_excel(file_path)

# Clean columns
df.columns = df.columns.str.strip()

# --- Calculated Fields ---
df["Unsold_Value"] = df["Stock"] * df["Cost Price"]
df["Total_Sales"] = df["Qty Sold"] * df["Sel Price"]

# --- KPIs ---
total_unsold_value = df["Unsold_Value"].sum()
dead_stock_items = df[df["Qty Sold"] == 0].shape[0]
slow_movers = df[(df["Qty Sold"] > 0) & (df["Qty Sold"] < 5)].shape[0]
avg_margin = df["Margin"].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Unsold Value", f"{total_unsold_value:,.2f}")
kpi2.metric("📦 Dead Stock Items", dead_stock_items)
kpi3.metric("🐢 Slow Movers (<5 sold)", slow_movers)
kpi4.metric("📈 Avg Margin %", f"{avg_margin:.2f}")

st.divider()

# --- Key Insights ---
st.subheader("🔑 Key Insights")
insights = []
if dead_stock_items > 0:
    insights.append(f"{dead_stock_items} items had **zero sales** in September → potential dead stock.")
if slow_movers > 0:
    insights.append(f"{slow_movers} items sold less than 5 units → consider clearance or bundle offers.")
if total_unsold_value > 0:
    insights.append(f"Unsold inventory worth **{total_unsold_value:,.2f}** is stuck in stock.")
if avg_margin < 10:
    insights.append("Average margin is very low → pricing review recommended.")
if len(insights) == 0:
    insights.append("No critical issues found. Inventory looks balanced.")

for i in insights:
    st.write("- " + i)

st.divider()

# --- Charts ---
st.subheader("📊 Visual Analysis")

# 1. Stock value distribution
fig1 = px.bar(df.sort_values("Unsold_Value", ascending=False).head(20),
              x="Item Name", y="Unsold_Value",
              title="Top 20 Items with Highest Unsold Value",
              labels={"Unsold_Value": "Unsold Stock Value"})
st.plotly_chart(fig1, use_container_width=True)

# 2. Margin vs Qty Sold
fig2 = px.scatter(df, x="Margin", y="Qty Sold",
                  size="Unsold_Value", color="Sel Price",
                  hover_data=["Item Code", "Item Name"],
                  title="Margin vs Quantity Sold")
st.plotly_chart(fig2, use_container_width=True)

# 3. Dead stock breakdown
dead_stock_df = df[df["Qty Sold"] == 0]
if not dead_stock_df.empty:
    fig3 = px.pie(dead_stock_df, values="Stock", names="Item Name",
                  title="Dead Stock Breakdown")
    st.plotly_chart(fig3, use_container_width=True)
