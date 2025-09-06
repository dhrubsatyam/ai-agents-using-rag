import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

print("🔄 Updating financial data with consistent company profiles...")

# Create consistent company profiles
companies = {
    'TechCorp': {'sector': 'Technology', 'business': 'software and cloud services'},
    'FinanceInc': {'sector': 'Finance', 'business': 'banking and financial services'},  
    'HealthPlus': {'sector': 'Healthcare', 'business': 'medical devices and pharmaceuticals'},
    'EnergyGiant': {'sector': 'Energy', 'business': 'renewable energy and utilities'},
    'RetailMax': {'sector': 'Retail', 'business': 'e-commerce and retail operations'}
}

# Create better news headlines that match companies
news_data = []
for i, (company, profile) in enumerate(companies.items()):
    sector = profile['sector']
    
    if sector == 'Technology':
        headlines = [
            f'{company} reports strong Q3 cloud revenue growth',
            f'{company} announces new AI product launch',
            f'{company} expands data center operations globally',
            f'{company} faces cybersecurity investigation',
            f'{company} partners with major enterprise clients'
        ]
    elif sector == 'Healthcare':
        headlines = [
            f'{company} receives FDA approval for new medical device',
            f'{company} reports positive clinical trial results',
            f'{company} expands pharmaceutical research division',
            f'{company} faces regulatory inquiry on drug pricing',
            f'{company} announces healthcare technology partnership'
        ]
    elif sector == 'Finance':
        headlines = [
            f'{company} reports record quarterly earnings',
            f'{company} expands digital banking services',
            f'{company} increases lending portfolio',
            f'{company} faces regulatory capital requirements',
            f'{company} announces fintech acquisition'
        ]
    elif sector == 'Energy':
        headlines = [
            f'{company} completes major solar farm project',
            f'{company} reports renewable energy growth',
            f'{company} expands wind power operations',
            f'{company} faces environmental compliance review',
            f'{company} announces clean energy investment'
        ]
    else:  # Retail
        headlines = [
            f'{company} reports strong holiday sales',
            f'{company} expands e-commerce platform',
            f'{company} opens new distribution centers',
            f'{company} faces supply chain disruptions',
            f'{company} announces loyalty program enhancement'
        ]
    
    # Generate news for each company
    for j, headline in enumerate(headlines):
        sentiment = ['positive', 'negative', 'neutral'][j % 3]
        sentiment_score = random.uniform(0.6, 0.9) if sentiment == 'positive' else random.uniform(-0.9, -0.6) if sentiment == 'negative' else random.uniform(-0.1, 0.1)
        
        date = datetime.now() - timedelta(days=random.randint(1, 30))
        
        news_data.append({
            'id': len(news_data) + 1,
            'date': date.strftime('%Y-%m-%d'),
            'company': company,
            'sector': sector,
            'headline': headline,
            'sentiment': sentiment,
            'sentiment_score': round(sentiment_score, 3),
            'market_impact': random.choice(['high', 'medium', 'low']),
            'source': random.choice(['Reuters', 'Bloomberg', 'WSJ', 'Financial Times'])
        })

# Save improved data
news_df = pd.DataFrame(news_data)
news_df.to_csv('data/financial_news_data.csv', index=False)
print(f'✅ Updated financial news with {len(news_data)} consistent records')
print('✅ Data updated successfully!')
