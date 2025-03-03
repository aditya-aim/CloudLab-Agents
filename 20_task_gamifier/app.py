import streamlit as st
import openai
import random

def call_gpt4o(api_key, prompt):
    """Calls OpenAI GPT-4o API to generate task suggestions."""
    client = openai.Client(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a productivity coach that gamifies tasks."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

def generate_random_rewards():
    rewards = ["🎉 Extra Break Time", "🏆 Productivity Badge", "🍫 Treat Yourself", "📖 Read a Chapter of a Book", "🎮 10 Min Game Time"]
    return random.choice(rewards)

def main():
    st.set_page_config(page_title="🎮 AI Productivity Gamifier", page_icon="🚀", layout="wide")
    st.title("🎮 AI Productivity Gamifier")
    st.markdown("Turn your daily tasks into a fun, gamified experience!")
    
    with st.sidebar:
        st.header("🔑 API Configuration")
        openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        if not openai_api_key:
            st.warning("⚠️ Please enter your OpenAI API Key to proceed")
            return
        st.success("API Key accepted!")
    
    st.header("📝 Gamify Your Tasks")
    task_description = st.text_area("Enter your task:", "Complete a project report")
    difficulty = st.selectbox("Select Difficulty Level:", ["Easy", "Medium", "Hard"])
    
    if st.button("🎯 Generate Gamified Task"):
        with st.spinner("Generating gamified task..."):
            prompt = f"Convert this task into a gamified experience: {task_description}. Difficulty level: {difficulty}."
            response = call_gpt4o(openai_api_key, prompt)
            st.markdown(f"**Gamified Task:** {response}")
            st.success(f"🏅 Reward upon completion: {generate_random_rewards()}")

if __name__ == "__main__":
    main()