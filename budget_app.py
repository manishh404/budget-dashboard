import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Monthly Budget Dashboard", layout="wide")

st.title("📊 Monthly Budget Dashboard")

# Load Excel
# uploaded_file = st.file_uploader(
 #   "Upload Budget Excel File",
  #   type=["xlsx"],
   #  key="budget_upload"
 #)

 #if uploaded_file is not None:

    # df = pd.read_excel(uploaded_file)''
df = pd.read_excel("monthly_budget.xlsx")

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# KPIs
income = df[df["Type"] == "Income"]["Amount"].sum()
expense = df[df["Type"] == "Expense"]["Amount"].sum()
savings = income - expense
savings_rate = (savings / income) * 100 if income > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Income", f"₹{income:,.0f}")
col2.metric("Total Expense", f"₹{expense:,.0f}")
col3.metric("Net Savings", f"₹{savings:,.0f}")
col4.metric("Savings Rate", f"{savings_rate:.1f}%")

st.divider()

# Expense Breakdown
expense_df = df[df["Type"] == "Expense"]
category_summary = expense_df.groupby("Category")["Amount"].sum().reset_index()

fig1 = px.pie(category_summary, names="Category", values="Amount",
              title="Expense Distribution by Category")

st.plotly_chart(fig1, use_container_width=True)

# Monthly Trend
monthly = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum().reset_index()
monthly["Date"] = monthly["Date"].astype(str)

fig2 = px.bar(monthly, x="Date", y="Amount",
              title="Monthly Cash Flow")

st.plotly_chart(fig2, use_container_width=True)

