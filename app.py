# 📦 Enhanced Supply Chain Management Dashboard
# Author: AI Assistant

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px  # For interactive plots

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
st.title("📊 Enhanced Supply Chain Management Dashboard")
st.markdown("""
Explore supply chain insights through interactive visualizations. Analyze production, costs, risks, and sustainability factors for data-driven decisions.
""")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter the Data")
product_type = st.sidebar.multiselect("Select Product Type(s):", data['product_type'].unique(), default=data['product_type'].unique())
supplier = st.sidebar.multiselect("Select Supplier(s):", data['supplier_name'].unique(), default=data['supplier_name'].unique())
location = st.sidebar.multiselect("Select Location(s):", data['location'].unique(), default=data['location'].unique())
transport_mode = st.sidebar.multiselect("Select Transportation Mode(s):", data['transportation_modes'].unique(), default=data['transportation_modes'].unique())

filtered_data = data.copy()
if product_type:
    filtered_data = filtered_data[filtered_data['product_type'].isin(product_type)]
if supplier:
    filtered_data = filtered_data[filtered_data['supplier_name'].isin(supplier)]
if location:
    filtered_data = filtered_data[filtered_data['location'].isin(location)]
if transport_mode:
    filtered_data = filtered_data[filtered_data['transportation_modes'].isin(transport_mode)]

