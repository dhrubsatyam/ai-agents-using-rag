"""
Configuration settings for the Financial RAG System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    
    # LLM Settings
    OPENAI_MODEL: str = "gpt-4"
    OLLAMA_MODEL: str = "llama3.1"
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Vector Database Settings
    VECTOR_DB_TYPE: str = "chroma"
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./financial_data.db"
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Streamlit Settings
    STREAMLIT_HOST: str = "0.0.0.0"
    STREAMLIT_PORT: int = 8501
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_RETRIEVED_DOCS: int = 5
    
    # Guardrails Settings
    ENABLE_GUARDRAILS: bool = True
    MAX_RESPONSE_LENGTH: int = 2000

# Global settings instance
settings = Settings()
