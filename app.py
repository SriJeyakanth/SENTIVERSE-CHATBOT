from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Your OpenAI API key
api_key = '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'

# Define the base URL for the OpenRouter API
base_url = "https://openrouter.ai/api/v1"

# Set headers for the request
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# Function to interact with the API and get chatbot response
def get_bot_response(user_input):
    data = {
        "model": "deepseek/deepseek-chat",  # specify the model you want to use
        "messages": [
            {"role": "system", "content": "You are SYNOVA AI, built by Sri Jeyakanth, a GENAI enthusiast. You must reply in a polite and practical way."},
            {"role": "user", "content": user_input}
        ]
    }
    
    response = requests.post(f"{base_url}/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        completion = response.json()
        return completion['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.json["user_input"]
    bot_response = get_bot_response(user_input)
    return jsonify({"bot_response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
