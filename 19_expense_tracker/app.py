import streamlit as st
import openai
import pandas as pd

# Streamlit App Configuration
st.set_page_config(
    page_title="🛒 AI Shopping & Expense Tracker",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to call GPT-4o API
def call_gpt4o(api_key, system_prompt, user_message):
    """Calls GPT-4o API using OpenAI's client API."""
    client = openai.Client(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

# Function to analyze expenses
def analyze_expenses(expense_data):
    df = pd.DataFrame(expense_data, columns=["Item", "Category", "Cost ($)"])
    total_spent = df["Cost ($)"].sum()
    category_breakdown = df.groupby("Category")["Cost ($)"].sum().to_dict()
    return total_spent, category_breakdown

# Sidebar: API Configuration
with st.sidebar:
    st.header("🔑 API Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
    if not openai_api_key:
        st.warning("⚠️ Please enter your OpenAI API Key to proceed")
        st.stop()
    st.success("API Key accepted!")

# Main UI
st.title("🛒 AI Shopping & Expense Tracker")
st.markdown("""
    <div style='background-color: #228B22; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Track your shopping expenses, analyze spending patterns, and get budget insights using AI.
    </div>
""", unsafe_allow_html=True)

if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.header("📝 Add Expenses")
col1, col2, col3 = st.columns(3)

with col1:
    item_name = st.text_input("Item Name")
with col2:
    category = st.selectbox("Category", ["Food", "Clothing", "Electronics", "Entertainment", "Utilities", "Other"])
with col3:
    cost = st.number_input("Cost ($)", min_value=0.0, step=0.01)

if st.button("➕ Add Expense"):
    if item_name and cost > 0:
        st.session_state.expenses.append([item_name, category, cost])
        st.success("Expense added!")
    else:
        st.warning("⚠️ Please enter valid expense details.")

if st.session_state.expenses:
    st.header("📊 Expense Overview")
    total_spent, category_breakdown = analyze_expenses(st.session_state.expenses)
    st.write(f"💰 **Total Spent:** ${total_spent:.2f}")
    st.write("📌 **Category Breakdown:**")
    for cat, amount in category_breakdown.items():
        st.write(f"- {cat}: ${amount:.2f}")
    
    # AI Budget Advice
    if st.button("🤖 Get Budget Insights"):
        with st.spinner("Analyzing your spending habits..."):
            user_expense_data = "\n".join([f"{item[0]} ({item[1]}): ${item[2]:.2f}" for item in st.session_state.expenses])
            budget_prompt = "You are a financial assistant. Provide insights on how to improve budgeting based on the following expenses."
            advice = call_gpt4o(openai_api_key, budget_prompt, user_expense_data)
            st.subheader("💡 AI Budgeting Tips")
            st.write(advice)

    # Option to clear expenses
    if st.button("🗑 Clear Expenses"):
        st.session_state.expenses = []
        st.success("All expenses cleared!")

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for intelligent expense tracking.")
