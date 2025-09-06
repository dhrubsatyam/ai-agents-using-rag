"""
Streamlit Frontend for Financial RAG System
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# Configure page
st.set_page_config(
    page_title="Financial RAG System",
    page_icon="📈",
    layout="wide"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1em;
    }
    .status-good { color: #28a745; font-weight: bold; }
    .status-error { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def check_api_status():
    """Check if FastAPI backend is available"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_system_status():
    """Get system status from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def query_financial_agent(query: str):
    """Send query to financial agent"""
    try:
        payload = {"query": query, "use_rag": True, "use_tools": True}

        with st.spinner("🤖 Analyzing your query..."):
            response = requests.post(
                f"{API_BASE_URL}/analyze",
                json=payload,
                timeout=60
            )

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

def main():
    """Main Streamlit application"""

    # Header
    st.markdown('<h1 class="main-header">📈 Financial RAG System</h1>', unsafe_allow_html=True)
    st.markdown("### Advanced Financial Analysis using RAG, LLM, and AI Agents")

    # Check API status
    api_available = check_api_status()

    if not api_available:
        st.error("⚠️ FastAPI backend not available. Start with: python fastapi_app.py")
        st.stop()

    # Sidebar
    st.sidebar.title("🎛️ Control Panel")

    # System Status
    st.sidebar.subheader("System Status")
    status = get_system_status()

    if status:
        st.sidebar.markdown("**OpenAI:** " + 
            f'<span class="status-good">✅ Available</span>' if status.get('openai_available') 
            else '<span class="status-error">❌ Not Available</span>', 
            unsafe_allow_html=True)

        st.sidebar.markdown("**RAG System:** " + 
            f'<span class="status-good">✅ Enabled</span>' if status.get('rag_enabled') 
            else '<span class="status-error">❌ Disabled</span>', 
            unsafe_allow_html=True)

        st.sidebar.markdown("**Agent Tools:** " + 
            f'<span class="status-good">✅ Enabled</span>' if status.get('tools_enabled') 
            else '<span class="status-error">❌ Disabled</span>', 
            unsafe_allow_html=True)

    # Main tabs
    tab1, tab2, tab3 = st.tabs(["💬 Financial Assistant", "📊 Data Dashboard", "🔧 System Info"])

    # Tab 1: Financial Assistant
    with tab1:
        st.header("Financial Analysis Assistant")
        st.write("Ask questions about financial markets, companies, or economic indicators.")

        # Sample queries
        st.subheader("💡 Try these sample queries:")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📈 Market Sentiment"):
                st.session_state.query = "What is the market sentiment for technology companies?"

            if st.button("🧮 P/E Calculation"):
                st.session_state.query = "Calculate P/E ratio for stock price $150 and EPS $8"

        with col2:
            if st.button("📊 Company Analysis"):
                st.session_state.query = "Analyze TechCorp's recent performance"

            if st.button("📰 Financial News"):
                st.session_state.query = "Show recent financial news with positive sentiment"

        # Query input
        query = st.text_area(
            "Enter your financial question:",
            value=st.session_state.get('query', ''),
            height=100,
            placeholder="e.g., What are the key economic indicators?"
        )

        # Query button
        if st.button("🔍 Analyze", type="primary"):
            if query.strip():
                if 'query' in st.session_state:
                    del st.session_state.query

                result = query_financial_agent(query)

                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.success("✅ Analysis Complete")

                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Processing Time", f"{result.get('processing_time_ms', 0):,} ms")
                    with col2:
                        st.metric("Context Used", "Yes" if result.get('context_used') else "No")
                    with col3:
                        st.metric("Timestamp", result.get('timestamp', '').split('T')[1][:8])

                    # Response
                    st.subheader("📋 Analysis Results")
                    st.markdown(result.get('response', 'No response'))

                    # Raw data
                    with st.expander("🔍 View Raw Response Data"):
                        st.json(result)
            else:
                st.warning("Please enter a question.")

    # Tab 2: Data Dashboard
    with tab2:
        st.header("Financial Data Dashboard")

        # Sample visualizations
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Market Sentiment")
            sentiment_data = pd.DataFrame({
                'Sentiment': ['Positive', 'Neutral', 'Negative'],
                'Count': [45, 30, 25]
            })

            fig = px.pie(sentiment_data, values='Count', names='Sentiment', 
                        title="Market Sentiment Distribution")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📊 Sector Performance")
            sector_data = pd.DataFrame({
                'Sector': ['Technology', 'Finance', 'Healthcare', 'Energy'],
                'Performance': [8.2, -2.1, 5.4, -1.8]
            })

            fig = px.bar(sector_data, x='Sector', y='Performance',
                        title="Sector Performance (%)")
            st.plotly_chart(fig, use_container_width=True)

        # Key metrics
        st.subheader("📉 Key Economic Indicators")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            st.metric("GDP Growth", "2.3%", "0.2%")
        with metric_col2:
            st.metric("Inflation Rate", "3.1%", "-0.1%")
        with metric_col3:
            st.metric("Unemployment", "3.6%", "-0.2%")
        with metric_col4:
            st.metric("Interest Rate", "4.25%", "0.25%")

    # Tab 3: System Info
    with tab3:
        st.header("🔧 System Information")

        if st.button("🔄 Refresh System Status"):
            status = get_system_status()
            if status:
                st.json(status)
            else:
                st.error("Could not retrieve system status")

        st.subheader("📚 Available Features")
        features = [
            "✅ **LLM Integration**: OpenAI GPT-4 and Ollama support",
            "✅ **RAG System**: Vector database with financial context",
            "✅ **Agent Tools**: SQL database, web search, calculator",
            "✅ **Safety Guardrails**: Content filtering and validation",
            "✅ **Real-time Analysis**: Interactive financial insights"
        ]

        for feature in features:
            st.markdown(feature)

        st.subheader("🚀 Quick Start Guide")
        st.markdown("""
        1. **Start Backend**: `python fastapi_app.py`
        2. **Launch Dashboard**: `streamlit run streamlit_app.py`
        3. **Ask Questions**: Use the Financial Assistant tab
        4. **View Data**: Explore the Data Dashboard
        5. **Monitor System**: Check this System Info tab
        """)

if __name__ == "__main__":
    main()
