import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq  # ✅ Correct import
from langchain.schema import HumanMessage

# Load API key from .env
load_dotenv()



# Initialize Groq Chat Model (Using DeepSeek)
chat_model = ChatGroq(
    groq_api_key="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",
        model="deepseek-r1-distill-llama-70b"
 # Use DeepSeek model via Groq
)

# Test the model
response = chat_model([HumanMessage(content="Hello! How are you?")])
print(f"✅ Groq (DeepSeek) Response: {response.content}")
