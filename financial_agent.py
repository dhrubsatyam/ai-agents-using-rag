"""
Main Financial Agent Implementation
Combines RAG, LLM, and Tools for financial analysis
"""
from typing import List, Dict, Any, Optional, Union
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append('src')

from src.openai_client import OpenAIClient
from src.ollama_client import OllamaClient
from src.vector_store import VectorStoreManager, process_financial_datasets
from src.agent_tools import get_financial_tools
from config import settings

class FinancialRAGAgent:
    """Advanced Financial RAG Agent"""

    def __init__(self, use_openai: bool = True, use_ollama: bool = True, 
                 enable_rag: bool = True, enable_tools: bool = True):
        """Initialize the Financial RAG Agent"""
        self.use_openai = use_openai
        self.use_ollama = use_ollama
        self.enable_rag = enable_rag
        self.enable_tools = enable_tools

        # Initialize LLM clients
        self.openai_client = None
        self.ollama_client = None

        if self.use_openai and settings.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAIClient()
                print("✓ OpenAI client initialized")
            except Exception as e:
                print(f"OpenAI initialization failed: {e}")

        if self.use_ollama:
            try:
                self.ollama_client = OllamaClient()
                print("✓ Ollama client initialized")
            except Exception as e:
                print(f"Ollama initialization failed: {e}")

        # Initialize RAG system
        self.vector_store_manager = None
        self.vector_store = None

        if self.enable_rag:
            self.setup_rag_system()

        # Initialize agent tools
        self.tools = []
        if self.enable_tools:
            self.tools = get_financial_tools()
            print(f"✓ Loaded {len(self.tools)} agent tools")

        # Initialize conversation history
        self.conversation_history: List = []

        # Agent executor
        self.agent_executor = None
        if self.enable_tools and self.openai_client:
            self.setup_agent_executor()

    def setup_rag_system(self):
        """Setup RAG system with vector store"""
        try:
            print("Setting up RAG system...")
            self.vector_store_manager, self.vector_store = process_financial_datasets()
            if self.vector_store:
                print("✓ RAG system ready")
        except Exception as e:
            print(f"RAG setup error: {e}")

    def setup_agent_executor(self):
        """Setup LangChain agent executor"""
        try:
            system_prompt = """
                You are a Senior Financial Analyst AI with access to financial databases and tools.

                ## Your Role:
                - Provide clear, structured financial analysis
                - Use specific data from tools to support your insights
                - Validate data consistency before making conclusions
                - Focus on factual analysis over speculation

                ## Response Structure:
                1. **Data Summary**: Key facts from your tools/database
                2. **Analysis**: What the data indicates
                3. **Context**: Relevant market/industry factors
                4. **Limitations**: Data gaps or uncertainties

                ## Data Validation:
                - Check if company/sector combinations make sense
                - Flag inconsistent or mixed data sources
                - Distinguish between different companies if data seems mixed
                - Always cite specific sources for claims

                ## Guidelines:
                - Use tools for calculations and data retrieval
                - Provide structured, bullet-pointed responses
                - Explain financial metrics clearly
                - Include appropriate disclaimers for investment-related content

                Remember: This is educational analysis only, not investment advice.
                """


            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])

            agent = create_openai_functions_agent(
                llm=self.openai_client.chat_model,
                tools=self.tools,
                prompt=prompt
            )

            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                max_iterations=10,
                return_intermediate_steps=True
            )

            print("✓ Agent executor ready")

        except Exception as e:
            print(f"Agent executor setup error: {e}")

    def retrieve_relevant_context(self, query: str, k: int = 5) -> str:
        """Retrieve relevant context using RAG"""
        if not self.vector_store_manager or not self.vector_store:
            return ""

        try:
            docs = self.vector_store_manager.similarity_search(query, k=k)
            context_parts = []

            for i, doc in enumerate(docs, 1):
                metadata_info = []
                if 'company' in doc.metadata:
                    metadata_info.append(f"Company: {doc.metadata['company']}")
                if 'date' in doc.metadata:
                    metadata_info.append(f"Date: {doc.metadata['date']}")

                metadata_str = " | ".join(metadata_info)
                context_parts.append(f"[{i}] {doc.page_content} ({metadata_str})")

            return "\n\n".join(context_parts)

        except Exception as e:
            print(f"Context retrieval error: {e}")
            return ""

    def get_llm_response(self, prompt: str, use_agent: bool = True) -> str:
        """Get response from LLM"""
        if use_agent and self.agent_executor and self.enable_tools:
            try:
                result = self.agent_executor.invoke({
                    "input": prompt,
                    "chat_history": self.conversation_history[-10:]
                })
                return result.get("output", "No response generated")
            except Exception as e:
                print(f"Agent executor error: {e}")

        # Fallback to direct LLM
        try:
            if self.openai_client:
                return self.openai_client.chat_with_system_prompt(
                    "You are a financial analysis expert.",
                    prompt
                )
            elif self.ollama_client:
                return self.ollama_client.chat_with_system_prompt(
                    "You are a financial analysis expert.",
                    prompt
                )
            else:
                return "No LLM client available"
        except Exception as e:
            return f"LLM error: {str(e)}"

    def analyze_query(self, user_query: str) -> Dict[str, Any]:
        """Main method to analyze financial queries"""
        print(f"\n🔍 Analyzing: {user_query}")

        analysis_result = {
            "query": user_query,
            "context": "",
            "response": "",
            "sources": [],
            "method": "hybrid"
        }

        # Retrieve context
        if self.enable_rag:
            print("🧠 Retrieving relevant context...")
            context = self.retrieve_relevant_context(user_query)
            analysis_result["context"] = context

        # Enhance query with context
        enhanced_query = user_query
        if analysis_result["context"]:
            enhanced_query = f"""
            User Question: {user_query}

            Relevant Context:
            {analysis_result["context"]}

            Please analyze this query using the provided context and your financial expertise.
            """

        # Get LLM response
        print("🤖 Generating analysis...")
        response = self.get_llm_response(enhanced_query)
        analysis_result["response"] = response

        # Update conversation history
        self.conversation_history.append(HumanMessage(content=user_query))
        self.conversation_history.append(AIMessage(content=response))

        return analysis_result

    def get_system_status(self) -> Dict[str, bool]:
        """Get status of all system components"""
        return {
            "openai_available": self.openai_client is not None,
            "ollama_available": self.ollama_client is not None,
            "rag_enabled": self.vector_store is not None,
            "tools_enabled": len(self.tools) > 0,
            "agent_executor_available": self.agent_executor is not None
        }

def create_full_agent() -> FinancialRAGAgent:
    """Create full-featured financial agent"""
    return FinancialRAGAgent(
        use_openai=True,
        use_ollama=True,
        enable_rag=True,
        enable_tools=True
    )

def demo_financial_agent():
    """Demo the financial agent capabilities"""
    print("🚀 Starting Financial RAG Agent Demo...")

    agent = create_full_agent()
    status = agent.get_system_status()
    print(f"\nSystem Status: {status}")

    test_queries = [
        "What is the market sentiment for technology companies?",
        "Calculate the P/E ratio for a stock with price $120 and EPS of $6",
        "Show me recent financial news about TechCorp"
    ]

    for query in test_queries:
        result = agent.analyze_query(query)
        print(f"\nQuery: {result['query']}")
        print(f"Response: {result['response'][:200]}...")

if __name__ == "__main__":
    demo_financial_agent()
