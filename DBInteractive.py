import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset
file_path = "C:\\Test BankersLab\\Simulation results\\TabularResults (2).xlsx"
xls = pd.ExcelFile(file_path)

# Select a sheet to work with
sheet_name = "Emerging - Unsecured"
df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=7)

# Extract relevant columns
df = df.dropna(how='all', axis=1)  # Remove empty columns
df.columns = ["Category", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]
df = df.dropna(subset=["Category"])  # Remove empty rows
df.set_index("Category", inplace=True)

# Streamlit UI
st.title("Interactive Financial Model")

# Sidebar Inputs
marketing = st.slider("Marketing (Applications)", min_value=100000, max_value=500000, value=300000, step=5000)
interest_rate = st.slider("Interest Rate (%)", min_value=5, max_value=30, value=25, step=1)
low_side = st.slider("Low-Side Overrides", min_value=0, max_value=5, value=1, step=1)
credit_line = st.number_input("Credit Line ($)", min_value=1000, max_value=50000, value=10000, step=500)
months_income = st.slider("Months of Income Considered", min_value=1, max_value=12, value=6, step=1)

# Ensure the function applies user inputs correctly
def calculate_financials():
    """
    Simulate financial impacts based on user inputs.
    The financial results should change dynamically.
    """
    adjusted_df = df.copy()

    # Apply changes based on user inputs
    if "Applications" in adjusted_df.index:
        adjusted_df.loc["Applications"] *= (marketing / 300000)  # Scale applications

    if "Interest Revenue" in adjusted_df.index:
        adjusted_df.loc["Interest Revenue"] *= (interest_rate / 25)  # Adjust revenue based on interest rate
    
    if "Net Income" in adjusted_df.index:
        adjusted_df.loc["Net Income"] *= ((interest_rate / 25) + (marketing / 300000) - (low_side / 5))

    if "Loans Booked" in adjusted_df.index:
        adjusted_df.loc["Loans Booked"] *= ((marketing / 300000) + (credit_line / 10000))

    if "Cumulative Net Income" in adjusted_df.index:
        adjusted_df.loc["Cumulative Net Income"] = adjusted_df.loc["Net Income"].cumsum()

    # Additional adjustments based on months_income
    if "Fee Revenue" in adjusted_df.index:
        adjusted_df.loc["Fee Revenue"] *= (months_income / 6)

    if "Interest Expense" in adjusted_df.index:
        adjusted_df.loc["Interest Expense"] *= (months_income / 6)

    if "Net Interest Revenue" in adjusted_df.index:
        adjusted_df.loc["Net Interest Revenue"] = adjusted_df.loc["Interest Revenue"] - adjusted_df.loc["Interest Expense"]

    return adjusted_df.loc[
        ["Applications", "Loans Booked", "Interest Revenue", "Fee Revenue", "Interest Expense", "Net Interest Revenue", "Net Income", "Cumulative Net Income"]
    ]

# Display updated results
st.write("### Financial Impact")
updated_results = calculate_financials()
st.dataframe(updated_results)