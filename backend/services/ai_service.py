from google import genai
from google.genai import types
from backend.config import settings
from typing import Dict, Any, List
import json

class AIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def generate_table_documentation(self, table_name: str, metadata: Dict[str, Any], quality: Dict[str, Any]) -> Dict[str, Any]:
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

        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            return {"documentation": response.text}
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg:
                return {"error": "API Permission Denied. Please enable the 'Generative Language API' in your Google Cloud Console for project 186819853120."}
            return {"error": f"Gemini API Error: {error_msg}"}

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

        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json'
                )
            )
            return json.loads(response.text)
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg:
                return {
                    "error": "API Permission Denied. Please enable the 'Generative Language API' in your Google Cloud Console for project 186819853120.",
                    "sql": "-- API Error",
                    "explanation": "I can't generate the query right now because the Google AI API is not enabled for your account.",
                    "business_interpretation": "To fix this, go to Google Cloud Console and enable the Generative Language API."
                }
            return {"error": f"Gemini API Error: {error_msg}"}



