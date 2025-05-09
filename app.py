from flask import Flask, request, jsonify
from flask_cors import CORS
import language_tool_python
import os
import json
import fitz  # PyMuPDF for PDF reading
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load grammar checking tool
tool = language_tool_python.LanguageTool('en-US')

# Load BERT model for classification
MODEL_NAME = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

# Helper function for sentiment classification using BERT
def classify_text_with_bert(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=1).item()
    return "Positive" if prediction == 1 else "Negative"

# ============= ROUTES ==============

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    text = ''

    # Read file
    if file.filename.endswith('.pdf'):
        try:
            pdf = fitz.open(stream=file.read(), filetype="pdf")
            for page in pdf:
                text += page.get_text()
        except Exception as e:
            return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 400

    elif file.filename.endswith('.txt'):
        try:
            text = file.read().decode('utf-8')
        except Exception as e:
            return jsonify({"error": f"Failed to process TXT: {str(e)}"}), 400

    elif file.filename.endswith('.json'):
        try:
            json_data = json.load(file)
            text = json.dumps(json_data, indent=2)
        except Exception as e:
            return jsonify({"error": f"Failed to process JSON: {str(e)}"}), 400

    else:
        return jsonify({"error": "Unsupported file format"}), 400

    if not text.strip():
        return jsonify({"error": "Empty file"}), 400

    # Summarization (using DistilBART for efficiency)
    try:
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        if len(text) > 1000:
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
            summaries = []
            for chunk in chunks:
                chunk_summary = summarizer(chunk, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
                summaries.append(chunk_summary)
            summary = "\n".join(summaries)
        else:
            summary = summarizer(text, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
    except Exception as e:
        summary = f"Unable to summarize due to: {str(e)}"

    # Grammar check
    grammar_matches = tool.check(text)
    grammar_errors = len(grammar_matches)
    grammar_score = max(0, 100 - grammar_errors * 2)

    # Section presence check
    important_sections = ['Education', 'Experience', 'Skills', 'Projects', 'Certifications']
    sections_found = sum(1 for section in important_sections if section.lower() in text.lower())
    section_score = (sections_found / len(important_sections)) * 100
    missing_sections = [section for section in important_sections if section.lower() not in text.lower()]

    # Sentiment classification using BERT
    sentiment = classify_text_with_bert(text)

    # Final score
    final_score = int((grammar_score + section_score) / 2)

    return jsonify({
        "summary": summary,
        "score": final_score,
        "grammar_issues": grammar_errors,
        "missing_sections": missing_sections,
        "sentiment": sentiment
    })

# ============== MAIN ==============

if __name__ == '__main__':
    app.run(debug=True)