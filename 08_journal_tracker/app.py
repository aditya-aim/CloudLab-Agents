import streamlit as st
import openai
from textblob import TextBlob

# Streamlit App Configuration
st.set_page_config(
    page_title="📖 AI Personal Journal & Mood Tracker",
    page_icon="📝",
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
st.title("📖 AI Personal Journal & Mood Tracker")
st.markdown("""
    <div style='background-color: #FFD700; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: black;'>
    Reflect on your daily experiences and track your mood with AI-powered insights.
    </div>
""", unsafe_allow_html=True)

# User Inputs
st.header("✍️ Write Your Daily Journal Entry")
journal_entry = st.text_area("How was your day?", placeholder="Write about your experiences, thoughts, and emotions...")

if st.button("📊 Analyze Mood & Get AI Insights"):
    if journal_entry.strip():
        with st.spinner("Analyzing your mood and generating insights..."):
            # Perform sentiment analysis
            sentiment = TextBlob(journal_entry).sentiment.polarity
            mood = "😊 Positive" if sentiment > 0.2 else "😐 Neutral" if sentiment >= -0.2 else "😞 Negative"
            
            # Get AI insights
            ai_prompt = f"Provide reflective insights and journaling prompts based on this journal entry: {journal_entry}"
            ai_response = call_gpt4o(openai_api_key, "You are a personal journaling assistant providing insights.", ai_prompt)
            
            # Display results
            st.subheader("🧠 AI-Generated Insights")
            st.markdown(ai_response)
            
            st.subheader("💡 Mood Analysis")
            st.markdown(f"**Detected Mood:** {mood}")
    else:
        st.warning("Please write a journal entry before analyzing.")

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered journaling and mood tracking.")