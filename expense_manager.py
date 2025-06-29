import streamlit as st
import csv
from datetime import date, datetime
from collections import defaultdict
import matplotlib.pyplot as plt
from io import BytesIO

# CSV file to store data
DATA_FILE = "expenses.csv"

# Function to load data
def load_data():
    try:
        with open(DATA_FILE, newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []

# Function to save data
def save_data(expenses):
    with open(DATA_FILE, mode='w', newline='') as file:
        fieldnames = ['Date', 'Category', 'Amount', 'Description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

# Title
st.title("Simple Expense Manager")

# Sidebar - Add Expense
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form"):
    expense_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Other"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_entry = {
            "Date": expense_date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": f"{amount:.2f}",
            "Description": description
        }
        data = load_data()
        data.append(new_entry)
        save_data(data)
        st.success("Expense added successfully!")

# Load data again
data = load_data()

# View all expenses
st.subheader("📄 All Expenses")
if data:
    for i, entry in enumerate(data):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"📅 {entry['Date']} | 🏷 {entry['Category']} | ₹{entry['Amount']} | 💬 {entry['Description']}")
        with col2:
            if st.button("❌", key=f"delete_{i}"):
                data.pop(i)
                save_data(data)
                st.rerun()

else:
    st.info("No expenses added yet.")

# Filter by category
st.subheader("🔍 Filter Expenses")
all_categories = list(set(entry["Category"] for entry in data))
category_filter = st.selectbox("Select Category", ["All"] + sorted(all_categories))

if category_filter != "All":
    filtered_data = [e for e in data if e["Category"] == category_filter]
else:
    filtered_data = data

# Show filtered in table
st.write("### Filtered Expenses")
if filtered_data:
    st.table(filtered_data)
else:
    st.info("No data to display.")

# Total expenses
st.subheader("💰 Total Expenses")
total = sum(float(entry["Amount"]) for entry in filtered_data)
st.write(f"Total spent: ₹{total:.2f}")

# Monthly summary
st.subheader("📆 Monthly Expense Summary")
monthly_totals = defaultdict(float)

for entry in data:
    try:
        dt = datetime.strptime(entry["Date"], "%Y-%m-%d")
        month = dt.strftime("%Y-%m")
        monthly_totals[month] += float(entry["Amount"])
    except:
        continue

if monthly_totals:
    months = sorted(monthly_totals.keys())
    values = [monthly_totals[m] for m in months]
    fig, ax = plt.subplots()
    ax.bar(months, values)
    ax.set_title("Monthly Expenses")
    st.pyplot(fig)
else:
    st.info("No monthly data to show.")

# Category-wise pie chart
st.subheader("📊 Category-wise Spending")
category_totals = defaultdict(float)
for entry in data:
    category_totals[entry["Category"]] += float(entry["Amount"])

if category_totals:
    labels = list(category_totals.keys())
    values = list(category_totals.values())
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.set_title("Spending by Category")
    st.pyplot(fig)
else:
    st.info("No category-wise data to show.")