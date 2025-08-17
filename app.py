from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Health check route for Render
@app.route("/healthz")
def healthz():
    return "ok", 200

# Home route
@app.route("/")
def home():
    return "🚀 AkinSokpah AI Bot is live!"

# Simple chat endpoint (optional)
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150
        )
        return jsonify({"reply": response.choices[0].text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
