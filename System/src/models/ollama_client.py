import requests

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", model="gemma2:2b"):
        self.base_url = base_url
        self.model = model

    def check_connection(self):
        try:
            requests.get(f"{self.base_url}/api/tags", timeout=2)
            return True
        except:
            return False

    def get_models(self):
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if r.status_code == 200:
                data = r.json()
                # Extract model names (e.g., "gemma:2b")
                return [model["name"] for model in data.get("models", [])]
            return []
        except:
            return []

    def generate_response(self, context_query):
        try:
            payload = {
                "model": self.model,
                "prompt": context_query,
                "stream": False
            }
            r = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=300)
            if r.status_code == 200:
                return r.json().get("response", "")
            return f"Error: Ollama returned status {r.status_code}"
        except Exception as e:
            return f"Error calling Ollama: {e}"
