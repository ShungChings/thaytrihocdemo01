from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Define the route for PhoGPT API integration
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user's input from the frontend
        data = request.get_json()
        user_message = data.get("message")

        # PhoGPT API setup (replace with actual URL or credentials if needed)
        api_url = 'http://localhost:8000/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "model": "vinai/PhoGPT-4B-Chat",
            "messages": [{"role": "user", "content": user_message}]
        }

        # Make a POST request to PhoGPT API
        response = requests.post(api_url, headers=headers, json=payload)
        response_data = response.json()

        # Extract the AI's reply from the response
        ai_reply = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Error: No response")

        # Return the AI's reply to the frontend
        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port=8000)
