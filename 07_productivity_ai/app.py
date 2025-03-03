import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="⏳ AI Productivity Assistant",
    page_icon="📅",
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
st.title("⏳ AI Productivity Assistant")
st.markdown("""
    <div style='background-color: #32CD32; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Get AI-powered daily schedules, task prioritization, and time management strategies to boost productivity.
    </div>
""", unsafe_allow_html=True)

# User Inputs
st.header("📌 Personalize Your Productivity Plan")
primary_goal = st.text_input("Primary Goal for the Day", placeholder="E.g., Finish project report, Study for exams")
available_hours = st.slider("Available Hours", 1, 16, 8)
work_style = st.selectbox("Preferred Work Style", ["Pomodoro Technique", "Deep Work", "Time Blocking", "Flexible Workflow"])
additional_notes = st.text_area("Additional Notes (Optional)", placeholder="Mention any specific tasks or constraints")

if st.button("🚀 Generate Productivity Plan"):
    with st.spinner("Creating your personalized schedule..."):
        productivity_prompt = f"""
        Generate a daily schedule using the {work_style} for a person whose primary goal is {primary_goal}. 
        They have {available_hours} hours available. 
        Additional notes: {additional_notes}.
        """
        response = call_gpt4o(openai_api_key, "You are a productivity coach. Create an efficient schedule.", productivity_prompt)
        
        st.subheader("🗓️ Your AI-Generated Productivity Plan")
        st.markdown(response)

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-driven productivity enhancement.")
