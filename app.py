
import streamlit as st
import pandas as pd
import numpy as np

st.title("🎟️ Tour Sales Forecast Tool")

# Inputs
current_sales = st.number_input("Current Ticket Sales", value=3965)
total_capacity = st.number_input("Total Tour Capacity", value=12351)
goal_capacity = st.number_input("Target Capacity (e.g. 90% of total)", value=12351)
weeks_remaining = st.number_input("Weeks Remaining Until Tour", value=28)
cost_per_ticket = st.number_input("Cost per Ticket (GBP)", value=4.25)
budget_remaining = st.number_input("Marketing Budget Remaining (GBP)", value=15000)

# Calculations
tickets_needed = goal_capacity - current_sales
additional_tickets_from_budget = budget_remaining / cost_per_ticket
projected_sales = current_sales + additional_tickets_from_budget
weekly_sales_target = tickets_needed / weeks_remaining
weekly_budget_boost = additional_tickets_from_budget / weeks_remaining

# Create DataFrame
weekly_data = pd.DataFrame({
    "Week": [f"Week {i+1}" for i in range(int(weeks_remaining))],
    "Target Weekly Sales": [weekly_sales_target] * int(weeks_remaining),
    "Sales from Budget": [weekly_budget_boost] * int(weeks_remaining),
    "Projected Total Sales": np.cumsum([weekly_budget_boost] * int(weeks_remaining)) + current_sales
})

# Output
st.metric("🎯 Weekly Ticket Target", f"{weekly_sales_target:.1f}")
st.metric("📈 Weekly Boost from Budget", f"{weekly_budget_boost:.1f}")
st.metric("📊 Projected Final Sales", f"{projected_sales:.0f}")
st.metric("❗ Shortfall / Surplus", f"{projected_sales - goal_capacity:.0f} tickets")

# Chart
st.line_chart(weekly_data.set_index("Week")["Projected Total Sales"])

# Table
st.subheader("📅 Weekly Forecast Table")
st.dataframe(weekly_data)
