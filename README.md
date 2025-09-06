# 🚀 Financial RAG System

A comprehensive **Generative AI application** for financial analysis using **Retrieval-Augmented Generation (RAG)**, **LLM agents**, and **financial data**.

## 📊 Business Use Case

**Financial News Sentiment Analysis & Investment Advisory System**

The system analyzes financial news sentiment, company performance, and economic indicators to provide data-driven investment insights through:

- **📰 Financial News Analysis**: 500+ articles with sentiment scoring
- **📈 Stock Performance Tracking**: Multi-company OHLCV data analysis  
- **📉 Economic Indicators**: GDP, inflation, unemployment trends
- **🧠 AI-Powered Insights**: RAG-enhanced LLM analysis
- **🛡️ Safety Guardrails**: Compliant financial advice filtering

## 🏗️ System Architecture

```
User Query → Streamlit UI → FastAPI Backend → Financial Agent
     ↓
RAG System (Vector DB) + Agent Tools (SQL/Search/Calculator) + LLM (OpenAI/Ollama)
     ↓
Guardrails & Safety → Response with Financial Disclaimers
```

## ✅ Implementation Coverage

### 🤖 **LLM → Base Reasoning Engine**
- ✅ **OpenAI GPT-4** integration with API handling
- ✅ **Ollama** local model support with fallback
- ✅ Dual LLM architecture with error handling

### 🧠 **RAG + Vector DB → Document Storage**  
- ✅ **Chroma** vector database for persistent storage
- ✅ **FAISS** alternative for high-performance search
- ✅ **Sentence Transformers** embeddings
- ✅ Financial document chunking and indexing

### ⚡ **Framework → LangChain Orchestration**
- ✅ **LangChain agents** with tool integration
- ✅ Custom prompt templates for financial domain
- ✅ Chain orchestration for multi-step reasoning

### 🛠️ **Agent → Multi-Tool Integration**
- ✅ **SQL Database Tool**: Natural language queries
- ✅ **Web Search Tool**: DuckDuckGo integration  
- ✅ **Calculator Tool**: Financial ratios and calculations
- ✅ **Sentiment Analysis Tool**: Market sentiment scoring

### 🔌 **MCP → External API Integration** 
- ✅ **Model Context Protocol** mock implementation
- ✅ Standardized financial API connection patterns
- ✅ Real-time data integration framework

### 🛡️ **Guardrails + Evaluation → Safety & Compliance**
- ✅ **Input validation** prevents prompt injection
- ✅ **Output filtering** ensures appropriate content
- ✅ **Financial disclaimers** automatically added
- ✅ **Response evaluation** with quality metrics

### 🚀 **Deployment → Production Infrastructure**
- ✅ **FastAPI backend** with comprehensive REST API
- ✅ **Streamlit dashboard** with interactive interface
- ✅ **Docker containerization** with compose orchestration
- ✅ **Health monitoring** and status endpoints

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key
- Docker (optional)

### 1. **Local Development Setup**

```bash
# Clone and setup
git clone <repository-url>
cd financial-rag-system

# Install dependencies  
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env and add your OPENAI_API_KEY

# Start the system
python fastapi_app.py          # Backend (port 8000)
streamlit run streamlit_app.py  # Frontend (port 8501)
```

### 2. **Docker Deployment**

```bash
# Set environment
export OPENAI_API_KEY="your-openai-api-key"

# Start with Docker Compose
cd docker/
docker-compose up --build

# Access applications
# - Frontend: http://localhost:8501
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### 3. **Test the System**

```python
from financial_agent import create_full_agent

# Create agent
agent = create_full_agent()

# Ask financial questions
result = agent.analyze_query("What is the market sentiment for tech companies?")
print(result['response'])
```

## 💡 **Example Queries**

**Market Analysis:**
- "What is the overall market sentiment for technology companies?"
- "Compare recent performance of TechCorp vs FinanceInc"
- "Show me financial news with positive sentiment in the last 30 days"

**Financial Calculations:**
- "Calculate P/E ratio for stock price $150 and EPS $8.50"
- "What is the ROE for net income $5M and equity $25M?"
- "Analyze current ratio with assets $10M and liabilities $4M"

**Economic Insights:**
- "What do current economic indicators suggest about market conditions?"
- "How has inflation affected different market sectors?"
- "Analyze unemployment trends and their market impact"

## 📁 **Project Structure**

```
financial-rag-system/
├── requirements.txt              # Python dependencies
├── config.py                     # System configuration  
├── .env.template                 # Environment variables
├── financial_agent.py            # Main RAG agent
├── fastapi_app.py               # Backend API server
├── streamlit_app.py             # Frontend dashboard
├── data/                        # Financial datasets
│   ├── financial_news_data.csv  # News with sentiment
│   ├── stock_data.csv           # Stock OHLCV data
│   └── economic_indicators.csv  # Economic metrics
├── src/                         # Core modules
│   ├── openai_client.py         # OpenAI integration
│   ├── ollama_client.py         # Ollama integration  
│   ├── vector_store.py          # RAG vector database
│   ├── agent_tools.py           # SQL/Search/Calculator tools
│   └── guardrails.py           # Safety and compliance
├── docker/                      # Deployment
│   ├── Dockerfile              # Container definition
│   ├── docker-compose.yml      # Multi-service setup
│   └── .dockerignore           # Build exclusions
└── docs/                        # Documentation
    └── architecture.png         # System diagram
```

## 🔒 **Safety & Compliance**

- **🛡️ Input Validation**: Prevents malicious prompt injection
- **⚠️ Financial Disclaimers**: Auto-added to investment discussions
- **🚫 Content Filtering**: Blocks inappropriate financial advice  
- **📝 Source Attribution**: All data traced to original sources
- **🔍 Calculation Validation**: Prevents dangerous operations

## 🎯 **Key Features**

- **💬 Interactive Chat**: Natural language financial queries
- **📊 Data Visualization**: Charts and market sentiment analysis
- **🔧 Financial Tools**: Calculators and ratio analysis
- **📈 Real-time Analysis**: Current market data integration
- **🤖 AI Agents**: Automated tool selection and execution
- **🎨 Modern UI**: Professional Streamlit dashboard
- **⚡ Fast API**: High-performance backend with async support

## 🧪 **Testing**

```bash
# Test individual components
python src/openai_client.py
python src/vector_store.py  
python src/agent_tools.py

# Test full system
python financial_agent.py

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/status
```

## ⚠️ **Important Disclaimers**

- **📚 Educational Purpose**: System designed for learning and research
- **🎭 Mock Data**: Uses synthetic data for demonstration  
- **❌ Not Financial Advice**: Outputs are informational only
- **👨‍💼 Professional Consultation**: Always consult qualified advisors
- **📋 Regulatory Compliance**: Ensure compliance with local regulations

## 🔧 **Configuration**

Edit `config.py` to customize:

- **🤖 LLM Models**: Switch between OpenAI/Ollama
- **🗃️ Vector Database**: Choose Chroma vs FAISS  
- **📝 RAG Settings**: Chunk size, overlap, retrieval count
- **🌐 API Settings**: Host, port, CORS configuration
- **🛡️ Guardrails**: Safety thresholds and filters

## 🚀 **Ready to Use!**

This complete implementation provides:

- ✅ **Production-ready code** with error handling
- ✅ **Comprehensive documentation** with examples
- ✅ **Real financial use case** with practical applications
- ✅ **Modern tech stack** following best practices
- ✅ **Scalable architecture** for future enhancements

Start exploring financial AI with this complete RAG system! 🎉

---

**Built for the Financial AI Community** 📈🤖

*For support and updates, check the project repository and documentation.*