# --- KPI Section ---
st.markdown("### 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_data['revenue_generated'].sum()
avg_lead_time = filtered_data['lead_time'].mean()
total_production = filtered_data['production_volumes'].sum()
avg_defect_rate = filtered_data['defect_rates'].mean()

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Avg Lead Time", f"{avg_lead_time:.2f} days")
col3.metric("Total Production Volume", f"{total_production:,.0f}")
col4.metric("Avg Defect Rate", f"{avg_defect_rate:.2f}%")

st.markdown("---")

# --- Insights Section ---
st.subheader("💡 Key Insights Summary")
top_location_revenue = filtered_data.groupby('location')['revenue_generated'].sum().idxmax()
highest_cost_supplier = filtered_data.groupby('supplier_name')['manufacturing_costs'].mean().idxmax()
most_efficient_mode = filtered_data.groupby('transportation_modes')['costs'].mean().idxmin()  # Proxy for sustainability

st.markdown(f"""
✅ **Top Location (by Revenue):** {top_location_revenue}  
✅ **Highest Cost Supplier:** {highest_cost_supplier}  
✅ **Most Efficient Transport Mode (Lowest Cost):** {most_efficient_mode}  
✅ **Risk Insight:** Average defect rate indicates quality risks; focus on suppliers with high rates.  
""")

st.markdown("---")

# --- Tabs for Visualizations ---
tab1, tab2, tab3, tab4 = st.tabs(["📦 Production & Stock", "💰 Revenue & Costs", "🚚 Shipping & Routes", "⚠️ Risks & Sustainability"])

# --- Tab 1: Production & Stock ---
with tab1:
    st.subheader("Production Volumes, Stock Levels, and Lead Times")
    fig1, ax1 = plt.subplots(figsize=(10,6))
    sns.scatterplot(x='production_volumes', y='stock_levels', size='lead_time', hue='product_type', data=filtered_data, palette='coolwarm')
    ax1.set_title("Relationship: Production Volume vs Stock Levels (Size: Lead Time)")
    st.pyplot(fig1)
    
    st.subheader("Relationship Between Production Volume, Stock Levels, and Order Quantities")
    fig2, ax2 = plt.subplots(figsize=(10,6))
    sns.scatterplot(x='production_volumes', y='stock_levels', size='order_quantities', hue='product_type', data=filtered_data, palette='Set1')
    ax2.set_title("Production Volume vs Stock Levels (Size: Order Quantities)")
    st.pyplot(fig2)

# --- Tab 2: Revenue & Costs ---
with tab2:
    st.subheader("Revenue Distribution by Location")
    fig3, ax3 = plt.subplots(figsize=(8,5))
    sns.barplot(x='location', y='revenue_generated', data=filtered_data, estimator=sum, palette='viridis')
    plt.xticks(rotation=45)
    ax3.set_title("Total Revenue by Location")
    st.pyplot(fig3)
    
    st.subheader("Manufacturing Costs by Supplier")
    fig4, ax4 = plt.subplots(figsize=(8,5))
    sns.barplot(x='supplier_name', y='manufacturing_costs', data=filtered_data, estimator='mean', palette='pastel')
    plt.xticks(rotation=45)
    ax4.set_title("Average Manufacturing Costs by Supplier")
    st.pyplot(fig4)
    
    st.subheader("Comparison of Price and Manufacturing Costs by Product Type")
    fig5, ax5 = plt.subplots(figsize=(10,6))
    melted = filtered_data.melt(id_vars='product_type', value_vars=['price', 'manufacturing_costs'], var_name='Cost Type', value_name='Amount')
    sns.boxplot(x='product_type', y='Amount', hue='Cost Type', data=melted, palette='tab10')
    ax5.set_title("Price vs Manufacturing Costs by Product Type")
    st.pyplot(fig5)
    
    st.subheader("Average Lead Time by Product Type")
    fig6, ax6 = plt.subplots(figsize=(8,5))
    sns.barplot(x='product_type', y='lead_time', data=filtered_data, estimator='mean', palette='Blues')
    plt.xticks(rotation=45)
    ax6.set_title("Average Lead Time by Product Type")
    st.pyplot(fig6)

# --- Tab 3: Shipping & Routes ---
with tab3:
    st.subheader("Distribution of Shipping Costs by Shipping Carriers")
    fig7, ax7 = plt.subplots(figsize=(8,5))
    sns.histplot(x='shipping_costs', hue='shipping_carriers', data=filtered_data, multiple='stack', palette='Set2')
    ax7.set_title("Shipping Costs Distribution by Carrier")
    st.pyplot(fig7)
    
    st.subheader("Transportation Routes and Their Frequency")
    route_counts = filtered_data['routes'].value_counts().reset_index()
    route_counts.columns = ['Route', 'Frequency']
    fig8 = px.bar(route_counts, x='Route', y='Frequency', title="Frequency of Transportation Routes", color='Frequency', color_continuous_scale='Reds')
    st.plotly_chart(fig8)

# --- Tab 4: Risks & Sustainability ---
with tab4:
    st.subheader("Supply Chain Risk Distribution by Risk Factors (Defect Rates & Inspection Results)")
    fig9, ax9 = plt.subplots(figsize=(10,6))
    sns.boxplot(x='inspection_results', y='defect_rates', data=filtered_data, palette='coolwarm')
    ax9.set_title("Defect Rates by Inspection Results (Risk Proxy)")
    st.pyplot(fig9)
    
    st.subheader("Sustainability Factors: Cost Efficiency by Transportation Mode")
    fig10, ax10 = plt.subplots(figsize=(8,5))
    sns.barplot(x='transportation_modes', y='costs', data=filtered_data, estimator='mean', palette='Greens')
    ax10.set_title("Average Costs by Transportation Mode (Lower = More Sustainable)")
    st.pyplot(fig10)
    
    # Additional Sustainability Insight: Profit Margin vs Costs
    st.subheader("Sustainability Insight: Profit Margin vs Manufacturing Costs")
    fig11, ax11 = plt.subplots(figsize=(8,5))
    sns.scatterplot(x='manufacturing_costs', y='profit_margin', hue='product_type', data=filtered_data, palette='tab20')
    ax11.set_title("Profit Margin vs Manufacturing Costs (Efficiency Indicator)")
    st.pyplot(fig11)

st.markdown("---")

# --- Download Filtered Data ---
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Filtered Report", data=csv, file_name="supply_chain_filtered_report.csv", mime="text/csv")

# --- Footer ---
st.markdown("---")
st.caption("📍 Created by AI Assistant | Supply Chain Analytics 2025 | Built with Streamlit")
