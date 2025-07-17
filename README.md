# 🫁 Lung Cancer Risk Assessment Chatbot

An AI-powered chatbot that provides lung cancer insights based on a comprehensive dataset of 3,001 medical cases. Built with Python Flask and Google's Gemini AI.

![Chatbot Demo](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-orange.svg)

## 🚀 Features

- **Dataset-Based Responses**: All answers derived from 3,001 real medical cases
- **Smart Filtering**: Only responds to lung cancer-related queries
- **Real-time Statistics**: Live dataset insights and analysis
- **Professional UI**: Clean, medical-themed interface
- **Comprehensive Analysis**: Age, gender, symptoms, and risk factor correlations

## 📊 Dataset Information

- **Total Records**: 3,001 medical cases
- **Parameters**: 16 medical indicators including demographics, symptoms, and risk factors
- **Coverage**: Smoking, chest pain, coughing, shortness of breath, age, gender, and more
- **Target Variable**: Lung cancer diagnosis (YES/NO)

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **AI Model**: Google Gemini 2.0 Flash
- **Data Processing**: Pandas
- **Frontend**: HTML5, CSS3, JavaScript
- **Environment**: Python 3.8+

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/lung-cancer-chatbot.git
   cd lung-cancer-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file and add:
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Add your dataset**
   ```bash
   # Place your CSV file at: data/lung_cancer_data.csv
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
lung-cancer-chatbot/
├── data/
│   └── lung_cancer_data.csv    # Medical dataset
├── static/
│   └── style.css              # Styling
├── templates/
│   └── index.html             # Main interface
├── app.py                     # Flask application
├── chatbot_utils.py           # Core chatbot logic
├── test_api.py               # API testing script
├── requirements.txt          # Dependencies
├── .env                      # Environment variables
└── README.md                 # Documentation
```

## 🔑 Getting Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

## 💬 Sample Questions

**✅ Supported Queries:**
- "What are the most common lung cancer symptoms?"
- "How many smoking cases are in your dataset?"
- "What's the age distribution of cancer patients?"
- "How does chest pain correlate with lung cancer?"

**❌ Filtered Queries:**
- Non-lung cancer medical questions
- General health inquiries
- Unrelated topics

## 🧪 Testing

```bash
# Test API configuration
python test_api.py

# Test with sample questions
# Visit http://localhost:5000 and try the sample questions above
```

## 📊 Dataset Features

| Feature | Description | Values |
|---------|-------------|---------|
| AGE | Patient age | Numeric |
| GENDER | Patient gender | M/F |
| SMOKING | Smoking status | 1=No, 2=Yes |
| CHEST_PAIN | Chest pain presence | 1=No, 2=Yes |
| COUGHING | Persistent cough | 1=No, 2=Yes |
| SHORTNESS_OF_BREATH | Breathing difficulty | 1=No, 2=Yes |
| ... | 10 more symptoms | 1=No, 2=Yes |
| LUNG_CANCER | Diagnosis | YES/NO |

## 🔒 Security & Privacy

- **No Data Storage**: User conversations are not stored
- **API Key Protection**: Environment variables for sensitive data
- **Medical Disclaimer**: Clear warnings about professional consultation
- **Input Validation**: Sanitized user inputs

## 🚨 Medical Disclaimer

This chatbot is for **educational purposes only** and should not replace professional medical advice. Always consult qualified healthcare providers for medical concerns.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛠️ Troubleshooting

### Common Issues:

**API Key Error:**
```bash
# Verify your API key
python test_api.py
```

**Dataset Not Found:**
```bash
# Ensure CSV file is at: data/lung_cancer_data.csv
```

**Module Import Error:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 📞 Support

For support, please open an issue in the GitHub repository or contact 

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Advanced data visualizations
- [ ] Mobile app version
- [ ] Real-time model training
- [ ] Integration with hospital systems

---

**Built with ❤️ for medical research and education**

*Last updated: January 2025*
