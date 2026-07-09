from time import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
from ai_service import generate_flashcards

app = Flask(__name__)
CORS(app)

# cooldown per IP
last_request = {}

@app.route("/")
def home():
    return "Server running"

@app.route("/upload", methods=["POST"])
def upload_pdf():
    ip = request.remote_addr
    now = time()

    # cooldown 12 sec
    if ip in last_request and now - last_request[ip] < 12:
        return jsonify({"error": "Too many requests. Wait a few seconds."}), 429

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    last_request[ip] = now

    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages[:5]:  # limitation for speed
            if page.extract_text():
                text += page.extract_text()

    flashcards = generate_flashcards(text)

    return jsonify(flashcards)

if __name__ == "__main__":
    app.run(debug=True)