"""
OpenAI LLM Client Implementation
"""
import os
from typing import Optional, List, Dict, Any
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from config import settings

class OpenAIClient:
    """OpenAI client for chat completions and embeddings"""

    def __init__(self, model: str = None, temperature: float = 0.7):
        """Initialize OpenAI client"""
        self.model = model or settings.OPENAI_MODEL
        self.temperature = temperature

        # Validate API key
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        # Initialize chat model
        self.chat_model = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            openai_api_key=settings.OPENAI_API_KEY
        )

        # Initialize embeddings model
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )

    def chat(self, messages: List[BaseMessage]) -> str:
        """Send chat completion request"""
        try:
            response = self.chat_model.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error in OpenAI chat: {e}")
            raise

    def chat_with_system_prompt(self, system_prompt: str, user_message: str) -> str:
        """Chat with system prompt"""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        return self.chat(messages)

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for texts"""
        try:
            return self.embeddings.embed_documents(texts)
        except Exception as e:
            print(f"Error getting embeddings: {e}")
            raise

    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for single text"""
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            print(f"Error getting embedding: {e}")
            raise

def test_openai_client():
    """Test OpenAI client functionality"""
    try:
        client = OpenAIClient()
        response = client.chat_with_system_prompt(
            "You are a financial analyst.",
            "What are the key factors to consider when analyzing a stock?"
        )
        print(f"Chat response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"OpenAI client test failed: {e}")
        return False

if __name__ == "__main__":
    test_openai_client()
