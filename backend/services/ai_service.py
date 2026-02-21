from google import genai
from google.genai import types
from backend.config import settings
from typing import Dict, Any, List
import json

class AIService:
    def __init__(self):
        self.api_keys = [k.strip() for k in settings.GEMINI_API_KEYS.split(",") if k.strip()]
        self.current_key_index = 0
        self._clients = []
        self._doc_cache = {} # Simple in-memory cache for documentation
        self._initialize_clients()

    def _initialize_clients(self):
        for key in self.api_keys:
            try:
                self._clients.append(genai.Client(api_key=key))
            except Exception as e:
                print(f"Error initializing Gemini client with key {key[:10]}...: {e}")

    @property
    def client(self):
        if not self._clients:
            return None
        return self._clients[self.current_key_index]

    def rotate_key(self):
        if len(self._clients) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self._clients)
            print(f"Rotating to Gemini API key index: {self.current_key_index}")
            return True
        return False

    def generate_table_documentation(self, table_name: str, metadata: Dict[str, Any], quality: Dict[str, Any]) -> Dict[str, Any]:
        # Check cache first
        if table_name in self._doc_cache:
            return {"documentation": self._doc_cache[table_name], "cached": True}

        if not self.client:
            return {"error": "Gemini API Key not configured or client failed to initialize"}

        prompt = f"""
        Generate business-friendly documentation for the database table '{table_name}'.
        
        Metadata: {metadata}
        Data Quality Metrics: {quality}
        
        Please provide:
        1. A high-level business description of the table.
        2. Column-level explanations.
        3. Usage recommendations for BI/Analytics.
        4. Risk insights based on quality metrics (e.g., high null percentage).
        5. Suggested business analysis use cases.
        
        Format the response as clear Markdown text.
        """

        for attempt in range(len(self._clients)):
            models_to_try = [
                'gemini-2.5-flash',
                'gemini-2.0-flash', 
                'gemini-1.5-flash', 
                'gemini-1.5-flash-8b', 
                'gemini-1.0-pro'
            ]
            last_error = ""

            for model_name in models_to_try:
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    self._doc_cache[table_name] = response.text
                    return {"documentation": response.text, "model_used": model_name, "key_index": self.current_key_index}
                except Exception as e:
                    last_error = str(e)
                    if "429" in last_error or "RESOURCE_EXHAUSTED" in last_error:
                        # Rate limit hit, try rotating if we have more keys
                        if self.rotate_key():
                            break # Break model loop to retry with new key
                        else:
                            return {
                                "error": "API Rate Limit Exceeded on all available keys. Please wait 60 seconds.",
                                "details": last_error
                            }
                    continue # Try next model
            else:
                # If we broke out of model loop because of a rotation, the for-else won't execute.
                # If we finished model loop normally and failed, we return error.
                if "429" not in last_error and "RESOURCE_EXHAUSTED" not in last_error:
                    error_msg = last_error
                    if "403" in error_msg:
                        return {"error": "API Permission Denied. Please enable the 'Generative Language API' or 'Vertex AI API'."}
                    return {"error": f"Gemini API Error: {error_msg}"}
                continue # Retry outer loop if we rotated
        
        return {"error": "Failed after trying all API keys."}

    def generate_sql_from_question(self, question: str, schema_context: str) -> Dict[str, Any]:
        if not self.client:
            return {"error": "Gemini API Key not configured or client failed to initialize"}

        prompt = f"""
        You are a SQL expert. Based on the following database schema:
        {schema_context}
        
        User Question: "{question}"
        
        Generate a PostgreSQL compatible SQL query to answer this question.
        Also provide a brief business interpretation of what the query calculates.
        
        Response format (JSON):
        {{
            "sql": "SELECT ...",
            "explanation": "This query calculates...",
            "business_interpretation": "A higher value means..."
        }}
        """

        for attempt in range(len(self._clients)):
            models_to_try = [
                'gemini-2.5-flash',
                'gemini-2.0-flash', 
                'gemini-1.5-flash', 
                'gemini-1.5-flash-8b', 
                'gemini-1.0-pro'
            ]
            last_error = ""

            for model_name in models_to_try:
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type='application/json'
                        )
                    )
                    return json.loads(response.text)
                except Exception as e:
                    last_error = str(e)
                    if "429" in last_error or "RESOURCE_EXHAUSTED" in last_error:
                        if self.rotate_key():
                            break
                        else:
                            return {
                                "error": "API Rate Limit Exceeded.",
                                "sql": "-- Rate Limit",
                                "explanation": "Gemini API rate limit reached on all keys.",
                                "business_interpretation": "Wait 60 seconds."
                            }
                    continue
            else:
                if "429" not in last_error and "RESOURCE_EXHAUSTED" not in last_error:
                    error_msg = last_error
                    if "403" in error_msg:
                        return {
                            "error": "API Permission Denied. Enable 'Generative Language API' or 'Vertex AI API'.",
                            "sql": "-- API Error",
                            "explanation": "Google AI API is not enabled for your account.",
                            "business_interpretation": "Fix this in your Google console."
                        }
                    return {"error": f"Gemini API Error: {error_msg}"}
                continue

        return {"error": "Failed after trying all API keys."}



