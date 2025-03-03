import streamlit as st
import openai
import requests

def call_gpt4o(api_key, prompt):
    """Calls OpenAI DALL·E API to generate an AI image."""
    client = openai.Client(api_key=api_key)
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url
    except Exception as e:
        return f"❌ Error: {e}"

def main():
    st.set_page_config(page_title="🎨 AI Digital Art Generator", page_icon="🎭", layout="wide")
    st.title("🎨 AI Digital Art Generator")
    st.markdown("Generate stunning AI-powered artwork based on your imagination!")

    with st.sidebar:
        st.header("🔑 API Configuration")
        openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        if not openai_api_key:
            st.warning("⚠️ Please enter your OpenAI API Key to proceed")
            return
        st.success("API Key accepted!")

    st.header("🖌️ Create Your AI Artwork")
    prompt = st.text_area("Describe your artwork idea:", "A futuristic city skyline at sunset with flying cars")
    if st.button("🎨 Generate Art"):
        with st.spinner("Generating your AI artwork..."):
            image_url = call_gpt4o(openai_api_key, prompt)
            if image_url.startswith("http"):
                st.image(image_url, caption="Generated Artwork")
                
                # Download Button
                img_data = requests.get(image_url).content
                st.download_button(label="📥 Download Image", data=img_data, file_name="ai_generated_art.png", mime="image/png")
            else:
                st.error(image_url)

if __name__ == "__main__":
    main()