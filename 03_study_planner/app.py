import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="📚 AI Study Planner",
    page_icon="🎓",
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
st.title("📚 AI Study Planner")
st.markdown("""
    <div style='background-color: #4CAF50; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Get a personalized study plan tailored to your goals and available time.
    </div>
""", unsafe_allow_html=True)

st.header("📝 Enter Your Study Details")
subject = st.text_input("Subject/Topic", help="Enter the subject or topic you want to study.")
study_goal = st.text_area("Study Goal", help="Describe your learning objectives and goals.")
available_time = st.number_input("Hours Available Per Week", min_value=1, max_value=100, step=1)
study_resources = st.text_area("Preferred Resources (Optional)", help="Mention any books, websites, or materials you prefer.")

if st.button("📅 Generate Study Plan"):
    with st.spinner("Creating your personalized study schedule..."):
        study_prompt = f"""
        You are an AI study planner. Create a structured study plan for {subject} based on the user's goals, 
        available time per week ({available_time} hours), and preferred resources: {study_resources}.
        """
        
        st.session_state.conversation.append({"role": "system", "content": study_prompt})
        response = call_gpt4o(openai_api_key, study_prompt, st.session_state.conversation)
        st.session_state.conversation.append({"role": "assistant", "content": response})
        
        st.subheader("📅 Your AI-Generated Study Plan")
        st.markdown(response)

st.header("💬 Ask About Your Study Plan")
user_question = st.text_area("Ask a question about your study plan:")
if st.button("Get Answer"):
    if user_question:
        st.session_state.conversation.append({"role": "user", "content": user_question})
        response = call_gpt4o(openai_api_key, "Provide study advice and resources.", st.session_state.conversation)
        st.session_state.conversation.append({"role": "assistant", "content": response})
        
        st.subheader("🤖 AI's Response")
        st.markdown(response)

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered study planning.")