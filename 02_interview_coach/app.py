import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="🎤 AI Interview Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to call GPT-4o API
def call_gpt4o(api_key, system_prompt, conversation_history):
    """Calls GPT-4o API using OpenAI's client API."""
    client = openai.Client(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation_history
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

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Main UI
st.title("🎤 AI Interview Coach")
st.markdown("""
    <div style='background-color: #1E90FF; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Practice mock interviews and receive AI-driven feedback to improve your responses.
    </div>
""", unsafe_allow_html=True)

st.header("📝 Enter Your Job Role & Details")
job_role = st.text_input("Job Role", help="Enter the job role you are preparing for.")
custom_question = st.text_area("Custom Interview Question (Optional)", help="Enter a specific question you want feedback on.")

if st.button("🎤 Start Mock Interview"):
    with st.spinner("Generating mock interview questions and feedback..."):
        interview_prompt = f"You are an AI interview coach. Conduct a mock interview for a {job_role} role. Ask relevant questions and provide feedback on ideal responses."
        if custom_question:
            interview_prompt += f"\nInclude this custom question: {custom_question}"
        
        # Maintain conversation history
        st.session_state.conversation.append({"role": "system", "content": interview_prompt})
        response = call_gpt4o(openai_api_key, interview_prompt, st.session_state.conversation)
        st.session_state.conversation.append({"role": "assistant", "content": response})
        
        st.subheader("🎤 AI-Generated Mock Interview")
        st.markdown(response)

st.header("💬 Continue the Conversation")
user_response = st.text_area("Your Response", help="Type your response to the interview question here.")
if st.button("Submit Response"):
    if user_response:
        st.session_state.conversation.append({"role": "user", "content": user_response})
        response = call_gpt4o(openai_api_key, "Continue the interview conversation and provide feedback.", st.session_state.conversation)
        st.session_state.conversation.append({"role": "assistant", "content": response})
        
        st.subheader("🤖 AI's Feedback")
        st.markdown(response)

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered interview coaching.")