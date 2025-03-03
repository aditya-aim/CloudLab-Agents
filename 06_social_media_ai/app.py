import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="📱 AI Social Media Post Generator",
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
st.title("📱 AI Social Media Post Generator")
st.markdown("""
    <div style='background-color: #FFD700; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: black;'>
    Generate high-quality social media posts tailored to your platform and audience with AI.
    </div>
""", unsafe_allow_html=True)

# User Inputs
st.header("✍️ Create Your Social Media Post")
platform = st.selectbox("Select Platform", ["Twitter (X)", "Instagram", "Facebook", "LinkedIn", "TikTok"], index=0)
tone = st.selectbox("Select Tone", ["Professional", "Casual", "Inspirational", "Humorous", "Sales-Oriented"])
audience = st.text_input("Target Audience", placeholder="E.g., Small business owners, fitness enthusiasts, tech lovers")
content_topic = st.text_area("What is your post about?", placeholder="Describe your post content here...")

if st.button("📢 Generate Post"):
    with st.spinner("Creating your post..."):
        post_prompt = f"""
        Generate a {tone.lower()} social media post for {platform}. 
        The target audience is {audience}. 
        The post should be about: {content_topic}.
        """
        response = call_gpt4o(openai_api_key, "You are a social media expert. Craft a compelling post.", post_prompt)
        
        st.subheader("🎯 Generated Post")
        st.markdown(response)

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered social media content creation.")