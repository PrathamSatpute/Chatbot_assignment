# Iron Lady Chatbot

## 🚀 Features Implemented

### Core Functionality
- **Smart FAQ System**: Instant responses to common questions about programs, duration, certificates, and mentors
- **AI-Powered Responses**: OpenAI GPT integration for handling complex queries
- **Modern UI**: Beautiful, responsive chat interface with smooth animations
- **Real-time Chat**: Live typing indicators and message animations
- **Quick Actions**: Pre-defined buttons for common questions
- **Error Handling**: Graceful handling of API failures and network issues

### User Experience
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Typing Indicators**: Shows when the bot is processing responses
- **Auto-scroll**: Automatically scrolls to latest messages
- **Enter Key Support**: Press Enter to send messages
- **Loading States**: Visual feedback during API calls
- **XSS Protection**: Secure message handling

## 🛠️ Tech Stack

### Backend
- **Flask 2.3.3**: Python web framework
- **OpenAI API**: GPT-3.5-turbo for AI responses
- **python-dotenv 1.0.0**: Environment variable management

### Frontend
- **HTML5**: Semantic markup
- **Tailwind CSS 2.2.19**: Utility-first CSS framework
- **Font Awesome 6.0.0**: Icons and visual elements
- **Vanilla JavaScript**: Modern ES6+ features

### Development Tools
- **Python 3.12+**: Programming language
- **Virtual Environment**: Isolated dependency management
- **Git**: Version control

## 📋 Prerequisites

- Python 3.12 or higher
- OpenAI API key (for AI responses)
- pip (Python package installer)

## 🚀 How to Run

### 1. Clone/Download the Project
```bash
# If using git
git clone <repository-url>
cd Chatbot

# Or download and extract the project files
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv chatbot_env

# Activate virtual environment
# On Windows:
chatbot_env\Scripts\activate
# On macOS/Linux:
source chatbot_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

**To get an OpenAI API key:**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up/Login to your account
3. Create a new API key
4. Copy the key and paste it in the `.env` file

### 5. Run the Application
```bash
python app.py
```

### 6. Access the Chatbot
Open your browser and go to: `http://localhost:5000`

## 🎯 Usage

### FAQ Questions (Work without API key)
- "What programs do you offer?"
- "Is the program online or offline?"
- "How long are the programs?"
- "Do you provide certificates?"
- "Tell me about mentors"

### AI Questions (Require API key)
- "What's the weather like?"
- "Tell me a joke"
- "What is leadership?"
- Any other general questions"# Chatbot_assignment" 
