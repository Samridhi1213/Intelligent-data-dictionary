import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")

# Configure Gemini
try:
    client = genai.Client(api_key=api_key)
    
    print("Sending test prompt to Gemini...")
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents="Hello, this is a test from the Intelligent Data Dictionary agent. Say 'System ready!' if you can hear me."
    )
    
    print("\nGemini Response:")
    print(response.text)
    
    if "System ready!" in response.text:
        print("\nVerification successful!")
    else:
        print("\nVerification partially successful (got a response, but it didn't match the expected string).")

except Exception as e:
    print(f"\nError during verification: {str(e)}")
