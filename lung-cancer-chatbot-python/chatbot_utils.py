import pandas as pd
import json
import os
from typing import Dict, List, Any
import google.generativeai as genai
import time

class LungCancerDataProcessor:
    def __init__(self, csv_path: str):
        """Initialize the data processor with CSV file path"""
        self.csv_path = csv_path
        self.df = None
        self.dataset_info = None
        self.load_data()
    
    def load_data(self) -> None:
        """Load and process the CSV data"""
        try:
            print(f"📂 Loading dataset from: {self.csv_path}")
            self.df = pd.read_csv(self.csv_path)
            self.dataset_info = self.get_dataset_info()
            print(f"✅ Successfully loaded {len(self.df)} records from dataset")
        except FileNotFoundError:
            print(f"❌ Dataset file not found: {self.csv_path}")
            print("Please ensure your CSV file is in the data/ folder")
            self.df = pd.DataFrame()
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            self.df = pd.DataFrame()
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get comprehensive dataset information"""
        if self.df.empty:
            return {
                'total_records': 0,
                'columns': [],
                'cancer_cases': 0,
                'non_cancer_cases': 0,
                'age_stats': {'mean': 0, 'min': 0, 'max': 0},
                'gender_distribution': {},
                'smoking_stats': {},
                'common_symptoms': {}
            }
        
        info = {
            'total_records': len(self.df),
            'columns': list(self.df.columns),
            'cancer_cases': len(self.df[self.df['LUNG_CANCER'] == 'YES']) if 'LUNG_CANCER' in self.df.columns else 0,
            'non_cancer_cases': len(self.df[self.df['LUNG_CANCER'] == 'NO']) if 'LUNG_CANCER' in self.df.columns else 0,
            'age_stats': {
                'mean': float(self.df['AGE'].mean()) if 'AGE' in self.df.columns else 0,
                'min': int(self.df['AGE'].min()) if 'AGE' in self.df.columns else 0,
                'max': int(self.df['AGE'].max()) if 'AGE' in self.df.columns else 0
            },
            'gender_distribution': self.df['GENDER'].value_counts().to_dict() if 'GENDER' in self.df.columns else {},
            'smoking_stats': self.df['SMOKING'].value_counts().to_dict() if 'SMOKING' in self.df.columns else {},
            'common_symptoms': self.get_common_symptoms()
        }
        return info
    
    def get_common_symptoms(self) -> Dict[str, int]:
        """Get statistics for common symptoms"""
        symptom_columns = [
            'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC_DISEASE',
            'FATIGUE', 'ALLERGY', 'WHEEZING', 'ALCOHOL_CONSUMING', 'COUGHING',
            'SHORTNESS_OF_BREATH', 'SWALLOWING_DIFFICULTY', 'CHEST_PAIN'
        ]
        
        symptoms_stats = {}
        for symptom in symptom_columns:
            if symptom in self.df.columns:
                # Count cases where symptom = 2 (present)
                symptoms_stats[symptom] = int(len(self.df[self.df[symptom] == 2]))
        
        return symptoms_stats
    
    def get_sample_data(self, n: int = 5) -> List[Dict]:
        """Get sample data for AI context"""
        if self.df.empty:
            return []
        
        sample_df = self.df.head(n)
        return sample_df.to_dict('records')

class GeminiChatbot:
    def __init__(self, api_key: str, data_processor: LungCancerDataProcessor):
        """Initialize Gemini chatbot with API key and data processor"""
        self.api_key = api_key
        self.data_processor = data_processor
        self.model = None
        self.model_name = None
        self.setup_gemini()
    
    def setup_gemini(self) -> None:
        """Setup Gemini AI configuration with automatic model detection"""
        try:
            if not self.api_key:
                print("❌ No API key provided")
                return
                
            print(f"🔑 Configuring Gemini with API key: {self.api_key[:10]}...")
            genai.configure(api_key=self.api_key)
            
            # Try different model names in order of preference (updated for 2024)
            model_candidates = [
                'models/gemini-2.0-flash',        # Latest Gemini 2.0
                'models/gemini-1.5-flash',        # Reliable Gemini 1.5
                'models/gemini-1.5-pro',          # Pro version
                'models/gemini-2.5-flash',        # Preview version
                'gemini-1.5-flash',               # Without models/ prefix
                'gemini-1.5-pro'                  # Without models/ prefix
            ]
            
            for model_name in model_candidates:
                try:
                    print(f"🧪 Trying model: {model_name}")
                    model = genai.GenerativeModel(model_name)
                    
                    # Test the model
                    test_response = model.generate_content("Hello")
                    if test_response.text:
                        self.model = model
                        self.model_name = model_name
                        print(f"✅ Successfully configured with model: {model_name}")
                        return
                        
                except Exception as e:
                    print(f"⚠️ Model {model_name} failed: {e}")
                    continue
            
            # If all models fail, try to list available models
            try:
                print("🔍 Checking available models...")
                models = genai.list_models()
                for model in models:
                    if 'generateContent' in model.supported_generation_methods:
                        print(f"📋 Available: {model.name}")
                        try:
                            test_model = genai.GenerativeModel(model.name)
                            test_response = test_model.generate_content("Hello")
                            if test_response.text:
                                self.model = test_model
                                self.model_name = model.name
                                print(f"✅ Successfully configured with: {model.name}")
                                return
                        except:
                            continue
            except Exception as e:
                print(f"❌ Could not list models: {e}")
            
            print("❌ No working model found")
            
        except Exception as e:
            print(f"❌ Error configuring Gemini AI: {e}")
            self.model = None
    
    def create_context_prompt(self, user_question: str) -> str:
        """Create comprehensive context prompt for Gemini"""
        dataset_info = self.data_processor.dataset_info
        sample_data = self.data_processor.get_sample_data(3)
        
        context = f"""You are a medical chatbot specializing in lung cancer analysis. Answer ONLY lung cancer related questions based on the dataset provided.

