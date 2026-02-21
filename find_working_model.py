from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_keys = [k.strip() for k in os.getenv("GEMINI_API_KEYS", "").split(",") if k.strip()]

def find_working_model():
    if not api_keys:
        print("No API keys found.")
        return

    for i, key in enumerate(api_keys):
        print(f"\nTesting Key {i} ({key[:10]}...)")
        client = genai.Client(api_key=key)
        try:
            models = client.models.list()
            for m in models:
                name = m.name
                # Skip models that are clearly not for text generation or are experimental
                if "gemini" not in name.lower():
                    continue
                
                print(f"  Attempting: {name}...", end=" ")
                try:
                    # Clean the name (sometimes it comes as 'models/gemini-...' but SDK might want just 'gemini-...')
                    clean_name = name.replace("models/", "")
                    response = client.models.generate_content(
                        model=clean_name,
                        contents="hi"
                    )
                    print("SUCCESS!")
                    return clean_name
                except Exception as e:
                    print(f"Failed ({str(e)[:50]}...)")
        except Exception as e:
            print(f"  Error listing models: {e}")
    
    return None

if __name__ == "__main__":
    working = find_working_model()
    if working:
        print(f"\nFINAL WORKING MODEL FOUND: {working}")
        with open("working_model.txt", "w") as f:
            f.write(working)
    else:
        print("\nNo working models found for any key.")
