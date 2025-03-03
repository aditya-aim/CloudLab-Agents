import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="🛠️ AI Code Debugger & Optimizer",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to call GPT-4o API
def call_gpt4o(api_key, system_prompt, user_code):
    """Calls GPT-4o API using OpenAI's client API."""
    client = openai.Client(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_code},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

# Sidebar: API Configuration
with st.sidebar:
    st.header("🔑 API Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
    if not openai_api_key:
        st.warning("⚠️ Please enter your OpenAI API Key to proceed")
        st.stop()
    st.success("API Key accepted!")

# Main UI
st.title("🛠️ AI Code Debugger & Optimizer")
st.markdown("""
    <div style='background-color: #FF8C00; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Paste your Python code below to analyze, debug, and optimize it for better performance.
    </div>
""", unsafe_allow_html=True)

# Code Input
st.header("🐍 Paste Your Python Code")
user_code = st.text_area("Enter Python code here", height=250, help="Paste your Python script for debugging and optimization.")

if st.button("🔍 Analyze & Optimize"):
    with st.spinner("Analyzing and optimizing your code..."):
        system_prompt = "You are an expert Python programmer. Analyze the given code for errors, inefficiencies, and optimizations. Provide a detailed report and an optimized version of the code."
        response = call_gpt4o(openai_api_key, system_prompt, user_code)
        
        st.subheader("📋 Analysis & Optimized Code")
        st.markdown(response)

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered debugging and optimization.")