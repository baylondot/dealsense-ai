from google import genai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Available Gemini Models:\n")

for model in client.models.list():
    # Only show Gemini models
    if "gemini" in model.name.lower():
        print(f"Name: {model.name}")

        # Display supported methods if available
        if hasattr(model, "supported_actions"):
            print(f"Supported Actions: {model.supported_actions}")

        print("-" * 60)