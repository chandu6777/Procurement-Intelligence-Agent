# Procurement Intelligence Agent 🤖

An intelligent procurement assistant that helps analyze and make decisions about equipment imports using real-time data, weather conditions, and currency exchange rates.

## 🌟 Features

- **Real-time Currency Analysis**: Compares multiple currency exchange rates (USD, EUR, GBP, JPY, etc.) to find the best rates against INR
- **Weather Impact Assessment**: Checks weather conditions at destination for potential shipping impacts
- **PDF Policy Analysis**: Analyzes procurement policies from uploaded PDF documents
- **Telegram Integration**: Sends automated alerts and analysis reports via Telegram
- **Interactive Web Interface**: User-friendly web interface for uploading documents and getting analysis

## 🚀 Demo

1. **Currency Analysis**:
   - Compares multiple currency rates against INR
   - Identifies best payment currency
   - Calculates potential savings

2. **Weather Analysis**:
   - Real-time weather data for shipping destinations
   - Impact assessment on delivery
   - Temperature, humidity, and wind conditions monitoring

3. **Procurement Analysis**:
   - Upload procurement documents (PDF)
   - Get intelligent analysis and recommendations
   - Compliance checking with policies

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/chandu6777/Procurement-Intelligence-Agent.git
   cd Procurement-Intelligence-Agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your API keys:
     - GEMINI_API_KEY
     - TELEGRAM_BOT_TOKEN
     - TELEGRAM_CHAT_ID
     - LANGCHAIN_API_KEY
     - OPENWEATHER_API_KEY

5. Run the application:
   ```bash
   python main.py
   ```

## 🌐 Usage

1. **Start the Application**:
   - Access the web interface at `http://localhost:5000`
   - You'll see the main dashboard

2. **Upload Documents**:
   - Click "Upload PDF" button
   - Select your procurement policy document
   - Submit for analysis

3. **Get Analysis**:
   - Enter import details (quantity, destination)
   - Click "Analyze"
   - Receive comprehensive analysis including:
     - Best currency for payment
     - Weather impact assessment
     - Delivery timeline estimates
     - Risk factors

4. **Telegram Notifications**:
   - Receive automated alerts
   - Get analysis summaries
   - Real-time updates

## 📚 API Documentation

### Currency Analysis
- Endpoint: `/analyze`
- Method: POST
- Parameters:
  - `quantity`: Number of units
  - `destination`: Delivery location
- Returns: Comprehensive analysis in JSON format

### PDF Upload
- Endpoint: `/upload_pdf`
- Method: POST
- Parameters:
  - `file`: PDF file
- Returns: Success/failure status

### Real-time Data
- Endpoint: `/get_realtime_data`
- Method: POST
- Returns: Current currency rates and weather data

## 🔑 Required API Keys

1. **Gemini API Key**:
   - Used for AI text analysis
   - Get from: [Google AI Studio](https://ai.google.dev/)

2. **Telegram Bot Token & Chat ID**:
   - For automated notifications
   - Create bot via [BotFather](https://telegram.me/BotFather)

3. **Langchain API Key**:
   - For document processing
   - Sign up at [Langchain](https://langchain.com)

4. **OpenWeather API Key**:
   - For weather data
   - Get from [OpenWeather](https://openweathermap.org/api)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.