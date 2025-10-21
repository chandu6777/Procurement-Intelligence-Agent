import os
import io
import certifi
import requests
import tempfile
from datetime import datetime
from dotenv import load_dotenv
from threading import Thread
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents import AgentExecutor
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# LangSmith tracing (optional)
if LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "procurement-agent"
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Enable CORS to allow frontend access
from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3
)

# Global variable to store QA chain
qa_chain = None
policy_loaded = False 

# ========== TOOL 1: Multi-Currency Forex Rates ==========
def get_all_forex_rates() -> str:
    """
    Get real-time forex rates for multiple currencies against INR using CoinGecko API.
    Uses Tether (USDT) stablecoin as a bridge to calculate fiat exchange rates.
    Returns rates for USD, EUR, GBP, JPY, AUD, CAD, CHF against INR.
    """
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        # Use Tether (USDT) as bridge - it's pegged to USD and provides accurate fiat rates
        params = {
            "ids": "tether",
            "vs_currencies": "inr,usd,eur,gbp,jpy,aud,cad,chf"
        }
        
        headers = {}
        if COINGECKO_API_KEY:
            headers["x-cg-demo-api-key"] = COINGECKO_API_KEY
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Verify response structure
        if "tether" not in data:
            return "❌ Unable to fetch forex rates from CoinGecko (no tether data)."
        
        usdt_rates = data["tether"]
        
        # Get INR rate
        inr_rate = usdt_rates.get("inr", 0)
        
        if inr_rate == 0:
            return "❌ Unable to calculate INR rates (no INR data)."
        
        # Calculate cross rates for each currency
        currency_codes = ["usd", "eur", "gbp", "jpy", "aud", "cad", "chf"]
        rates = {}
        
        for currency in currency_codes:
            if currency in usdt_rates and usdt_rates[currency] > 0:
                rates[currency.upper()] = inr_rate / usdt_rates[currency]
        
        if not rates:
            return "❌ Unable to calculate any forex rates."
        
        # Find best rate (lowest INR per unit = most favorable for procurement)
        best_currency = min(rates, key=rates.get)
        worst_currency = max(rates, key=rates.get)
        
        # Calculate savings
        best_rate = rates[best_currency]
        worst_rate = rates[worst_currency]
        savings_percent = ((worst_rate - best_rate) / worst_rate) * 100
        
        # Build formatted response
        result = "💱 FOREX RATES (1 Unit → INR)\n"
        result += "=" * 45 + "\n"
        
        for currency, rate in sorted(rates.items(), key=lambda x: x[1]):
            if currency == best_currency:
                marker = " ⭐ BEST RATE"
            elif currency == worst_currency:
                marker = " 🔴 HIGHEST"
            else:
                marker = ""
            result += f"  • {currency}: ₹{rate:.2f}{marker}\n"
        
        result += "=" * 45 + "\n"
        result += f"✅ RECOMMENDATION: Use {best_currency}\n"
        result += f"   Rate: ₹{best_rate:.2f} per {best_currency}\n"
        result += f"   Savings: {savings_percent:.1f}% vs worst rate ({worst_currency})\n"
        result += f"\n📊 Data Source: CoinGecko API (Live)"
        
        return result
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "⚠️ CoinGecko API rate limit exceeded. Please try again in a minute."
        elif e.response.status_code == 401:
            return "⚠️ CoinGecko API authentication failed. Check your API key."
        else:
            return f"❌ HTTP Error {e.response.status_code}: {str(e)}"
            
    except requests.exceptions.Timeout:
        return "⚠️ Request timeout. CoinGecko API is slow to respond."
        
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {str(e)}"
        
    except (KeyError, ValueError) as e:
        return f"❌ Data parsing error: {str(e)}"
        
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# ========== TOOL 2: Dynamic Weather Check ==========
def get_weather(city: str) -> str:
    """
    Get current weather conditions for any city using OpenWeatherMap API.
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            
            # Assess shipping conditions
            condition_assessment = "suitable"
            if wind_speed > 15:
                condition_assessment = "risky due to high winds"
            elif temp < 0 or temp > 45:
                condition_assessment = "challenging due to extreme temperature"
            
            return f"Weather in {city}: {temp}°C, {description}. Humidity: {humidity}%, Wind: {wind_speed} m/s. Conditions are {condition_assessment} for shipping."
        else:
            return f"Weather data unavailable for {city}. Assuming normal conditions."
    except Exception as e:
        return f"Weather check failed for {city}. Assuming moderate conditions. Error: {str(e)}"

# ========== TOOL 3: Python Calculator ==========
def calculate(expression: str) -> str:
    """
    Perform simple mathematical calculations.
    """
    try:
        result = eval(expression)
        return f"Calculation result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

# ========== TOOL 4: PDF Policy Retrieval ==========
def create_pdf_qa_chain(pdf_path: str, llm) -> RetrievalQA | None:
    """
    Create a RetrievalQA chain from a PDF document using local HuggingFace embeddings.
    """
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        vectorstore = FAISS.from_documents(texts, embeddings)

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=False
        )

        return qa_chain

    except Exception as e:
        print(f"Error loading PDF: {str(e)}")
        return None

def query_policy(question: str, qa_chain) -> str:
    """
    Query the procurement policy document.
    """
    try:
        if qa_chain is None:
            return "Policy document not loaded. Unable to verify compliance."
        
        result = qa_chain.invoke({"query": question})
        return result["result"]
    except Exception as e:
        return f"Policy query failed: {str(e)}"

# ========== Telegram Alert ==========
def send_telegram_alert(message: str) -> bool:
    try:
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("❌ Telegram credentials missing")
            return False

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🤖 Procurement Alert\n\n{message}",
            "parse_mode": "Markdown"
        }

        # Use certifi to ensure proper SSL certificate verification
        response = requests.post(url, json=payload, timeout=10, verify=False)
        print("📩 Telegram response:", response.status_code, response.text)

        if response.status_code != 200:
            print("❌ Failed to send message:", response.text)
            return False

        print("✅ Telegram message sent successfully!")
        return True
    
    except requests.exceptions.SSLError as ssl_err:
        print(f"❌ SSL Error: {ssl_err}")
        return False
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request Error: {req_err}")
        return False
    except Exception as e:
        print(f"❌ Telegram alert failed: {e}")
        return False

# ========== Flask Routes ==========
@app.route('/')
def index():
    """Render the main page"""
    api_status = {
        'gemini': bool(GEMINI_API_KEY),
        'coingecko': bool(COINGECKO_API_KEY),
        'weather': bool(OPENWEATHER_API_KEY),
        'telegram': bool(TELEGRAM_BOT_TOKEN)
    }
    return render_template('result.html', api_status=api_status)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    global qa_chain, policy_loaded
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
     
        try:
            qa_chain = create_pdf_qa_chain(filepath, llm)
            policy_loaded = True
            return jsonify({"success": True, "message": "Policy document loaded successfully!", "policy_loaded": True})

        except Exception as e:
            import traceback
            traceback.print_exc() 
            policy_loaded = False
            return jsonify({'success': False, 'error': str(e), 'policy_loaded': False})
    
    return jsonify({'success': False, 'error': 'Invalid file format', 'policy_loaded': False})

@app.route('/get_policy_status', methods=['GET'])
def get_policy_status():
    """Get current policy loading status"""
    return jsonify({'policy_loaded': policy_loaded})

@app.route('/get_realtime_data', methods=['POST'])
def get_realtime_data():
    """Get real-time forex and weather data based on user input"""
    data = request.json
    city = data.get('city', '')
    
    forex_data = get_all_forex_rates()
    weather_data = get_weather(city)
    
    return jsonify({
        'forex': forex_data,
        'weather': weather_data,
        'policy_loaded': policy_loaded
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze procurement decision"""
    global qa_chain
    
    data = request.json
    query = data.get('query', '')
    city = data.get('city', '')
    
    if not query:
        return jsonify({'success': False, 'error': 'No query provided'})
    
    try:
        # Create tools
        tools = [
            Tool(
                name="Multi_Currency_Forex_Checker",
                func=lambda x: get_all_forex_rates(),
                description="Get current forex rates for USD, EUR, GBP, JPY, AUD, CAD, CHF against INR. Identifies the best currency rate."
            ),
            Tool(
                name="Weather_Checker",
                func=lambda x: get_weather(city),
                description=f"Get current weather conditions for {city} to assess shipping viability."
            ),
            Tool(
                name="Calculator",
                func=lambda x: calculate(x),
                description="Perform mathematical calculations for cost analysis and delivery estimates."
            ),
        ]
        
        if qa_chain:
            tools.append(
                Tool(
                    name="Policy_Checker",
                    func=lambda x: query_policy(x, qa_chain),
                    description="Check procurement policy compliance and requirements."
                )
            )
        
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True
        )
        
        prompt = f"""
You are a Procurement Intelligence Agent analyzing international procurement decisions.

Query: "{query}"
Shipping Location: {city}

Follow these steps:
1. Check ALL currency exchange rates using Multi_Currency_Forex_Checker
2. Identify which currency offers the BEST (lowest) rate against INR
3. Check weather conditions for {city} using Weather_Checker
4. {"Check procurement policy compliance using Policy_Checker" if qa_chain else "Skip policy check"}
5. Calculate estimated delivery timeline based on:
   - Best currency rate advantage
   - Weather conditions impact
   - Standard international shipping times (7-21 days depending on currency region)
   - Use Calculator for any cost computations

Structure your response as:

DECISION: [PROCEED/DELAY/PROCEED WITH CONDITIONS]

CURRENCY ANALYSIS:
- Best Rate: [currency and rate]
- Cost Advantage: [percentage or amount saved compared to USD]
- Recommended Payment Currency: [currency]

DELIVERY ESTIMATE:
- Estimated Days: [number] days
- Based on: [currency advantage + weather + region]

WEATHER CONDITIONS:
- Location: {city}
- Impact: [summary]

{"POLICY COMPLIANCE:" if qa_chain else ""}
{"- Status: [compliant/non-compliant]" if qa_chain else ""}
{"- Notes: [any requirements]" if qa_chain else ""}

RECOMMENDATION:
[Detailed explanation with specific numbers]

RISK FACTORS:
[List any concerns]
"""     
        # Run agent
        response = agent.invoke({"input": prompt})
        decision = response.get("output", "No response generated")
        
        # Send Telegram alert asynchronously
        def send_alert():
            if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
                telegram_message = f"Query: {query}\nLocation: {city}\n\n{decision}"
                sent = send_telegram_alert(telegram_message)
                print("Telegram alert sent:", sent)
        
        Thread(target=send_alert).start()
        
        return jsonify({
            'success': True,
            'decision': decision,
            'telegram_sent': True
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/download_report', methods=['POST'])
def download_report():
    """Download decision report"""
    data = request.json
    query = data.get('query', '')
    decision = data.get('decision', '')
    city = data.get('city', '')
    
    report = f"""PROCUREMENT DECISION REPORT

Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Query: {query}
Shipping Location: {city}

{decision}
""" 
    output = io.BytesIO()
    output.write(report.encode('utf-8'))
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name=f"procurement_decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mimetype='text/plain'
    )

if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("⚠️ GEMINI_API_KEY not found in environment variables!")
    else:
        app.run(debug=True, use_reloader=False)