import streamlit as st
import openai
import json
from fpdf import FPDF

# Streamlit App Configuration
st.set_page_config(page_title="AI Parenting Assistant", page_icon="👶", layout="wide")

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

# Function to generate and download PDF
def generate_pdf(content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf_file = "parenting_tips.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Main function
def main():
    st.title("👶 AI Parenting Assistant")
    st.markdown("Get AI-driven parenting tips, educational activities, and solutions to parenting challenges.")

    # Sidebar: API Configuration
    with st.sidebar:
        st.header("🔑 API Configuration")
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        if not openai_api_key:
            st.warning("⚠️ Please enter your OpenAI API Key to proceed")
            return
        st.success("API Key accepted!")
    
    # User Inputs
    st.header("👪 Parenting Assistance")
    age_group = st.selectbox("Select Child's Age Group", ["0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"])
    challenge = st.text_area("Describe your parenting challenge or question")
    
    if st.button("🍼 Get Parenting Advice"):
        with st.spinner("Fetching expert advice..."):
            system_prompt = "You are an AI parenting expert. Provide advice based on age and query."
            user_input = f"Age Group: {age_group}\nParenting Challenge: {challenge}"
            advice = call_gpt4o(openai_api_key, system_prompt, user_input)
            
            if advice:
                st.markdown("### 🏡 Parenting Advice")
                st.write(advice)
                pdf_file = generate_pdf(advice)
                with open(pdf_file, "rb") as file:
                    st.download_button("📥 Download Advice as PDF", file, file_name="parenting_advice.pdf", mime="application/pdf")
            else:
                st.error("No advice received. Try again.")

if __name__ == "__main__":
    main()