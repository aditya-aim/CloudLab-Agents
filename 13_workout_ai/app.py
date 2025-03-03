import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="🧘 AI Workout & Yoga Instructor",
    page_icon="🏋️",
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
st.title("🧘 AI Workout & Yoga Instructor")
st.markdown("""
    <div style='background-color: #FF4500; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Get personalized workout and yoga plans with step-by-step instructions.
    </div>
""", unsafe_allow_html=True)

# Workout & Yoga Plan Generator
st.header("🏋️ Generate Your Workout/Yoga Plan")

goal = st.selectbox("Select Your Goal", ["Weight Loss", "Muscle Gain", "Flexibility", "General Fitness"])
experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
duration = st.slider("Workout Duration (minutes)", 10, 90, 30)

if st.button("🏆 Generate Plan"):
    if goal and experience:
        with st.spinner("Generating your personalized plan..."):
            ai_prompt = f"Create a {experience} level {goal} workout/yoga plan for {duration} minutes. Include step-by-step instructions."
            ai_response = call_gpt4o(openai_api_key, "You are an AI fitness coach that provides structured workout and yoga plans.", ai_prompt)
            
            # Display results
            st.subheader("📋 Your Workout/Yoga Plan")
            st.markdown(ai_response)
    else:
        st.warning("Please select a goal and experience level.")

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered fitness guidance.")
