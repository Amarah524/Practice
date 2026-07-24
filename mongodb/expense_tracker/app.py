import streamlit as st 
from db import expenses_collection
from datetime import date
import pandas as pd

st.title("Expense Tracker")
st.header("Add new expense")
# expense_date = st.date_input("Date", date.today())
expense_date = date.today()
st.write("Date:", expense_date)
category = st.selectbox("Category",
                        [
                            "Food",
                            "Travel",
                            "Shopping",
                            "Bills",
                            "Other"
                        ])
description = st.text_input("Description")
amount = st.number_input("Amount")
if st.button("Add expenses"):
    data = {
        "date": str(expense_date),
        "category": category,
        "description": description,
        "amount": amount
    }
    expenses_collection.insert_one(data)
# st.write("Welcome to Expense Tracker")
    st.success("Successfully")

st.header("All expenses")
expenses = list(expenses_collection.find({}, {"_id": 0}))
if expenses:
    df = pd.DataFrame(expenses)
    st.dataframe(df)
    total_expense = df["amount"].sum()
    st.subheader("Total Spending")
    st.success(f"Total Expense: {total_expense}")
else:
    st.info("No expenses found")