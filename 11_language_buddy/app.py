import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="🗣️ AI Language Learning Buddy",
    page_icon="🌍",
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
st.title("🗣️ AI Language Learning Buddy")
st.markdown("""
    <div style='background-color: #1E90FF; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Improve your language skills with AI-driven exercises and conversations.
    </div>
""", unsafe_allow_html=True)

# Chat Interface
st.header("💬 Chat with Your AI Language Tutor")
st.session_state.messages = st.session_state.get("messages", [])

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("Thinking..."):
        ai_response = call_gpt4o(openai_api_key, "You are a helpful AI language tutor.", user_input)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered language learning.")