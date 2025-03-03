import streamlit as st
import openai
from fpdf import FPDF

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

def generate_pdf(summary):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)
    pdf_file = "budget_summary.pdf"
    pdf.output(pdf_file)
    return pdf_file

def main():
    st.set_page_config(page_title="🏡 AI Home Budget Planner", page_icon="💰", layout="wide")
    st.title("🏡 AI Home Budget Planner")
    st.markdown("Easily plan and manage your household budget with AI-powered insights!")
    
    with st.sidebar:
        st.header("🔑 API Configuration")
        openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        if not openai_api_key:
            st.warning("⚠️ Please enter your OpenAI API Key to proceed")
            return
        st.success("API Key accepted!")
    
    st.header("📊 Enter Your Budget Details")
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("Monthly Income ($)", min_value=100.0, step=100.0)
        rent = st.number_input("Rent/Mortgage ($)", min_value=0.0, step=50.0)
        groceries = st.number_input("Groceries ($)", min_value=0.0, step=20.0)
        utilities = st.number_input("Utilities (Electricity, Water, etc.) ($)", min_value=0.0, step=10.0)
    with col2:
        transportation = st.number_input("Transportation ($)", min_value=0.0, step=10.0)
        entertainment = st.number_input("Entertainment ($)", min_value=0.0, step=10.0)
        savings = st.number_input("Savings ($)", min_value=0.0, step=50.0)
        other_expenses = st.number_input("Other Expenses ($)", min_value=0.0, step=10.0)
    
    if st.button("📊 Generate Budget Plan"):
        with st.spinner("Generating your budget plan..."):
            user_profile = f"""
            Income: ${income}/month
            Rent/Mortgage: ${rent}
            Groceries: ${groceries}
            Utilities: ${utilities}
            Transportation: ${transportation}
            Entertainment: ${entertainment}
            Savings: ${savings}
            Other Expenses: ${other_expenses}
            """
            system_prompt = "You are an AI financial planner. Analyze the user's income and expenses, then provide a structured budget plan including recommended changes."
            budget_summary = call_gpt4o(openai_api_key, system_prompt, user_profile)
            
            if "❌ Error" not in budget_summary:
                st.subheader("📜 Budget Summary")
                st.markdown(budget_summary)
                
                pdf_file = generate_pdf(budget_summary)
                with open(pdf_file, "rb") as f:
                    st.download_button("📥 Download Budget Summary as PDF", f, file_name="budget_summary.pdf", mime="application/pdf")
            else:
                st.error(budget_summary)
    
if __name__ == "__main__":
    main()