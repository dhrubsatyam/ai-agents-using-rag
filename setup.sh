#!/bin/bash
# Financial RAG System Setup Script

echo "🚀 Setting up Financial RAG System..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Setup environment
echo "⚙️ Setting up environment..."
if [ ! -f .env ]; then
    cp .env.template .env
    echo "📝 Created .env file. Please add your OPENAI_API_KEY!"
else
    echo "📝 .env file already exists"
fi

# Initialize database and vector store
echo "🗄️ Initializing data..."
python -c "
import sys
sys.path.append('src')
from vector_store import process_financial_datasets
try:
    process_financial_datasets()
    print('✅ Data initialization complete')
except Exception as e:
    print(f'⚠️ Data initialization error: {e}')
"

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the system:"
echo "1. Add your OpenAI API key to .env file"
echo "2. Run: python fastapi_app.py (backend)"
echo "3. Run: streamlit run streamlit_app.py (frontend)"
echo ""
echo "🐳 Or use Docker:"
echo "1. export OPENAI_API_KEY='your-key'"
echo "2. cd docker && docker-compose up --build"
