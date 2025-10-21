# Demo Guide - Procurement Intelligence Agent 🚀

This guide demonstrates the complete workflow of the Procurement Intelligence Agent with practical examples.

## 🎯 Demo Scenarios

### Scenario 1: Basic Equipment Import Analysis
**Use Case**: Import 500 units of equipment to Bangalore

1. **Access the Application**
   ```
   URL: http://localhost:5000
   ```

2. **Analysis Request**
   ```json
   {
     "quantity": 500,
     "destination": "Bangalore",
     "urgency": "normal"
   }
   ```

3. **System Response**
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
       "status": "Suitable for shipping"
     },
     "delivery_estimate": {
       "days": 10,
       "confidence": "high"
     }
   }
   ```

### Scenario 2: Policy Compliance Check
**Use Case**: Check compliance for medical equipment import

1. **Upload Policy Document**
   ```
   File: medical_equipment_policy.pdf
   Size: < 10MB
   Format: PDF
   ```

2. **Analysis with Policy Check**
   ```json
   {
     "quantity": 200,
     "destination": "Bangalore",
     "category": "medical",
     "policy_check": true
   }
   ```

3. **System Output**
   ```json
   {
     "policy_compliance": {
       "status": "compliant",
       "requirements_met": [
         "Import license verified",
         "Quality certification available",
         "Storage conditions suitable"
       ]
     }
   }
   ```

### Scenario 3: Emergency Procurement
**Use Case**: Urgent medical supplies import

1. **Emergency Request**
   ```json
   {
     "quantity": 1000,
     "destination": "Bangalore",
     "urgency": "high",
     "category": "medical_supplies"
   }
   ```

2. **Expedited Analysis**
   ```json
   {
     "decision": "PROCEED IMMEDIATELY",
     "fast_track_options": {
       "shipping": "express_air",
       "customs": "priority_clearance",
       "estimated_days": 3
     }
   }
   ```

## 🎮 Interactive Examples

### 1. Web Interface Demo

```bash
# Start the application
python main.py

# Access web interface
http://localhost:5000
```

**Steps**:
1. Click "New Analysis"
2. Fill the form:
   - Quantity: 500
   - Destination: Bangalore
   - Category: Equipment
3. Click "Analyze"
4. View real-time analysis results

### 2. Telegram Bot Demo

```
# Start conversation
/start

# Request analysis
/analyze 500 units Bangalore

# Get instant updates
🤖 Analysis in progress...
⏳ Checking currency rates...
🌤️ Analyzing weather...
📊 Generating report...
```

### 3. API Integration Demo

```python
# Python example
import requests

# Setup
base_url = 'http://localhost:5000'
headers = {'Content-Type': 'application/json'}

# Analysis request
data = {
    'quantity': 500,
    'destination': 'Bangalore',
    'urgency': 'normal'
}

# Send request
response = requests.post(f'{base_url}/analyze', json=data)
result = response.json()

print(f"Decision: {result['decision']}")
print(f"Best Currency: {result['currency_analysis']['best_rate']}")
print(f"Delivery Estimate: {result['delivery_estimate']['days']} days")
```

## 📊 Sample Reports

### Currency Analysis Report
```
💱 FOREX RATES (1 Unit → INR)
=============================================
  • JPY: ₹0.58 ⭐ BEST RATE
  • AUD: ₹57.21
  • CAD: ₹62.49
  • USD: ₹88.11
  • EUR: ₹102.36
  • CHF: ₹110.98
  • GBP: ₹117.81 🔴 HIGHEST
=============================================
✅ RECOMMENDATION: Use JPY
   Rate: ₹0.58 per JPY
   Savings: 99.5% vs worst rate (GBP)
```

### Weather Impact Report
```
🌤️ Weather Conditions - Bangalore
=============================================
Temperature: 25.51°C
Humidity: 76%
Wind Speed: 8.49 m/s
Status: ✅ Suitable for shipping
Impact: No expected weather-related delays
=============================================
```

## 🚀 Quick Start Demo

1. **Clone & Setup**
   ```bash
   git clone https://github.com/chandu6777/Procurement-Intelligence-Agent.git
   cd Procurement-Intelligence-Agent
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run**
   ```bash
   python main.py
   ```

4. **Test**
   ```bash
   # Open browser
   http://localhost:5000

   # Try sample analysis
   curl -X POST http://localhost:5000/analyze \
     -H "Content-Type: application/json" \
     -d '{"quantity": 500, "destination": "Bangalore"}'
   ```

## 📱 Mobile Interface Demo

Access the responsive web interface on mobile devices:
1. Open browser on mobile
2. Visit `http://[your-ip]:5000`
3. Use the mobile-optimized interface

## 🎥 Demo Video Guide

For a video walkthrough of the features:
1. Basic Analysis Flow
2. Policy Document Upload
3. Real-time Currency Monitoring
4. Weather Impact Assessment
5. Telegram Bot Integration

Video URL: [Coming Soon]

## 🔍 Testing the Demo

1. **Currency Analysis Test**
   ```bash
   python -m procurement_agent.tests.test_currency
   ```

2. **Weather Analysis Test**
   ```bash
   python -m procurement_agent.tests.test_weather
   ```

3. **Full Integration Test**
   ```bash
   python -m procurement_agent.tests.test_integration
   ```

## 📞 Demo Support

For demo-related questions:
- GitHub Issues: [Create Issue](https://github.com/chandu6777/Procurement-Intelligence-Agent/issues)
- Email: support@example.com
- Telegram: @ProcurementAgentBot