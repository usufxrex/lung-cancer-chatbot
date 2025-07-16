from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from chatbot_utils import LungCancerDataProcessor, GeminiChatbot, is_lung_cancer_related

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize data processor and chatbot
print("🚀 Initializing Lung Cancer Chatbot...")
data_processor = LungCancerDataProcessor('data/lung_cancer_data.csv')
chatbot = GeminiChatbot(GEMINI_API_KEY, data_processor) if GEMINI_API_KEY else None

@app.route('/')
def index():
    """Render main chatbot interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not chatbot:
            return jsonify({'error': 'Chatbot not configured. Please check API key.'}), 500
        
        # Check if question is lung cancer related
        if not is_lung_cancer_related(user_message):
            response = """I specialize in lung cancer information based on my medical dataset. 
            I can help you with:
            
            • Lung cancer symptoms and risk factors
            • Dataset analysis and statistics
            • Prevention and lifestyle factors
            • Medical information related to lung cancer
            
            Please ask me something related to lung cancer, and I'll provide information based on my dataset of """ + str(data_processor.dataset_info.get('total_records', 0)) + """ cases."""
        else:
            # Get AI response
            response = chatbot.get_response(user_message)
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'dataset_loaded': not data_processor.df.empty,
        'total_records': len(data_processor.df),
        'gemini_configured': chatbot is not None and chatbot.model is not None
    })

@app.route('/api/dataset-info')
def dataset_info():
    """Get dataset information"""
    return jsonify(data_processor.dataset_info)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🫁 LUNG CANCER CHATBOT STARTING...")
    print("="*50)
    
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("Please add your API key to .env file")
        print("Example: GEMINI_API_KEY=your_actual_api_key_here")
    else:
        print("✅ Gemini API key loaded")
    
    print(f"📊 Dataset loaded: {len(data_processor.df)} records")
    print(f"🤖 Chatbot configured: {chatbot is not None and chatbot.model is not None}")
    print("🌐 Starting server on http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)