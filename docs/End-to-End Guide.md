# End-to-End Guide.md

# Procurement Intelligence Agent - End-to-End Guide 🚀

This guide walks you through the complete setup and usage of the Procurement Intelligence Agent system.

## 📸 Interface Screenshots

### Main Dashboard
![Main Dashboard](/docs/images/img1.png)
*The main interface where users can start new analyses and view results*

### Analysis Form
![Analysis Form](images/analysis-form.png)
*Form for submitting new procurement analysis requests*

### Currency Analysis Results
![Currency Analysis](images/currency-analysis.png)
*Real-time currency analysis and recommendations*

### Weather Impact Assessment
![Weather Report](images/weather-report.png)
*Weather conditions and shipping impact analysis*

### Telegram Bot Integration
![Telegram Bot](images/telegram-bot.png)
*Automated notifications and alerts via Telegram*

### Policy Document Upload
![PDF Upload](images/pdf-upload.png)
*Interface for uploading and analyzing procurement policies*

## Table of Contents
- [Initial Setup](#initial-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Complete Usage Examples](#complete-usage-examples)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Initial Setup

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/chandu6777/Procurement-Intelligence-Agent.git
cd Procurement-Intelligence-Agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Key Configuration
Create `.env` file with your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
LANGCHAIN_API_KEY=your_langchain_key
OPENWEATHER_API_KEY=your_weather_key
```

## Running the Application

### 1. Start the Server
```bash
python main.py
```
The server will start at `http://localhost:5000`

### 2. Verify Setup
- Open browser to `http://localhost:5000`
- Check if the dashboard loads
- Verify Telegram bot connection

## Complete Usage Examples

### Web Interface Workflow

1. **Upload Policy Document**
   ```
   1. Access dashboard at http://localhost:5000
   2. Click "Upload PDF" button
   3. Select procurement policy document
   4. Click Upload
   ```

2. **Submit Analysis Request**
   ```
   1. Fill in the analysis form:
      - Quantity: 500
      - Destination: Bangalore
      - Currency Preference: USD
   2. Click "Analyze"
   ```

3. **View Results**
   You'll receive a comprehensive analysis:
   ```json
   {
     "decision": "PROCEED WITH CONDITIONS",
     "currency_analysis": {
       "best_rate": "JPY at ₹0.58",
       "savings": "99.34% vs USD",
       "recommended_currency": "JPY"
     },
     "weather_impact": {
       "temperature": "25.51°C",
       "humidity": "76%",
       "wind_speed": "8.49 m/s",
       "condition": "suitable for shipping"
     },
     "delivery_estimate": {
       "days": 10,
       "confidence": "high"
     }
   }
   ```

### API Integration

1. **Upload Document Example**
```python
import requests

def upload_policy_doc(file_path):
    url = 'http://localhost:5000/upload_pdf'
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    return response.json()

# Usage
result = upload_policy_doc('procurement_policy.pdf')
```

2. **Analysis Request Example**
```python
def get_procurement_analysis(quantity, location):
    url = 'http://localhost:5000/analyze'
    data = {
        'quantity': quantity,
        'destination': location
    }
    response = requests.post(url, json=data)
    return response.json()

# Usage
analysis = get_procurement_analysis(500, 'Bangalore')
```

### Telegram Bot Usage

1. **Initialize Bot**
```
/start - Begin interaction with bot
```

2. **Request Analysis**
```
/analyze 500 units Bangalore
```

3. **Check Status**
```
/status - Get current analysis status
```

### Sample Workflow

1. **Start Analysis**
```
User: /analyze 500 units Bangalore
Bot: Starting analysis for 500 units to Bangalore...
     Checking currency rates...
     Analyzing weather conditions...
     Reviewing policy compliance...
```

2. **Receive Results**
```
Bot: 🤖 Procurement Alert

Query: Should we proceed with importing 500 units to Bangalore?

DECISION: PROCEED WITH CONDITIONS

Currency Analysis:
- Best Rate: JPY at ₹0.58
- Savings: 99.34% vs USD
- Recommended: Use JPY for payment

Weather Impact:
- Temperature: 25.51°C
- Conditions: Suitable for shipping
- No weather-related delays expected

Delivery Estimate: 10 days
```

## Monitoring and Maintenance

### System Health Checks

1. **View Logs**
```bash
tail -f procurement_agent.log
```

2. **Check API Status**
```bash
python -m procurement_agent.utils.check_apis
```

### Regular Maintenance

1. **Update Exchange Rates**
```bash
python -m procurement_agent.utils.update_rates
```

2. **Backup System**
```bash
python -m procurement_agent.utils.backup
```

### Troubleshooting

1. **API Connection Issues**
```bash
# Check API connectivity
python -m procurement_agent.utils.check_connection

# Test individual APIs
python -m procurement_agent.utils.test_api weather
python -m procurement_agent.utils.test_api currency
```

2. **Database Issues**
```bash
# Verify database
python -m procurement_agent.utils.verify_db

# Reset if needed
python -m procurement_agent.utils.reset_db
```

## Tips and Best Practices

1. **Optimal Usage**
   - Upload clear, legible PDF documents
   - Provide accurate location details
   - Keep system updated with latest rates

2. **Performance Optimization**
   - Regular cache clearing
   - Monitor system resources
   - Update dependencies regularly

3. **Security Best Practices**
   - Regular API key rotation
   - Secure environment variable handling
   - Regular security audits

## Support and Help

For additional support:
- GitHub Issues: Create a new issue
- Email: support@example.com
- Telegram: @ProcurementAgentBot