DATASET SUMMARY:
- Total Records: {dataset_info.get('total_records', 0)}
- Cancer Cases: {dataset_info.get('cancer_cases', 0)}
- Non-Cancer Cases: {dataset_info.get('non_cancer_cases', 0)}
- Age Range: {dataset_info.get('age_stats', {}).get('min', 0)} to {dataset_info.get('age_stats', {}).get('max', 0)} years

COMMON SYMPTOMS (count of patients with symptom):
{json.dumps(dataset_info.get('common_symptoms', {}), indent=2)}

SAMPLE DATA:
{json.dumps(sample_data, indent=2)}

INSTRUCTIONS:
1. Answer only lung cancer related questions
2. Use dataset statistics in your response
3. Be informative but concise
4. Include medical disclaimer
5. If non-lung cancer question, redirect politely

USER QUESTION: {user_question}

Provide a helpful response based on the dataset:"""
        
        return context
    
    def get_response(self, user_question: str) -> str:
        """Get response from Gemini AI with enhanced error handling"""
        if not self.model:
            return f"❌ Chatbot not properly configured. No working model found. Please check your API key and internet connection."
        
        try:
            print(f"🤖 Processing question with {self.model_name}: {user_question[:50]}...")
            
            prompt = self.create_context_prompt(user_question)
            
            # Add timeout and retry logic
            for attempt in range(2):
                try:
                    response = self.model.generate_content(prompt)
                    
                    if response.text:
                        print("✅ Response generated successfully")
                        return response.text
                    else:
                        print(f"⚠️ Empty response on attempt {attempt + 1}")
                        time.sleep(1)
                        
                except Exception as e:
                    print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                    if attempt < 1:
                        time.sleep(2)
                    else:
                        raise e
            
            return "I couldn't generate a response after multiple attempts. Please try rephrasing your question."
                
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            
            # Provide specific error messages
            if "API_KEY" in str(e).upper():
                return "❌ API key error. Please check your Gemini API key configuration."
            elif "QUOTA" in str(e).upper():
                return "❌ API quota exceeded. Please try again later."
            elif "SAFETY" in str(e).upper():
                return "❌ Content filtered for safety. Please rephrase your question."
            else:
                return f"❌ Technical error: {str(e)[:100]}. Please try again."

def is_lung_cancer_related(question: str) -> bool:
    """Check if question is related to lung cancer"""
    lung_cancer_keywords = [
        'lung cancer', 'lung', 'cancer', 'smoking', 'cough', 'coughing',
        'chest pain', 'shortness of breath', 'wheezing', 'fatigue',
        'yellow fingers', 'chronic disease', 'anxiety', 'allergy',
        'swallowing difficulty', 'symptoms', 'risk factors', 'prevention',
        'dataset', 'medical', 'health', 'diagnosis', 'treatment', 'breath'
    ]
    
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in lung_cancer_keywords)