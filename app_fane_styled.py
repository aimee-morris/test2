
import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title="Tour Sales Forecast", layout="wide")

# Apply custom styles
st.markdown("""
    <style>
        body {
            background-color: #F2F2F2;
        }
        .main {
            background-color: #F2F2F2;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stApp {
            font-family: 'sans-serif';
        }
        .metric-label, .metric-container {
            color: #0F2744 !important;
        }
        .big-metric {
            font-size: 28px !important;
            color: #ED145B !important;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 style="color: white; background-color: #0F2744; padding: 1rem; border-radius: 8px;">🎟️ Tour Sales Forecast Tool</h1>', unsafe_allow_html=True)

# Inputs
with st.sidebar:
    st.header("📥 Input Your Data")
    current_sales = st.number_input("Current Ticket Sales", value=3965)
    total_capacity = st.number_input("Total Tour Capacity", value=12351)
    goal_capacity = st.number_input("Target Capacity", value=12351)
    weeks_remaining = st.number_input("Weeks Remaining Until Tour", value=28)
    cost_per_ticket = st.number_input("Cost per Ticket (GBP)", value=4.25)
    budget_remaining = st.number_input("Marketing Budget Remaining (GBP)", value=15000)

# Calculations
tickets_needed = goal_capacity - current_sales
additional_tickets_from_budget = budget_remaining / cost_per_ticket
projected_sales = current_sales + additional_tickets_from_budget
weekly_sales_target = tickets_needed / weeks_remaining
weekly_budget_boost = additional_tickets_from_budget / weeks_remaining

# Weekly Data
weekly_data = pd.DataFrame({
    "Week": [f"Week {i+1}" for i in range(int(weeks_remaining))],
    "Target Weekly Sales": [weekly_sales_target] * int(weeks_remaining),
    "Sales from Budget": [weekly_budget_boost] * int(weeks_remaining),
    "Projected Total Sales": np.cumsum([weekly_budget_boost] * int(weeks_remaining)) + current_sales
})

# Display metrics
st.markdown("### 📊 Forecast Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🎯 Weekly Ticket Target", f"{weekly_sales_target:.1f}")
col2.metric("📈 Weekly Boost from Budget", f"{weekly_budget_boost:.1f}")
col3.metric("📊 Projected Final Sales", f"{projected_sales:.0f}")
col4.metric("❗ Shortfall / Surplus", f"{projected_sales - goal_capacity:.0f} tickets")

# Chart
st.markdown("### 📈 Projected Ticket Sales")
st.line_chart(weekly_data.set_index("Week")["Projected Total Sales"])

# Table
st.markdown("### 📅 Weekly Forecast Table")
st.dataframe(weekly_data)
