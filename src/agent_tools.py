"""
Agent Tools Implementation
SQL Database, Web Search, and Calculator tools
"""
import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional
from langchain_core.tools import BaseTool, tool
from langchain_community.tools import DuckDuckGoSearchRun
import math
import re

class FinancialDatabaseTool:
    """Tool for interacting with financial database"""

    def __init__(self, db_path: str = "financial_data.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Set up SQLite database with financial data"""
        conn = sqlite3.connect(self.db_path)

        try:
            # Load CSV data into database
            news_df = pd.read_csv('data/financial_news_data.csv')
            news_df.to_sql('financial_news', conn, if_exists='replace', index=False)

            stock_df = pd.read_csv('data/stock_data.csv')
            stock_df.to_sql('stock_prices', conn, if_exists='replace', index=False)

            econ_df = pd.read_csv('data/economic_indicators.csv')
            econ_df.to_sql('economic_indicators', conn, if_exists='replace', index=False)

            print(f"✓ Database setup complete: {self.db_path}")

        except Exception as e:
            print(f"Error setting up database: {e}")
        finally:
            conn.close()

    def query_database(self, query: str) -> str:
        """Execute SQL query and return results"""
        try:
            conn = sqlite3.connect(self.db_path)
            result = pd.read_sql_query(query, conn)
            conn.close()

            if result.empty:
                return "No results found for the query."

            if len(result) > 10:
                result_str = result.head(10).to_string(index=False)
                result_str += f"\n... (showing first 10 of {len(result)} results)"
            else:
                result_str = result.to_string(index=False)

            return result_str

        except Exception as e:
            return f"Database error: {str(e)}"

@tool
def financial_database_query(query: str) -> str:
    """
    Execute SQL queries on financial database.

    Available tables:
    - financial_news: id, date, company, sector, headline, sentiment, sentiment_score
    - stock_prices: company, date, open_price, high_price, low_price, close_price, volume
    - economic_indicators: date, indicator, value, period
    """
    db_tool = FinancialDatabaseTool()
    return db_tool.query_database(query)

@tool
def web_search(query: str) -> str:
    """Search the web for current financial information."""
    try:
        search = DuckDuckGoSearchRun()
        results = search.run(query)
        return results
    except Exception as e:
        return f"Web search error: {str(e)}"

@tool
def financial_calculator(expression: str) -> str:
    """Perform financial calculations and mathematical operations."""
    try:
        expression = expression.strip()

        # Handle percentage calculations
        if '%' in expression:
            expression = re.sub(r'(\d+(?:\.\d+)?)%\s+of\s+(\d+(?:\.\d+)?)', 
                              r'(\1/100) * \2', expression)
            expression = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', expression)

        # Safety check
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars or c.isalnum() for c in expression.replace('**', '^')):
            return "Error: Invalid characters in expression"

        expression = expression.replace('^', '**')
        result = eval(expression, {"__builtins__": {}, "math": math})

        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            else:
                return f"{result:.4f}".rstrip('0').rstrip('.')
        else:
            return str(result)

    except Exception as e:
        return f"Calculation error: {str(e)}"

@tool
def financial_ratio_calculator(metric_type: str, **kwargs) -> str:
    """
    Calculate common financial ratios.

    Supported metrics: pe_ratio, roe, current_ratio, debt_to_equity, profit_margin
    """
    try:
        if metric_type.lower() == 'pe_ratio':
            price = float(kwargs.get('price', 0))
            eps = float(kwargs.get('earnings_per_share', 0))
            if eps == 0:
                return "P/E Ratio: Cannot calculate (EPS is zero)"
            pe = price / eps
            return f"P/E Ratio: {pe:.2f}"

        elif metric_type.lower() == 'roe':
            net_income = float(kwargs.get('net_income', 0))
            equity = float(kwargs.get('shareholders_equity', 0))
            if equity == 0:
                return "ROE: Cannot calculate (Equity is zero)"
            roe = (net_income / equity) * 100
            return f"ROE: {roe:.2f}%"

        else:
            return f"Unsupported metric type: {metric_type}"

    except Exception as e:
        return f"Calculation error: {str(e)}"

@tool
def get_market_sentiment(company: str = None, sector: str = None, days: int = 30) -> str:
    """Analyze market sentiment from financial news data."""
    try:
        db_tool = FinancialDatabaseTool()

        conditions = []
        if company:
            conditions.append(f"company = '{company}'")
        if sector:
            conditions.append(f"sector = '{sector}'")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        query = f"""
        SELECT sentiment, COUNT(*) as count, AVG(sentiment_score) as avg_score
        FROM financial_news 
        WHERE {where_clause}
        GROUP BY sentiment
        ORDER BY count DESC
        """

        result = db_tool.query_database(query)
        return f"Market sentiment analysis:\n{result}"

    except Exception as e:
        return f"Sentiment analysis error: {str(e)}"

def get_financial_tools():
    """Get list of all financial agent tools"""
    return [
        financial_database_query,
        web_search, 
        financial_calculator,
        financial_ratio_calculator,
        get_market_sentiment
    ]

if __name__ == "__main__":
    # Test tools
    print("Testing financial tools...")
    result = financial_database_query("SELECT COUNT(*) as total_news FROM financial_news")
    print(f"Database test: {result}")

    result = financial_calculator("150 * 1.05")
    print(f"Calculator test: {result}")
