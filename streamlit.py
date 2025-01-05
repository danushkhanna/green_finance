import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Sample Data
projects = ['Project A', 'Project B', 'Project C', 'Project D']
esg_scores = [85, 70, 95, 60]  # ESG Scores out of 100
risks = [0.2, 0.5, 0.1, 0.4]  # Risk as a fraction (0 = Low, 1 = High)
min_allocations = [20000, 15000, 25000, 10000]  # Minimum required budget allocations
total_budget = 75000  # Default budgets

# Streamlit App
st.markdown("<h1 style='text-align: center;'>Green Finance Optimiser</h1>",unsafe_allow_html=True)
#st.write("### Visualizing ESG Scores, Budget Allocation, and Risk Analysis")
files=st.file_uploader("Upload File",type=["pdf"])

# Dynamic Budget Slider
budget = st.slider("Adjust Budget", min_value=50000, max_value=100000, step=5000, value=total_budget)
st.write(f"#### Current Budget: ₹{budget:,}")

# Budget Allocation Logic
allocations = np.minimum(min_allocations, (budget / sum(min_allocations)) * np.array(min_allocations))
remaining_budget = budget - sum(allocations)

# DataFrame for Display
data = pd.DataFrame({
    'Project': projects,
    'ESG Score': esg_scores,
    'Risk (Low = Good)': risks,
    'Min Allocation (₹)': min_allocations,
    'Allocated Budget (₹)': allocations
})

# Pie Chart for Budget Allocation
st.write("### Budget Allocation")
fig_pie = px.pie(data, values='Allocated Budget (₹)', names='Project', title="Budget Allocation by Project")
st.plotly_chart(fig_pie)

# Bar Chart for ESG Scores
st.write("### ESG Scores")
fig_bar = px.bar(data, x='Project', y='ESG Score', title="ESG Scores of Projects", color='ESG Score', text='ESG Score')
fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
st.plotly_chart(fig_bar)

# Line Chart for Risk Analysis
st.write("### Risk Analysis")
fig_line = px.line(data, x='Project', y='Risk (Low = Good)', title="Risk Analysis by Project", markers=True)
st.plotly_chart(fig_line)

# Display Table
st.write("### Detailed Project Breakdown")
st.table(data)

# Display Remaining Budget
st.write(f"#### Remaining Budget: ₹{remaining_budget:,}")