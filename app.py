import fitz  # PyMuPDF
import json
from flask import Flask, request, jsonify
import os
from transformers import pipeline
import waitress

app = Flask(__name__)

# Load the question-answering model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Percorso della directory contenente i PDF
pdf_dir = 'C:/Users/UTENTE/LineeGUIDATIp/pdf'

# Funzione per estrarre testo dai PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Estrazione e salvataggio dei testi
def save_text_to_json(pdf_path, json_path):
    text = extract_text_from_pdf(pdf_path)
    data = {"content": text}
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Percorsi dei file PDF e JSON
pdf_files = [
    ("REV.2024.01.02 Linee guida.pdf", "linee_guida.json"),
    ("2024.01.02 PROCEDURE ATIPROJECT.pdf", "procedure.json"),
    ("2024.01.02 VALIDAZIONE ZUCCHETTI E CALENDARIO ASSENZE.pdf", "validazione.json")
]

# Estrazione dei testi
for pdf, json_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf)
    save_text_to_json(pdf_path, json_file)

# Carica i dati estratti dai PDF
def load_data():
    with open('linee_guida.json', 'r', encoding='utf-8') as f:
        linee_guida_data = json.load(f)['content']
    with open('procedure.json', 'r', encoding='utf-8') as f:
        procedure_data = json.load(f)['content']
    with open('validazione.json', 'r', encoding='utf-8') as f:
        validazione_data = json.load(f)['content']
    return linee_guida_data, procedure_data, validazione_data

linee_guida_data, procedure_data, validazione_data = load_data()

# Funzione per trovare la risposta utilizzando il modello di question-answering
def find_answer(question):
    context = linee_guida_data + " " + procedure_data + " " + validazione_data
    result = qa_pipeline(question=question, context=context)
    return result['answer']

@app.route('/chatbot', methods=['POST'])
def chatbot():
    question = request.json.get('question')
    response = find_answer(question)
    return jsonify({'response': response})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)
