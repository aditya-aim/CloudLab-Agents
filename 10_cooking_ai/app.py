import streamlit as st
import openai

# Streamlit App Configuration
st.set_page_config(
    page_title="🍳 AI Cooking Assistant",
    page_icon="🥘",
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
st.title("🍳 AI Cooking Assistant")
st.markdown("""
    <div style='background-color: #FF6347; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
    Get AI-powered recipe suggestions based on the ingredients you have at home.
    </div>
""", unsafe_allow_html=True)

# User Inputs
st.header("🥕 Enter Available Ingredients")
ingredients = st.text_area("List Your Ingredients", placeholder="E.g., eggs, tomatoes, cheese, chicken...")

if st.button("🍽️ Get Recipe Suggestions"):
    if ingredients.strip():
        with st.spinner("Finding the best recipes for you..."):
            # Get AI-generated recipes
            ai_prompt = f"Suggest recipes based on the following ingredients: {ingredients}"
            ai_response = call_gpt4o(openai_api_key, "You are a chef providing recipe ideas.", ai_prompt)
            
            # Display results
            st.subheader("👨‍🍳 AI-Generated Recipe Suggestions")
            st.markdown(ai_response)
    else:
        st.warning("Please enter at least one ingredient before getting recipes.")

st.write("---")
st.caption("🔹 Developed with Streamlit & GPT-4o for AI-powered cooking assistance.")
