from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_url_path='/python/static')
app.config['APPLICATION_ROOT'] = '/python'

# Configure Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Static system prompt
SYSTEM_PROMPT = """You are an expert python tutor.  You HELP students complete their exercises, but you NEVER give students the full and complete code."""

# Initialize chat at module level
model = genai.GenerativeModel(os.getenv('GEMINI_MODEL', 'gemini-pro'))
chat = model.start_chat()
chat.send_message(SYSTEM_PROMPT)

# Routes
@app.route('/python/')
def home():
    try:
        # Reset chat when loading the page
        global chat
        chat = model.start_chat()
        chat.send_message(SYSTEM_PROMPT)
        
        print("DEBUG: Template directory:", app.template_folder)
        print("DEBUG: Attempting to render chat.html")
        return render_template('chat.html')
    except Exception as e:
        print(f"DEBUG: Error details - {type(e).__name__}: {str(e)}")
        print(f"DEBUG: Template folder contents:", os.listdir(app.template_folder))
        raise

@app.route('/python/api/chat', methods=['POST'])
def chat_endpoint():
    try:
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        # Send message and get response
        response = chat.send_message(user_input)
        
        # Handle response parts
        parts = []
        for part in response.parts:
            if hasattr(part, 'text'):
                parts.append(part.text)
        
        bot_response = '\n'.join(parts)
        
        return jsonify({'response': bot_response})
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
