import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="📖 AI Story & Novel Writer",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to call GPT-4o API
def call_gpt4o(api_key, system_prompt, user_input):
    """Calls GPT-4o API using OpenAI's client API."""
    client = openai.Client(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
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
st.title("📖 AI Story & Novel Writer")
st.markdown("""
    <div style='background-color: #6A5ACD; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Generate short stories or outline your next novel with AI-powered assistance.
    </div>
""", unsafe_allow_html=True)

# Story/Novel Input
st.header("✍️ Enter Story Details")
st.text_input("Title", key="story_title", help="Enter a title for your story or novel.")
genre = st.selectbox("Select Genre", ["Fantasy", "Science Fiction", "Mystery", "Romance", "Horror", "Historical", "Adventure"], help="Choose a genre for your story.")
user_prompt = st.text_area("Story Idea or Starting Paragraph", height=200, help="Provide an idea or a starting paragraph to guide the AI.")

if st.button("📜 Generate Story"):
    with st.spinner("Crafting your story..."):
        system_prompt = f"You are an AI author. Generate a compelling short story or outline based on the user's title, genre, and input. Ensure it follows a strong narrative structure."
        user_input = f"Title: {st.session_state.story_title}\nGenre: {genre}\nPrompt: {user_prompt}"
        response = call_gpt4o(openai_api_key, system_prompt, user_input)
        
        st.subheader("📖 AI-Generated Story")
        st.markdown(response)

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered story and novel writing.")
