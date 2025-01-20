from flask import Flask, request, jsonify, render_template_string
import os
import json
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

# Store the HTML template as a string
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Chat Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            display: flex;
            height: 100vh;
        }

        .instructions {
            width: 300px;
            padding: 20px;
            background: white;
            box-shadow: 2px 0 4px rgba(0,0,0,0.1);
            overflow-y: auto;
        }

        .instructions h2 {
            margin-bottom: 15px;
            color: #007bff;
        }

        .instructions ol {
            padding-left: 20px;
        }

        .instructions li {
            margin-bottom: 15px;
        }

        .chat-container {
            flex-grow: 1;
            padding: 20px;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .chat-messages {
            flex-grow: 1;
            overflow-y: auto;
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .message {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
            white-space: pre-wrap;
            overflow-wrap: break-word;
        }

        .user-message {
            background: #f0f7ff;
            margin-left: 20px;
        }

        .bot-message {
            background: #f9f9f9;
            margin-right: 20px;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }

        .bot-message code {
            background: #f0f0f0;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
        }

        .bot-message pre {
            background: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', monospace;
        }

        .input-container {
            display: flex;
            gap: 10px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        textarea {
            flex-grow: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            resize: none;
            height: 50px;
            font-family: inherit;
            font-size: 16px;
        }

        button {
            padding: 0 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background: #0056b3;
        }

        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <div class="instructions">
        <h2>How to Use</h2>
        <ol>
            <li>Ask the chatbot if it can help you with an exercise, then paste the exercise into the chat.</li>
            <li>Read the full output and answer any questions the chatbot asks you.</li>
            <li>As the chatbot helps you with the code, also write the code in the CODEHS editor.</li>
            <li>If you get errors on execution of your code, paste the error into the chatbot, along with a full copy of your code.</li>
            <li>Follow the chatbot's instructions to fix the code.</li>
        </ol>
    </div>
    <div class="chat-container">
        <div class="chat-messages" id="chat-messages"></div>
        <div class="input-container">
            <textarea
                id="user-input" 
                placeholder="Type your message here..."
                onkeydown="if(event.keyCode === 13 && !event.shiftKey) { event.preventDefault(); sendMessage(); }"
            ></textarea>
            <button onclick="sendMessage()" id="send-button">Send</button>
        </div>
    </div>

    <script>
        const messagesContainer = document.getElementById('chat-messages');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');

        function formatResponse(text) {
            // Replace markdown-style code blocks with HTML
            text = text.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
            
            // Replace inline code with HTML
            text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
            
            // Replace asterisks with HTML
            text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
            text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
            
            return text;
        }

        function appendMessage(content, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            
            if (isUser) {
                messageDiv.textContent = content;
            } else {
                messageDiv.innerHTML = formatResponse(content);
            }
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;

            // Disable input while processing
            userInput.disabled = true;
            sendButton.disabled = true;

            // Display user message
            appendMessage(message, true);
            userInput.value = '';

            try {
                const response = await fetch('/python/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message })
                });

                const data = await response.json();
                appendMessage(data.response, false);
            } catch (error) {
                appendMessage('Sorry, there was an error processing your message.', false);
            }

            // Re-enable input
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }

        // Focus input on page load
        window.onload = () => userInput.focus();
    </script>
</body>
</html>"""

def handler(event, context):
    # Get the HTTP method and path
    http_method = event.get('httpMethod', '')
    path = event.get('path', '').replace('/python', '')
    
    if http_method == 'GET' and path == '/':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': HTML_TEMPLATE
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
