from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def list_models():
    print(f"Checking models for key: {api_key[:10]}...")
    client = genai.Client(api_key=api_key)
    try:
        # Just print the object to see what it has
        models = client.models.list()
        print("\nAvailable Models:")
        for m in models:
            print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {str(e)}")

if __name__ == "__main__":
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
    else:
        list_models()
