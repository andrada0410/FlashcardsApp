from time import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pdfplumber, docx
from ai_service import generate_flashcards

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

CORS(app)

# cooldown per IP
last_request = {}

def extract_text_from_pdf(file_stream):
    text = ""
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages[:5]:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_stream):
    doc = docx.Document(file_stream)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text)
    return "\n".join(full_text)

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

    # cooldown 12 sec
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

if __name__ == "__main__":
    app.run(debug=True)