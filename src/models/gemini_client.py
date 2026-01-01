import json
import requests

class GeminiClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        # Gemini Flash 1.5 is fast and supports Lao well
        # Using specific version 001 to avoid resolution errors
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-001:generateContent"

    def check_connection(self):
        if not self.api_key:
            return False
        # Simple validity check usually requires a call. We'll assume True if Key exists for now, 
        # or try a dummy generic call if we want to be strict.
        return True 

    def generate_response(self, context_query):
        if not self.api_key:
            return "Error: Gemini API Key is missing."
            
        headers = {'Content-Type': 'application/json'}
        params = {'key': self.api_key}
        
        # Structure for Gemini API
        payload = {
            "contents": [{
                "parts": [{"text": context_query}]
            }]
        }

        try:
            response = requests.post(self.api_url, headers=headers, params=params, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                try:
                    return data['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError):
                    return "Error parsing Gemini response."
            else:
                return f"Error: Gemini API returned {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error connecting to Gemini: {e}"
