from flask import Flask, render_template, request, jsonify
import google.generativeai as ai

app = Flask(__name__)

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
    "❤️": "Love is in the air! 😊",
     "who created you?": "I was created by a dedicated team: K. Sri Jeyakanth, R. Sudhan Kumar, and H. Abilash.",
    "who trained you?": "All my AI and NLP functionalities were programmed and trained by K. Sri Jeyakanth from Palani, Tamil Nadu. He is an AI enthusiast, NLP, and chatbot expert.",
    "who developed the app?": "The app development was handled by R. Sudhan Kumar, a skilled Flutter developer from Pollachi, Coimbatore, Tamil Nadu.",
    "who contributed to cybersecurity?": "H. Abilash, a cybersecurity expert and junior Flutter developer from Pollachi, Tamil Nadu, ensured robust security measures.",
    "what is your purpose?": "I am designed to provide advanced sentiment analysis and NLP functionalities, powered by AI expertise from Sri Jeyakanth.",
    "what does sri jeyakanth do?": "Sri Jeyakanth is an AI enthusiast specializing in NLP and chatbot development. He designed and trained the AI behind me.",
    "what does sudhan kumar do?": "R. Sudhan Kumar is a Flutter app developer responsible for creating the user interface and app functionality.",
    "what does abilash do?": "H. Abilash is a cybersecurity expert and data analytics manager. He also contributed to app development as a junior Flutter developer.",
    "where is the team from?": "The team is from Tamil Nadu, India. Sri Jeyakanth is from Palani, while Sudhan Kumar and Abilash are from Pollachi.",
    "who leads AI development?": "AI development is led by K. Sri Jeyakanth, the NLP and chatbot expert.",
    "who ensured app security?": "App security was managed by H. Abilash, the cybersecurity expert.",
    "who created the user interface?": "The user interface was designed and implemented by R. Sudhan Kumar, the Flutter developer.",
    "who is sri jeyakanth?": "K. Sri Jeyakanth is an AI enthusiast, NLP, and chatbot expert from Palani, Tamil Nadu. He specializes in advanced AI development.",
    "who is sudhan kumar?": "R. Sudhan Kumar is a Flutter app developer from Pollachi, Coimbatore. He handled all Flutter-related development for this app.",
    "who is abilash?": "H. Abilash is a cybersecurity expert, data analytics manager, and junior Flutter developer from Pollachi, Tamil Nadu.",
    "what is NLP?": "Natural Language Processing (NLP) involves enabling machines to understand and process human language. This was implemented by K. Sri Jeyakanth.",
    "what is flutter?": "Flutter is a framework for app development. All Flutter-related work was done by R. Sudhan Kumar and supported by H. Abilash.",
    "what is cybersecurity?": "Cybersecurity ensures data and application safety. This was managed by H. Abilash.",
    "can I contact the team?": "You can contact the creators: Sri Jeyakanth (AI and NLP), Sudhan Kumar (Flutter), and Abilash (Cybersecurity and analytics).",
    "who are the main contributors?": "The main contributors are K. Sri Jeyakanth (AI and NLP), R. Sudhan Kumar (Flutter), and H. Abilash (Cybersecurity and analytics).",
    "who developed the sentiment analysis feature?": "The sentiment analysis feature was programmed and trained by K. Sri Jeyakanth.",
    "who ensured app performance?": "App performance was optimized by R. Sudhan Kumar, with inputs from H. Abilash.",
    "what makes this app unique?": "This app combines cutting-edge NLP, secure design, and user-friendly interfaces developed by a skilled team.",
    "who ensured app scalability?": "App scalability was handled by R. Sudhan Kumar, with backend support from K. Sri Jeyakanth.",
    "who is responsible for bug fixes?": "Bug fixes are managed collaboratively by the entire team: Sri Jeyakanth, Sudhan Kumar, and Abilash.",
    "who provided the AI expertise?": "AI expertise was provided by K. Sri Jeyakanth, an NLP and chatbot expert.",
    "who integrated batch analysis?": "Batch analysis was integrated by K. Sri Jeyakanth as part of the backend functionality.",
    "what is the role of abilash?": "H. Abilash played a crucial role in cybersecurity, data analytics, and junior Flutter development.",
    "what is the role of sudhan kumar?": "R. Sudhan Kumar managed the entire Flutter app development process.",
    "what is the role of sri jeyakanth?": "Sri Jeyakanth is the AI architect, handling NLP models, sentiment analysis logic, and chatbot features.",
    "how secure is the app?": "The app is highly secure, thanks to the expertise of H. Abilash in cybersecurity.",
    "what is the team’s vision?": "The team aims to create impactful AI-driven applications with user-friendly designs and robust security.",
    "who designed the chatbot?": "The chatbot feature was designed by K. Sri Jeyakanth.",
    "what is your backend technology?": "The backend is powered by Python, developed by K. Sri Jeyakanth.",
    "who implemented file uploads?": "File upload functionality was implemented by R. Sudhan Kumar with backend support from Sri Jeyakanth.",
    "who ensured user-friendly design?": "User-friendly design was ensured by R. Sudhan Kumar with inputs from the entire team.",
    "who created the batch processing feature?": "Batch processing for CSV files was created by K. Sri Jeyakanth.",
    "who handled data visualization?": "Data visualization features were implemented by R. Sudhan Kumar.",
    "who contributed to app security?": "App security was managed by H. Abilash, the cybersecurity expert.",
    "who reviewed the app?": "The app was thoroughly reviewed by the team: Sri Jeyakanth, Sudhan Kumar, and Abilash.",
    "who managed user feedback?": "User feedback management was a team effort led by H. Abilash.",
    "who optimized performance?": "Performance optimization was handled by R. Sudhan Kumar.",
    "who provided backend logic?": "The backend logic was developed by K. Sri Jeyakanth.",
    "who created the API?": "The API for the app was designed and developed by K. Sri Jeyakanth.",
    "who implemented badword detection?": "Badword detection was implemented by K. Sri Jeyakanth in the backend.",
    "who created the charts?": "Charts for data visualization were implemented by R. Sudhan Kumar.",
    "who ensured data privacy?": "Data privacy was ensured by the cybersecurity expert, H. Abilash.",
    "who integrated real-time analysis?": "Real-time analysis was integrated by K. Sri Jeyakanth.",
    "who contributed to multilingual support?": "Multilingual support was designed by K. Sri Jeyakanth.",
    "who worked on app updates?": "App updates are managed by the team: Sudhan Kumar, Abilash, and Sri Jeyakanth.",
     "who is the NLP expert?": "The NLP expert is K. Sri Jeyakanth.",
    "who is the chatbot expert?": "The chatbot expert is K. Sri Jeyakanth.",
    "who handled Flutter animations?": "Flutter animations were handled by R. Sudhan Kumar.",
    "who ensured app compatibility?": "App compatibility was ensured by R. Sudhan Kumar.",
    "who developed the report feature?": "The report download feature was developed by K. Sri Jeyakanth.",
    "who implemented language models?": "Language models were implemented by K. Sri Jeyakanth.",
    "who are you?": "I am SentiVerse AI.I am a NLP(Natural Language Processing) powered AI chatbot.I can help you to analyze the sentiments.",
    "who are you": "I am SentiVerse AI.I am a NLP(Natural Language Processing) powered AI chatbot.I can help you to analyze the sentiments.",
    "who are u?": "I am SentiVerse AI.I am a NLP(Natural Language Processing) powered AI chatbot.I can help you to analyze the sentiments.",
    "who are u": "I am SentiVerse AI.I am a NLP(Natural Language Processing) powered AI chatbot.I can help you to analyze the sentiments.",
    "hello": "Hi! How can I assist you today?",
    "bye": "Goodbye! Have a great day!",
    "how many languages do you know?":"More than 100 languages like tamil,kannada,english,telugu,hindi,chinese,etc.,",
    # Add more predefined responses with emojis here
}

# Function to handle user input and match emojis
def handle_message(message):
    # Normalize input by stripping whitespace and converting to lowercase
    normalized_message = message.strip().lower()
    # Return predefined response if exists
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
    app.run(debug=True)  

import time

def send_message_with_retry(chat, user_message, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = chat.send_message(user_message)
            return response.text
        except ai.errors.ApiError as api_err:
            app.logger.error(f"API Error on attempt {attempt + 1}: {api_err}")
            time.sleep(delay)  # Wait before retrying
        except Exception as e:
            app.logger.error(f"General Error on attempt {attempt + 1}: {e}")
            time.sleep(delay)  # Wait before retrying
    return "Sorry, something went wrong. Please try again."

@app.route('/chat', methods=['POST'])
def chat_response():
    user_message = request.form['message']
    predefined_response = handle_message(user_message)
    if predefined_response:
        return jsonify(response=predefined_response)
    
    response_text = send_message_with_retry(chat, user_message)
    return jsonify(response=response_text)

