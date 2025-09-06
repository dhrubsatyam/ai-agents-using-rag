"""
Vector Store Implementation using Chroma and FAISS
"""
import os
import pickle
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np
from langchain_community.vectorstores import Chroma, FAISS
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings

class VectorStoreManager:
    """Manages vector databases for RAG operations"""

    def __init__(self, vector_db_type: str = None, embedding_model: str = None):
        """Initialize vector store manager"""
        self.vector_db_type = vector_db_type or settings.VECTOR_DB_TYPE
        self.embedding_model_name = embedding_model or settings.EMBEDDING_MODEL

        # Initialize embedding model (using open-source model for compatibility)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def create_documents_from_dataframe(self, df: pd.DataFrame, 
                                      text_column: str, 
                                      metadata_columns: List[str] = None) -> List[Document]:
        """Create LangChain documents from DataFrame"""
        documents = []
        metadata_columns = metadata_columns or []

        for idx, row in df.iterrows():
            page_content = str(row[text_column])
            metadata = {"source_row": idx}

            for col in metadata_columns:
                if col in row:
                    metadata[col] = str(row[col])

            documents.append(Document(
                page_content=page_content,
                metadata=metadata
            ))

        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        return self.text_splitter.split_documents(documents)

    def create_chroma_store(self, documents: List[Document], 
                           collection_name: str = "financial_data") -> Chroma:
        """Create and populate Chroma vector store"""
        persist_dir = settings.CHROMA_PERSIST_DIRECTORY
        os.makedirs(persist_dir, exist_ok=True)

        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=collection_name,
            persist_directory=persist_dir
        )

        print(f"Created Chroma store with {len(documents)} documents")
        return vector_store

    def initialize_vector_store(self, documents: List[Document]) -> Any:
        """Initialize vector store based on configuration"""
        if self.vector_db_type.lower() == "chroma":
            self.vector_store = self.create_chroma_store(documents)
        elif self.vector_db_type.lower() == "faiss":
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            raise ValueError(f"Unsupported vector database type: {self.vector_db_type}")

        return self.vector_store

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Perform similarity search"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")

        return self.vector_store.similarity_search(query, k=k)

def process_financial_datasets():
    """Process financial datasets and create vector stores"""
    print("Processing financial datasets for vector storage...")

    vsm = VectorStoreManager()

    # Load financial data
    try:
        news_df = pd.read_csv('data/financial_news_data.csv')
        stock_df = pd.read_csv('data/stock_data.csv')
        economic_df = pd.read_csv('data/economic_indicators.csv')
        print("✓ Loaded financial datasets")
    except FileNotFoundError as e:
        print(f"Error loading datasets: {e}")
        return None, None

    # Create documents
    news_docs = vsm.create_documents_from_dataframe(
        news_df,
        text_column='headline',
        metadata_columns=['date', 'company', 'sector', 'sentiment', 'sentiment_score']
    )

    # Create stock summary documents
    stock_summaries = []
    for company in stock_df['company'].unique():
        company_data = stock_df[stock_df['company'] == company]
        latest_data = company_data.iloc[-1]
        summary = f"{company} stock analysis: Latest closing price ${latest_data['close_price']}, Volume: {latest_data['volume']:,}"
        stock_summaries.append(Document(
            page_content=summary,
            metadata={'type': 'stock_summary', 'company': company}
        ))

    all_documents = news_docs + stock_summaries
    split_docs = vsm.split_documents(all_documents)

    vector_store = vsm.initialize_vector_store(split_docs)
    print("✓ Vector store created successfully")

    return vsm, vector_store

if __name__ == "__main__":
    process_financial_datasets()
