import os
from time import time
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from ai_service import generate_flashcards
from services.text_extraction_service import extract_text_from_pdf, extract_text_from_docx
from services.pdf_service import generate_pdf

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

CORS(app)

last_request = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/flashcardsPage.html")
def flashcards_page():
    return render_template("flashcardsPage.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    ip = request.remote_addr
    now = time()

    if ip in last_request and now - last_request[ip] < 12:
        return jsonify({"error": "Too many requests. Wait a few seconds."}), 429

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename.lower()
    
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        return jsonify({"error": "Only PDF and DOCX files are allowed."}), 400

    if not text.strip():
        return jsonify({"error": "Could not extract text from the file."}), 400

    last_request[ip] = now
    card_count = request.form.get("cardCount", 15)

    flashcards = generate_flashcards(text, card_count)
    return jsonify(flashcards)

@app.route('/export-pdf', methods=['POST'])
def export_pdf():
    data = request.get_json()
    cards = data.get('cards', [])
    filename = data.get('filename', 'flashcards')

    if not cards:
        return jsonify({'error': 'Nu există carduri'}), 400

    buffer, output_filename = generate_pdf(cards, filename)

    return send_file( buffer, as_attachment=True, download_name=output_filename, mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True)