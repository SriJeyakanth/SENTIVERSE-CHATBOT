from flask import Flask, render_template, request, jsonify
from flask_frozen import Freezer
import google.generativeai as ai

app = Flask(__name__)
freezer = Freezer(app)

# Replace with your actual Gemini API key
API_KEY = 'AIzaSyCIgHspeOtytvBf0_ohZZdt43DUqNJBf2Q'
ai.configure(api_key=API_KEY)

# Start a conversation using the model
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

# Predefined responses (supports emojis)
predefined_responses = {
    "who are you": "I am SentiVerse AI 😊",
    "hello": "Hi! How can I assist you today? 👋",
    "bye": "Goodbye! Have a great day! 👋",
    # ... other predefined responses ...
}

def handle_message(message):
    normalized_message = message.strip().lower()
    if normalized_message in predefined_responses:
        return predefined_responses[normalized_message]
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    user_message = request.form['message']
    predefined_response = handle_message(user_message)
    if predefined_response:
        return jsonify(response=predefined_response)

    try:
        response = chat.send_message(user_message)
        return jsonify(response=response.text)
    except Exception as e:
        return jsonify(response="Sorry, something went wrong. Please try again.")

if __name__ == '__main__':
    freezer.freeze()
    app.run(debug=True)
