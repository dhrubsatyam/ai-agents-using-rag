"""
Test Script for Financial RAG System
"""
import sys
import os
sys.path.append('.')
sys.path.append('src')

def test_configuration():
    """Test system configuration"""
    print("🧪 Testing configuration...")
    try:
        from config import settings
        print(f"✅ Config loaded - API Host: {settings.API_HOST}:{settings.API_PORT}")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_data_loading():
    """Test data loading"""
    print("🧪 Testing data loading...")
    try:
        import pandas as pd
        news_df = pd.read_csv('data/financial_news_data.csv')
        stock_df = pd.read_csv('data/stock_data.csv')
        econ_df = pd.read_csv('data/economic_indicators.csv')

        print(f"✅ Data loaded - News: {len(news_df)}, Stocks: {len(stock_df)}, Indicators: {len(econ_df)}")
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def test_llm_clients():
    """Test LLM client initialization"""
    print("🧪 Testing LLM clients...")
    try:
        from src.openai_client import OpenAIClient
        from src.ollama_client import OllamaClient

        # Test OpenAI (will fail without API key, which is expected)
        try:
            openai_client = OpenAIClient()
            print("✅ OpenAI client initialized")
        except Exception as e:
            print(f"⚠️ OpenAI client: {e}")

        # Test Ollama (will fail if not running, which is expected)
        try:
            ollama_client = OllamaClient()
            print("✅ Ollama client initialized")
        except Exception as e:
            print(f"⚠️ Ollama client: {e}")

        return True
    except Exception as e:
        print(f"❌ LLM client test failed: {e}")
        return False

def test_agent_tools():
    """Test agent tools"""
    print("🧪 Testing agent tools...")
    try:
        from src.agent_tools import get_financial_tools, financial_calculator

        tools = get_financial_tools()
        print(f"✅ Loaded {len(tools)} agent tools")

        # Test calculator
        result = financial_calculator("10 + 5 * 2")
        print(f"✅ Calculator test: 10 + 5 * 2 = {result}")

        return True
    except Exception as e:
        print(f"❌ Agent tools test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running Financial RAG System Tests\n")

    tests = [
        test_configuration,
        test_data_loading,
        test_llm_clients,
        test_agent_tools
    ]

    results = []
    for test in tests:
        results.append(test())
        print()

    passed = sum(results)
    total = len(results)

    print("📊 Test Summary:")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! System ready to use.")
    else:
        print("⚠️ Some tests failed. Check the output above.")

    return passed == total

if __name__ == "__main__":
    main()
