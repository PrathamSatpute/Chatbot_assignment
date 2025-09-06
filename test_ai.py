#!/usr/bin/env python3
"""
Test script to verify AI functionality
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_connection():
    """Test OpenAI API connection"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    print("🔍 Testing OpenAI API Configuration...")
    print(f"API Key found: {'Yes' if api_key and api_key != 'your_openai_api_key_here' else 'No'}")
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ No valid API key found!")
        print("📝 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=sk-your-actual-api-key-here")
        return False
    
    try:
        # Try new version first, fallback to old version
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            print("✅ Using OpenAI v1.0+ (new version)")
            
            # Test API call with new version
            print("🚀 Testing API call...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'Hello, AI is working!' if you can respond."}
                ],
                max_tokens=50
            )
            result = response.choices[0].message.content
            
        except ImportError:
            import openai
            openai.api_key = api_key
            print("✅ Using OpenAI v0.28 (legacy version)")
            
            # Test API call with old version
            print("🚀 Testing API call...")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'Hello, AI is working!' if you can respond."}
                ],
                max_tokens=50
            )
            result = response["choices"][0]["message"]["content"]
        
        print(f"✅ AI Response: {result}")
        print("🎉 AI functionality is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing AI: {e}")
        return False

if __name__ == "__main__":
    test_openai_connection()
