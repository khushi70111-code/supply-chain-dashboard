# 📦 Supply Chain Management Dashboard (Enhanced)
# Author: Your Name

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="Supply Chain Management Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    data = pd.read_csv("cleaned_supply_chain1.csv")
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')
    return data

data = load_data()

# --- Title and Intro ---
st.title("📊 Supply Chain Management Dashboard")
st.markdown("""
Analyze and visualize supply chain data to uncover key insights on product performance, 
supplier efficiency, costs, and operational bottlenecks.
""")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter the Data")
product_type = st.sidebar.multiselect("Select Product Type(s):", data['product_type'].unique())
supplier = st.sidebar.multiselect("Select Supplier(s):", data['supplier_name'].unique())

filtered_data = data.copy()
if product_type:
    filtered_data = filtered_data[filtered_data['product_type'].isin(product_type)]
if supplier:
    filtered_data = filtered_data[filtered_data['supplier_name'].isin(supplier)]

# --- KPI Section ---
st.markdown("### 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_data['revenue_generated'].sum()
total_units = filtered_data['number_of_products_sold'].sum()
avg_lead_time = filtered_data['lead_time'].mean()
avg_defect_rate = filtered_data['defect_rates'].mean()

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Units Sold", f"{total_units:,.0f}")
col3.metric("Avg Lead Time", f"{avg_lead_time:.2f} days")
col4.metric("Avg Defect Rate", f"{avg_defect_rate:.2f}%")

st.markdown("---")

# --- Insights Section ---
st.subheader("💡 Key Insights Summary")

top_product = filtered_data.groupby('product_type')['revenue_generated'].sum().idxmax()
top_supplier = filtered_data.groupby('supplier_name')['revenue_generated'].sum().idxmax()
fastest_supplier = filtered_data.groupby('supplier_name')['lead_time'].mean().idxmin()
lowest_defect_supplier = filtered_data.groupby('supplier_name')['defect_rates'].mean().idxmin()

st.markdown(f"""
✅ **Top Product Type (by Revenue):** {top_product}  
✅ **Top Supplier (by Revenue):** {top_supplier}  
✅ **Fastest Supplier (Lowest Lead Time):** {fastest_supplier}  
✅ **Most Reliable Supplier (Lowest Defect Rate):** {lowest_defect_supplier}  
""")

st.markdown("---")

# --- Layout for Charts ---
tab1, tab2, tab3 = st.tabs(["📦 Product Performance", "🚚 Supplier Insights", "💰 Cost & Quality"])

# --- Tab 1: Product Performance ---
with tab1:
    st.subheader("Revenue by Product Type")
    fig1, ax1 = plt.subplots(figsize=(8,5))
    sns.barplot(x='product_type', y='revenue_generated', data=filtered_data, estimator=sum, palette='cool')
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    st.subheader("Sales vs Stock Levels")
    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.scatterplot(x='stock_levels', y='number_of_products_sold', hue='product_type', data=filtered_data, palette='Set2')
    st.pyplot(fig2)

# --- Tab 2: Supplier Insights ---
with tab2:
    st.subheader("Average Lead Time by Supplier")
    fig3, ax3 = plt.subplots(figsize=(8,5))
    sns.barplot(x='supplier_name', y='lead_time', data=filtered_data, estimator='mean', palette='viridis')
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    st.subheader("Defect Rate by Supplier")
    fig4, ax4 = plt.subplots(figsize=(8,5))
    sns.barplot(x='supplier_name', y='defect_rates', data=filtered_data, estimator='mean', palette='pastel')
    plt.xticks(rotation=45)
    st.pyplot(fig4)

# --- Tab 3: Cost & Quality ---
with tab3:
    st.subheader("Average Shipping Cost by Transportation Mode")
    fig5, ax5 = plt.subplots(figsize=(6,4))
    sns.barplot(x='transportation_modes', y='costs', data=filtered_data, estimator='mean', palette='Blues')
    st.pyplot(fig5)

    st.subheader("Manufacturing Cost vs Price")
    fig6, ax6 = plt.subplots(figsize=(6,4))
    sns.scatterplot(x='manufacturing_costs', y='price', hue='product_type', data=filtered_data, palette='tab10')
    st.pyplot(fig6)

st.markdown("---")

# --- Download Filtered Data ---
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Filtered Report", data=csv, file_name="supply_chain_filtered_report.csv", mime="text/csv")

# --- Footer ---
st.markdown("---")
st.caption("📍 Created by [Khushi Pandey] | Data Analytics Project 2025 | Built with Streamlit")
