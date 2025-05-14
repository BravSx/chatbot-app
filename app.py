from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Simple HTML form for chat
CHAT_PAGE = """
<!doctype html>
<title>Demo Chatbot</title>
<h1>Demo Chatbot</h1>
<form action="/" method="post">
  <input name="message" placeholder="Say something…" size="40">
  <input type="submit" value="Send">
</form>
{% if reply %}
  <p><strong>Bot:</strong> {{ reply }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    reply = None
    if request.method == "POST":
        user_msg = request.form.get("message", "")
        # “LLM” logic: here we just echo back
        reply = f"Echo: {user_msg}"
    return render_template_string(CHAT_PAGE, reply=reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
