from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# 🔐 Secure API Key loading (optional: use os.getenv if deployed)
GOOGLE_API_KEY = "AIzaSyD-nFR2QOqxkzk9z4oXbXiKrC3jlieAo70"  # Replace with your real API key

# ✅ Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Use correct model name — use full string from list_models()
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

# 🧠 Enable memory
chat = model.start_chat(history=[])

# ✅ Create Flask app
app = Flask(__name__, template_folder='templates')  # index.html must be in 'templates/'

# ✅ Route for frontend
@app.route('/')
def index():
    return render_template('index.html')

# ✅ POST /chat route for API
@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.json
    user_input = data.get('message')

    if not user_input:
        return jsonify({"reply": "⚠️ Please type something!"}), 400

    try:
        response_raw = chat.send_message(user_input)
        response = response_raw.text.strip()
        return jsonify({"reply": response})

    except Exception as e:
        print(" Error:", e)
        return jsonify({"reply": f"⚠️ Internal Error: {str(e)}"}), 500

# ✅ Run the server
if __name__ == '__main__':
    app.run(debug=True)

