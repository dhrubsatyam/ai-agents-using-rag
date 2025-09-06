"""
Ollama LLM Client Implementation
"""
from typing import Optional, List, Dict, Any
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from config import settings
import requests

class OllamaClient:
    """Ollama client for local LLM inference"""

    def __init__(self, model: str = None, temperature: float = 0.7):
        """Initialize Ollama client"""
        self.model = model or settings.OLLAMA_MODEL
        self.temperature = temperature
        self.base_url = settings.OLLAMA_BASE_URL

        # Check if Ollama is running
        if not self._check_ollama_status():
            print(f"Warning: Ollama server not accessible at {self.base_url}")
            print("Make sure Ollama is running with: ollama serve")

        # Initialize chat model
        try:
            self.chat_model = ChatOllama(
                model=self.model,
                temperature=self.temperature,
                base_url=self.base_url
            )

            # Try to initialize embeddings
            self.embeddings = None
            try:
                self.embeddings = OllamaEmbeddings(
                    model=self.model,
                    base_url=self.base_url
                )
            except Exception as e:
                print(f"Ollama embeddings not available: {e}")

        except Exception as e:
            print(f"Failed to initialize Ollama client: {e}")
            raise

    def _check_ollama_status(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def list_models(self) -> List[str]:
        """List available Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    def chat(self, messages: List[BaseMessage]) -> str:
        """Send chat completion request"""
        try:
            response = self.chat_model.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error in Ollama chat: {e}")
            raise

    def chat_with_system_prompt(self, system_prompt: str, user_message: str) -> str:
        """Chat with system prompt"""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        return self.chat(messages)

def test_ollama_client():
    """Test Ollama client functionality"""
    try:
        client = OllamaClient()
        models = client.list_models()
        print(f"Available models: {models}")

        if not models:
            print("No Ollama models found. Install with: ollama pull llama3.1")
            return False

        response = client.chat_with_system_prompt(
            "You are a financial analyst. Keep responses brief.",
            "What is diversification in investing?"
        )
        print(f"Chat response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"Ollama client test failed: {e}")
        return False

if __name__ == "__main__":
    test_ollama_client()
