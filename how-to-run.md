🖥️ Complete Setup Guide - Windows & Mac
📋 Prerequisites (Both Platforms)
Required:
Python 3.9+ installed

OpenAI API key (get from: https://platform.openai.com/api-keys)

4GB+ RAM available

Check Python Version:
Windows:
python --version

Mac:
python3 --version

## WINDOWS SETUP
Step 1: Extract and Navigate
text
# Extract the ZIP file to your desired location
# Navigate to the project folder
cd C:\Users\YourName\Downloads\financial-rag-system
Step 2: Install Dependencies
text
# Install required packages
pip install streamlit fastapi uvicorn pandas requests python-dotenv langchain langchain-openai plotly

# If you get permission errors, use:
pip install --user streamlit fastapi uvicorn pandas requests python-dotenv langchain langchain-openai plotly
Step 3: Setup Environment
text
# Copy the environment template
copy .env.template .env

# Edit .env file with Notepad
notepad .env
In the .env file, replace:

OPENAI_API_KEY=your_openai_api_key_here
With your actual API key:

OPENAI_API_KEY=sk-proj-your-actual-api-key-goes-here

Start the System

# Terminal 1 (Backend):

text
cd C:\Users\YourName\Downloads\financial-rag-system
python fastapi_app.py

# Terminal 2 (Frontend) - Open new Command Prompt:

text
cd C:\Users\YourName\Downloads\financial-rag-system  
streamlit run streamlit_app.py
Step 7: Access the System
Frontend Dashboard: http://localhost:8501

Backend API: http://localhost:8000

## 🍎 MAC SETUP

# Install required packages
pip3 install streamlit fastapi uvicorn pandas requests python-dotenv langchain langchain-openai plotly

# If using conda (you have base environment):
conda install -c conda-forge streamlit pandas requests
pip3 install fastapi uvicorn python-dotenv langchain langchain-openai plotly
# Setup Environment
bash

# Update .env file with your api key
OPENAI_API_KEY=your_openai_api_key_here
With your actual API key:

OPENAI_API_KEY=sk-proj-your-actual-api-key-goes-here

# Start the System
# Terminal 1 (Backend):

bash
cd ~/navigate to the project folder/financial-rag-system
python3 fastapi_app.py

# Terminal 2 (Frontend) - Open new terminal:

cd ~/navigate to the project folder/financial-rag-system
streamlit run streamlit_app.py
Step 7: Access the System
Frontend Dashboard: http://localhost:8501

Backend API: http://localhost:8000

##############################################################
✅ Testing (Both Platforms)
Verify Installation:
Windows:

text
python -c "import streamlit; print('✅ Streamlit ready')"
python -c "import fastapi; print('✅ FastAPI ready')" 
python -c "from config import settings; print('✅ Config loaded')"
Mac:

bash
python3 -c "import streamlit; print('✅ Streamlit ready')"
python3 -c "import fastapi; print('✅ FastAPI ready')"
python3 -c "from config import settings; print('✅ Config loaded')"
Test Queries (Both Platforms):
"What companies are in your database?"

"Calculate P/E ratio for stock price $150 and EPS $10"

"Show me recent news for TechCorp"

"What is the sentiment for healthcare companies?"

🛠️ Troubleshooting
Common Issues (Both Platforms):
1. Module Not Found Errors:
Windows:

text
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
Mac:

bash
pip3 install --upgrade pip
pip3 install -r requirements.txt --force-reinstall
2. Port Already in Use:
Windows:

text
netstat -ano | findstr :8000
netstat -ano | findstr :8501
# Kill processes if needed
taskkill /PID <PID_NUMBER> /F
Mac:

bash
lsof -i :8000
lsof -i :8501
# Kill processes if needed
kill -9 <PID_NUMBER>
3. Permission Errors:
Windows: Run Command Prompt as Administrator
Mac: Use sudo or --user flag with pip

4. Python Version Issues:
Windows: Use py -3.9 or py -3.11 instead of python
Mac: Use python3.11 instead of python3 if you have multiple versions

🎯 Success Indicators (Both Platforms)
✅ Backend Terminal Shows:

text
✅ OpenAI client initialized
🚀 Starting Financial RAG API server...
INFO: Uvicorn running on http://0.0.0.0:8000
✅ Frontend Browser Shows:

Green checkmarks for OpenAI and Agent Tools

Interactive chat interface

Sample query buttons working

✅ Queries Return:

Structured responses with bullet points

Accurate calculations

Realistic company-specific news
