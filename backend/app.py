import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ Use your Google Gemini API Key
GOOGLE_API_KEY = "........"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Check for the correct model name
MODEL_NAME = "gemini-2.5-pro"  # Change this based on the available models

# ✅ Predefined responses
responses = {
    "hello": "Hi there! How can I assist you?",
    "how are you": "I'm just a bot, but I'm doing great!",
    "what is your name": "I am Naarad, your student AI assistant.",
    "who is your founder ?": "Dinesh Yadav",
}

# ✅ Function to get AI response
def generate_response(user_input):
    user_input = user_input.lower().strip()

    if user_input in responses:
        return responses[user_input]
    
    # stop function


    # ✅ Use Google Gemini API
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(user_input)

        if hasattr(response, "text"):
            return response.text.strip()
        else:
            return "Error: No response from AI."
    except Exception as e:
        return f"Error: {str(e)}"

# ✅ API Endpoint for Chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    bot_response = generate_response(user_message)
    return jsonify({"reply": bot_response})

@app.route('/')
def home():
    return "Flask server is running. Use /chat endpoint for chatbot."

if __name__ == '__main__':   
    app.run(debug=True)
