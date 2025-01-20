from flask import Flask, request, jsonify, render_template_string
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask.json import jsonify
from http.client import responses

# Load environment variables
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Static system prompt
SYSTEM_PROMPT = """You are an expert python tutor.  You HELP students complete their exercises, but you NEVER give students the full and complete code."""

# Initialize chat at module level
model = genai.GenerativeModel(os.getenv('GEMINI_MODEL', 'gemini-pro'))
chat = model.start_chat()
chat.send_message(SYSTEM_PROMPT)

def handler(event, context):
    # Get the HTTP method and path
    http_method = event.get('httpMethod', '')
    path = event.get('path', '').replace('/python', '')
    
    if http_method == 'GET' and path == '/':
        # Read the HTML template
        with open('templates/chat.html', 'r') as f:
            html_content = f.read()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html_content
        }
    
    elif http_method == 'POST' and path == '/api/chat':
        try:
            # Parse the request body
            body = json.loads(event.get('body', '{}'))
            user_input = body.get('message')
            
            if not user_input:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'No message provided'})
                }
            
            # Send message and get response
            response = chat.send_message(user_input)
            
            # Handle response parts
            parts = []
            for part in response.parts:
                if hasattr(part, 'text'):
                    parts.append(part.text)
            
            bot_response = '\n'.join(parts)
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'response': bot_response})
            }
                
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': f'Server error: {str(e)}'})
            }
    
    return {
        'statusCode': 404,
        'body': json.dumps({'error': 'Not Found'})
    }
