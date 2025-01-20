# Python Tutor Chat App

This is a Python tutor chatbot that helps students with their Python programming exercises without providing complete solutions.

## Integration with Spikerpage

1. Create a new directory in your Spikerpage repo:
   ```bash
   cd Spikerpage
   mkdir python
   ```

2. Copy these files into the python directory:
   - netlify.toml
   - requirements.txt
   - templates/chat.html
   - netlify/functions/app.py

3. Configure Netlify environment variables:
   - Go to Site settings > Environment variables
   - Add the following variables:
     - GOOGLE_API_KEY: Your Google API key for Gemini
     - GEMINI_MODEL: gemini-pro

4. Update your Spikerpage repository:
   ```bash
   git add python/
   git commit -m "Add Python tutor chatbot"
   git push origin main
   ```

5. Netlify will automatically deploy the changes and the Python tutor will be available at TonySpiker.com/python

## Local Development

To run the app locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a .env file with your API keys:
   ```
   GOOGLE_API_KEY=your_api_key
   GEMINI_MODEL=gemini-pro
   ```

3. Run the development server:
   ```bash
   netlify dev
   ```

The app will be available at http://localhost:8888/python
