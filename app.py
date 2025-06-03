from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

# Configuration for multiple API endpoints
API_CONFIGURATIONS = [
    {
        "name": "OpenRouter DeepSeek",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "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",
        "model": "deepseek/deepseek-chat",
        "headers": {
            "Authorization": "Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-site.com"
        }
    },
    {
        "name": "OpenRouter Anthropic",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "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",
        "model": "anthropic/claude-3-opus",
        "headers": {
            "Authorization": "Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-site.com"
        }
    },
    # Add more backup APIs as needed
]

SYSTEM_PROMPT = "You are SYNOVA AI, built by Sri Jeyakanth, a GENAI enthusiast. You must reply in a polite and practical way.use more relevent emojis."

def get_bot_response(user_input):
    error_messages = []
    
    for config in API_CONFIGURATIONS:
        try:
            # Prepare headers with API key
            headers = {k: v.format(api_key=config["api_key"]) for k, v in config["headers"].items()}
            
            data = {
                "model": config["model"],
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7
            }
            
            # Make the API request with timeout
            start_time = time.time()
            response = requests.post(
                f"{config['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=15  # 15 seconds timeout
            )
            
            if response.status_code == 200:
                completion = response.json()
                return {
                    "success": True,
                    "response": completion['choices'][0]['message']['content'],
                    "provider": config["name"],
                    "response_time": time.time() - start_time
                }
            else:
                error_messages.append(f"{config['name']} error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            error_messages.append(f"{config['name']} connection failed: {str(e)}")
            continue
    
    # If all APIs failed
    return {
        "success": False,
        "error": "All API providers failed. Please try again later.",
        "details": error_messages
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.json["user_input"]
    response = get_bot_response(user_input)
    
    if response["success"]:
        return jsonify({
            "bot_response": response["response"],
            "provider": response["provider"],
            "response_time": response["response_time"]
        })
    else:
        return jsonify({
            "bot_response": response["error"],
            "error_details": response["details"],
            "provider": "Fallback"
        }), 503

if __name__ == "__main__":
    app.run(debug=True)
