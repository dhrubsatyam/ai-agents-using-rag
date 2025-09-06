# 🚀 Financial RAG System - Quick Start Guide

## 📋 Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] OpenAI API key (required)
- [ ] Git installed
- [ ] 8GB+ RAM recommended

## ⚡ 3-Minute Quick Start

### Option 1: Local Development (Recommended for beginners)

```bash
# 1. Setup
chmod +x setup.sh
./setup.sh

# 2. Add your OpenAI API key to .env file
echo "OPENAI_API_KEY=your-actual-key-here" > .env

# 3. Test the system
python test_system.py

# 4. Start backend
python fastapi_app.py

# 5. In new terminal, start frontend  
streamlit run streamlit_app.py

# 6. Visit http://localhost:8501
```

### Option 2: Docker (One-command deployment)

```bash
# 1. Set your API key and start
export OPENAI_API_KEY="your-actual-key-here"
cd docker/
docker-compose up --build

# 2. Visit http://localhost:8501
```

## 🧪 Test Your Installation

Try these sample queries in the web interface:

1. **Market Analysis**: "What is the market sentiment for technology companies?"
2. **Financial Calculation**: "Calculate P/E ratio for stock price $150 and EPS $8"  
3. **Company Research**: "Show me recent news about TechCorp"
4. **Economic Data**: "What are the current economic indicators?"

## 🛠️ Troubleshooting

**Backend won't start?**
- Check OpenAI API key in .env
- Ensure port 8000 is available
- Run: `python test_system.py`

**Frontend connection error?**  
- Make sure backend is running first
- Check API_BASE_URL in streamlit_app.py
- Ensure port 8501 is available

**No responses from agent?**
- Verify OpenAI API key is valid
- Check API quota/billing
- Try simpler queries first

**Docker issues?**
- Ensure Docker is running
- Check environment variables
- Try: `docker-compose down && docker-compose up --build`

## 📞 Getting Help

1. **Test System**: Run `python test_system.py` to diagnose issues
2. **Check Logs**: Look at console output for error messages
3. **API Status**: Visit http://localhost:8000/docs for backend status
4. **Reset Database**: Delete `financial_data.db` and restart

## 🎯 Next Steps

After getting the system running:

1. **Explore the UI**: Try different types of financial queries
2. **View API Docs**: Visit http://localhost:8000/docs
3. **Customize Data**: Modify CSV files in `data/` directory
4. **Add Features**: Extend `agent_tools.py` with new capabilities
5. **Deploy**: Use Docker for production deployment

## 💡 Pro Tips

- **Start Simple**: Begin with basic queries before complex analysis
- **Monitor Performance**: Use the system status panel
- **Customize**: Edit `config.py` to adjust system behavior
- **Scale Up**: Add more financial data sources as needed

**Happy Financial Analysis!** 📈🤖
