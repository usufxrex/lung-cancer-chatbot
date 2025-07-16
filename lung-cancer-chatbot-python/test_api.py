import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

print("🔍 Testing Gemini API Key...")
print(f"API Key found: {'✅' if api_key else '❌'}")

if api_key:
    print(f"API Key length: {len(api_key)}")
    print(f"API Key starts with: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Try current models in order of preference
        preferred_models = [
            'models/gemini-2.0-flash',           # Latest Gemini 2.0
            'models/gemini-1.5-flash',           # Reliable Gemini 1.5
            'models/gemini-1.5-pro',             # Pro version
            'models/gemini-2.5-flash',           # Preview version
        ]
        
        print("\n🧪 Testing preferred models:")
        
        for model_name in preferred_models:
            try:
                print(f"  Testing {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say hello in one sentence")
                
                if response.text:
                    print(f"  ✅ {model_name} - WORKING!")
                    print(f"  Response: {response.text}")
                    print(f"\n🎯 RECOMMENDED MODEL: {model_name}")
                    break
                    
            except Exception as e:
                print(f"  ❌ {model_name} failed: {str(e)[:100]}")
                continue
        else:
            print("\n⚠️ All preferred models failed. Trying any available model...")
            
            # If preferred models fail, try any available model
            models = genai.list_models()
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    # Skip deprecated models
                    if 'vision' in model.name.lower() or '1.0-pro' in model.name:
                        continue
                        
                    try:
                        print(f"  Testing {model.name}...")
                        test_model = genai.GenerativeModel(model.name)
                        response = test_model.generate_content("Hello")
                        
                        if response.text:
                            print(f"  ✅ {model.name} - WORKING!")
                            print(f"  Response: {response.text}")
                            print(f"\n🎯 WORKING MODEL FOUND: {model.name}")
                            break
                            
                    except Exception as e:
                        print(f"  ❌ {model.name} failed: {str(e)[:50]}")
                        continue
            else:
                print("❌ No working model found")
                
    except Exception as e:
        print(f"❌ API configuration error: {e}")
else:
    print("❌ No API key found. Please check your .env file")