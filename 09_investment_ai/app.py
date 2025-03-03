import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="📈 AI Investment Portfolio Analyzer",
    page_icon="💰",
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

# Sidebar: API Configuration
with st.sidebar:
    st.header("🔑 API Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
    if not openai_api_key:
        st.warning("⚠️ Please enter your OpenAI API Key to proceed")
        st.stop()
    st.success("API Key accepted!")

# Main UI
st.title("📈 AI Investment Portfolio Analyzer")
st.markdown("""
    <div style='background-color: #228B22; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Optimize your investment strategy with AI-driven insights and risk analysis.
    </div>
""", unsafe_allow_html=True)

# User Inputs
st.header("💰 Enter Your Investment Portfolio Details")
investment_details = st.text_area("Portfolio Composition", placeholder="Describe your current investments, assets, and strategies...")

if st.button("📊 Analyze Portfolio & Get Insights"):
    if investment_details.strip():
        with st.spinner("Analyzing your investment strategy..."):
            # Get AI analysis
            ai_prompt = f"Analyze the following investment portfolio and provide insights: {investment_details}"
            ai_response = call_gpt4o(openai_api_key, "You are an investment advisor providing optimization strategies.", ai_prompt)
            
            # Display results
            st.subheader("🧠 AI-Generated Investment Insights")
            st.markdown(ai_response)
    else:
        st.warning("Please enter your investment portfolio details before analyzing.")

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered investment analysis.")