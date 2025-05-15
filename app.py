from flask import Flask, render_template, request, jsonify
from transformers import pipeline, set_seed

app = Flask(__name__)

# load once at startup
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def chat():
    user_input = request.form["message"]
    # generate a short completion
    out = generator(user_input,
                    max_length=50,
                    num_return_sequences=1,
                    pad_token_id=50256)  # GPT-2 EOS
    reply = out[0]["generated_text"][len(user_input):].strip()
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
