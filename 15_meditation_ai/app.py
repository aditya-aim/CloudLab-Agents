import streamlit as st
import openai
import os
from fpdf import FPDF

# Streamlit App Configuration
st.set_page_config(
    page_title="🧘 AI Meditation & Mindfulness Coach",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to call GPT-4o API
def call_gpt4o(api_key, system_prompt, user_message):
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

# Function to generate a PDF summary
def generate_pdf(meditation_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, meditation_text.encode('latin-1', 'replace').decode('latin-1'))
    pdf_file = "meditation_summary.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

st.title("🧘 AI Meditation & Mindfulness Coach")
st.markdown("""
    <div style='background-color: #6a0dad; padding: 1rem; border-radius: 0.5rem; color: white;'>
    Find peace and mindfulness through AI-guided meditation. Personalize your session and practice mindful breathing with ease.
    </div>
""", unsafe_allow_html=True)

# Sidebar API Configuration
with st.sidebar:
    st.header("🔑 API Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
    if not openai_api_key:
        st.warning("⚠️ Please enter your OpenAI API Key to proceed")
        st.stop()
    st.success("API Key accepted!")

# User Input Section
st.header("🌿 Customize Your Meditation Session")
meditation_type = st.selectbox("Choose Meditation Type", ["Mindfulness", "Body Scan", "Gratitude", "Breathwork", "Sleep Meditation"])
meditation_duration = st.slider("Duration (minutes)", min_value=5, max_value=30, step=5)
mood_before = st.selectbox("How do you feel before meditation?", ["Stressed", "Anxious", "Tired", "Neutral", "Relaxed"])

if st.button("🧘 Start Guided Meditation"):
    with st.spinner("Generating your guided meditation..."):
        user_input = f"Meditation Type: {meditation_type}, Duration: {meditation_duration} min, Mood Before: {mood_before}"
        system_prompt = "You are a meditation coach. Guide the user through a relaxing meditation session."
        meditation_response = call_gpt4o(openai_api_key, system_prompt, user_input)
        
        st.session_state.conversation_history.append(f"**Meditation Session:**\n{meditation_response}")
        st.success("Your meditation guide is ready!")
        st.markdown(meditation_response)

# Conversational UI
st.header("💬 Mindfulness Chat")
user_message = st.text_input("Ask anything about mindfulness and meditation:")
if st.button("Get Advice"):
    if user_message:
        with st.spinner("Finding the best answer for you..."):
            context = "\n".join(st.session_state.conversation_history)
            advice = call_gpt4o(openai_api_key, "You are a mindfulness coach. Answer user questions.", f"{context}\nUser Question: {user_message}")
            st.session_state.conversation_history.append(f"**Q:** {user_message}\n**A:** {advice}")
            st.markdown(f"**Q:** {user_message}")
            st.markdown(f"**A:** {advice}")

# Download PDF option
if st.session_state.conversation_history:
    pdf_file = generate_pdf("\n".join(st.session_state.conversation_history))
    with open(pdf_file, "rb") as file:
        st.download_button(label="📥 Download Meditation Summary", data=file, file_name="meditation_summary.pdf", mime="application/pdf")