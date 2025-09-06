from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# 🔑 Initialize OpenAI - try new version first, fallback to old version
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_openai_api_key_here":
    print("⚠️  No OpenAI API key found. AI responses will be disabled.")
    print("📝 To enable AI responses, create a .env file with: OPENAI_API_KEY=your_actual_key")
    openai_client = None
    OPENAI_NEW_VERSION = None
else:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=api_key)
        OPENAI_NEW_VERSION = True
        print("✅ Using OpenAI v1.0+ (new version)")
    except ImportError:
        import openai
        openai.api_key = api_key
        openai_client = openai
        OPENAI_NEW_VERSION = False
        print("✅ Using OpenAI v0.28 (legacy version)")

# FAQ dictionary
faqs = {
    "programs": "Iron Lady offers comprehensive leadership development programs focusing on confidence building, communication skills, and workplace success. Our programs are designed to empower women in their professional journeys.",
    "duration": "Our programs typically run for 8-12 weeks, depending on the specific module you choose. Each session is carefully structured to provide maximum learning and development.",
    "mode": "Great question! Our programs are offered in both online and offline formats to accommodate different learning preferences and schedules. You can choose the format that works best for you.",
    "certificate": "Yes, absolutely! All participants receive official certificates upon successful completion of the program. These certificates are recognized and can enhance your professional profile.",
    "mentors": "Our programs are led by experienced mentors and coaches from various industries. They bring real-world expertise and are dedicated to helping you achieve your leadership goals."
}

# Rule-based FAQ check with improved logic
def get_faq_answer(message):
    msg = message.lower()
    
    # Check for specific combinations first (more specific matches)
    if ("online" in msg or "offline" in msg) and ("program" in msg or "course" in msg or "training" in msg):
        return faqs["mode"]
    elif "duration" in msg and ("program" in msg or "course" in msg or "training" in msg):
        return faqs["duration"]
    elif "certificate" in msg and ("program" in msg or "course" in msg or "training" in msg):
        return faqs["certificate"]
    elif ("mentor" in msg or "coach" in msg) and ("program" in msg or "course" in msg or "training" in msg):
        return faqs["mentors"]
    
    # Then check for individual keywords
    elif "online" in msg or "offline" in msg or "mode" in msg or "format" in msg:
        return faqs["mode"]
    elif "duration" in msg or "length" in msg or "weeks" in msg or "months" in msg:
        return faqs["duration"]
    elif "certificate" in msg or "certification" in msg or "cert" in msg:
        return faqs["certificate"]
    elif "mentor" in msg or "coach" in msg or "instructor" in msg or "teacher" in msg:
        return faqs["mentors"]
    elif "program" in msg or "course" in msg or "training" in msg or "workshop" in msg:
        return faqs["programs"]
    else:
        return None

# AI fallback using OpenAI
def get_ai_answer(message):
    try:
        # Check if OpenAI client is available
        if openai_client is None:
            return "I'm sorry, but the AI service is not configured. Please add your OpenAI API key to the .env file to enable AI responses."
        
        # Use appropriate API call based on OpenAI version
        if OPENAI_NEW_VERSION:
            # New OpenAI v1.0+ API
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful chatbot answering FAQs about Iron Lady leadership programs. Keep responses concise and helpful. If you don't know something specific about Iron Lady, politely say so and suggest contacting support."},
                    {"role": "user", "content": message}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content
        else:
            # Legacy OpenAI v0.28 API
            response = openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful chatbot answering FAQs about Iron Lady leadership programs. Keep responses concise and helpful. If you don't know something specific about Iron Lady, politely say so and suggest contacting support."},
                    {"role": "user", "content": message}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response["choices"][0]["message"]["content"]
            
    except Exception as e:
        error_msg = str(e)
        print(f"OpenAI API Error: {e}")
        
        # Handle specific error types
        if "quota" in error_msg.lower() or "429" in error_msg:
            return "I'm sorry, but I've reached my usage limit for today. Please try again later or contact our support team for assistance. In the meantime, feel free to ask me about our programs, duration, certificates, or mentors!"
        elif "api_key" in error_msg.lower():
            return "I'm sorry, but there's an issue with my AI service configuration. Please contact our support team for assistance."
        else:
            return f"I'm sorry, I'm having trouble processing your request right now. Please try again or contact our support team for assistance."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Validate request
        if not request.json or "message" not in request.json:
            return jsonify({"error": "Invalid request format"}), 400
        
        user_message = request.json.get("message", "").strip()
        
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # 1️⃣ Try FAQ first
        answer = get_faq_answer(user_message)

        # 2️⃣ If not found, use AI
        if not answer:
            answer = get_ai_answer(user_message)

        return jsonify({"answer": answer})
    
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
