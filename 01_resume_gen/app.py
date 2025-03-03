import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="📄 AI Resume & Cover Letter Generator",
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
st.title("📄 AI Resume & Cover Letter Generator")
st.markdown("""
    <div style='background-color: #228B22; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Generate professional resumes and cover letters tailored to your job applications using AI.
    </div>
""", unsafe_allow_html=True)

st.header("📝 Enter Your Details")
col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("Full Name")
    job_title = st.text_input("Job Title")
    experience = st.text_area("Work Experience", help="Describe your past job roles and responsibilities.")

with col2:
    skills = st.text_area("Key Skills", help="List your top skills relevant to the job.")
    education = st.text_area("Education Details", help="Enter your highest degree and institution.")
    achievements = st.text_area("Achievements", help="Highlight any awards, recognitions, or certifications.")

if st.button("📄 Generate Resume & Cover Letter"):
    with st.spinner("Generating your documents..."):
        user_profile = f"""
        Name: {full_name}
        Job Title: {job_title}
        Experience: {experience}
        Skills: {skills}
        Education: {education}
        Achievements: {achievements}
        """
        
        resume_prompt = "You are an AI resume writer. Generate a professional resume based on the user's details."
        resume_text = call_gpt4o(openai_api_key, resume_prompt, user_profile)
        
        cover_letter_prompt = "You are an AI cover letter writer. Generate a personalized cover letter based on the user's details."
        cover_letter_text = call_gpt4o(openai_api_key, cover_letter_prompt, user_profile)
        
        st.subheader("📄 AI-Generated Resume")
        st.markdown(resume_text)
        
        st.subheader("✉️ AI-Generated Cover Letter")
        st.markdown(cover_letter_text)

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered resume generation.")