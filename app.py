from flask import Flask, request, jsonify, render_template_string
import os
import openai

app = Flask(__name__)

# ✅ Use OpenAI key from Render environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Frontend UI (HTML + JS)
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
  <title>AkinBest AI</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f4f4f4; }
    #chatbox { width: 70%; margin: 40px auto; background: white; padding: 20px;
               border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    #messages { height: 400px; overflow-y: auto; border: 1px solid #ccc; 
                padding: 10px; border-radius: 8px; margin-bottom: 10px; }
    .msg { margin: 8px 0; padding: 6px 10px; border-radius: 6px; max-width: 80%; }
    .user { background: #d0e6ff; text-align: right; }
    .bot { background: #e2f7e1; }
    #input { width: 70%; padding: 10px; border-radius: 6px; border: 1px solid #ccc; }
    button { padding: 10px 16px; margin-left: 8px; border: none; border-radius: 6px;
             background: #4CAF50; color: white; cursor: pointer; }
    button:hover { background: #45a049; }
  </style>
</head>
<body>
  <div id="chatbox">
    <h2>🤖 AkinBest AI</h2>
    <div id="messages"></div>
    <input id="input" type="text" placeholder="Type your message..." />
    <button onclick="sendMessage()">Send</button>
  </div>
  <script>
    async function sendMessage() {
      let input = document.getElementById("input").value;
      if (!input.trim()) return;
      addMessage("You", input, "user");
      document.getElementById("input").value = "";
      addMessage("AI", "⏳ Thinking...", "bot");
      try {
        let res = await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: input })
        });
        let data = await res.json();
        updateLastBotMessage(data.reply || data.error);
      } catch (err) {
        updateLastBotMessage("⚠️ Error: " + err.message);
      }
    }
    function addMessage(sender, text, cls) {
      let div = document.createElement("div");
      div.classList.add("msg", cls);
      div.innerHTML = `<b>${sender}:</b> ${text}`;
      document.getElementById("messages").appendChild(div);
      document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
    }
    function updateLastBotMessage(newText) {
      let messages = document.getElementById("messages").getElementsByClassName("bot");
      let last = messages[messages.length - 1];
      last.innerHTML = `<b>AI:</b> ${newText}`;
    }
  </script>
</body>
</html>
"""

# ✅ Health check route
@app.route("/healthz")
def healthz():
    return "ok", 200

# ✅ Home route
@app.route("/")
def home():
    return render_template_string(HTML_CODE)

# ✅ Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "⚠️ Please type a message."})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are AkinBest AI, a helpful chatbot."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Start app (Render overrides port automatically)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
