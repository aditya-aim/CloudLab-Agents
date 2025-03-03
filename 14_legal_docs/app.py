import streamlit as st
import openai
from fpdf import FPDF
import base64

# Streamlit App Configuration
st.set_page_config(
    page_title="📜 AI Legal Document Assistant",
    page_icon="⚖️",
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

# Function to generate and download PDF
def generate_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))  # Handle Unicode encoding
    pdf_file = "legal_document.pdf"
    pdf.output(pdf_file, "F")
    return pdf_file

def get_pdf_download_link(pdf_file):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="{pdf_file}">📥 Download PDF</a>'
    return href

# Sidebar: API Configuration
with st.sidebar:
    st.header("🔑 API Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
    if not openai_api_key:
        st.warning("⚠️ Please enter your OpenAI API Key to proceed")
        st.stop()
    st.success("API Key accepted!")

# Main UI
st.title("📜 AI Legal Document Assistant")
st.markdown("""
    <div style='background-color: #00008B; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Generate legal contracts, agreements, and summaries with AI assistance.
    </div>
""", unsafe_allow_html=True)

# Legal Document Generator
st.header("⚖️ Generate Your Legal Document")

document_type = st.selectbox("Select Document Type", ["Contract", "Agreement", "Legal Summary"])
details = st.text_area("Enter Key Details", "Include necessary clauses, terms, and any specific information.")

generated_document = ""

if st.button("📄 Generate Document"):
    if document_type and details:
        with st.spinner("Generating your legal document..."):
            ai_prompt = f"Create a {document_type} based on the following details: {details}. Ensure clarity and legal appropriateness."
            generated_document = call_gpt4o(openai_api_key, "You are an AI legal assistant that drafts legal documents professionally.", ai_prompt)
            
            # Display results
            st.subheader("📋 Your Legal Document")
            st.markdown(generated_document)
            
            # Generate PDF and provide download link
            pdf_file = generate_pdf(generated_document)
            st.markdown(get_pdf_download_link(pdf_file), unsafe_allow_html=True)
    else:
        st.warning("Please select a document type and provide details.")

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered legal assistance.")
