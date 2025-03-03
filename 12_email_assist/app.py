import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="📧 AI Email Composer & Summarizer",
    page_icon="✉️",
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
st.title("📧 AI Email Composer & Summarizer")
st.markdown("""
    <div style='background-color: #1E90FF; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Draft professional emails and summarize long emails into key points.
    </div>
""", unsafe_allow_html=True)

# Email Composition
st.header("✍️ Compose an Email")
email_subject = st.text_input("Subject", placeholder="Enter email subject")
email_body = st.text_area("Body", placeholder="Describe what the email should convey")

tone = st.selectbox("Select Tone", ["Professional", "Friendly", "Concise", "Detailed"])

if st.button("📨 Generate Email"):
    if email_subject.strip() and email_body.strip():
        with st.spinner("Generating email draft..."):
            ai_prompt = f"Compose a {tone} email with subject '{email_subject}' and body details: {email_body}"
            ai_response = call_gpt4o(openai_api_key, "You are an AI email assistant that drafts professional emails.", ai_prompt)
            
            # Display results
            st.subheader("📩 AI-Generated Email")
            st.markdown(ai_response)
    else:
        st.warning("Please enter a subject and email body details.")

# Email Summarization
st.header("📋 Summarize an Email")
long_email = st.text_area("Paste the Email Content Here")

if st.button("🔍 Summarize Email"):
    if long_email.strip():
        with st.spinner("Summarizing email..."):
            summary_prompt = f"Summarize the following email into key points:\n{long_email}"
            summary_response = call_gpt4o(openai_api_key, "You are an AI summarization assistant for emails.", summary_prompt)
            
            # Display results
            st.subheader("📌 Email Summary")
            st.markdown(summary_response)
    else:
        st.warning("Please paste the email content to summarize.")

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered email assistance.")