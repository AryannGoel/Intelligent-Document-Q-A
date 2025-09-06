# app.py

import os
import fitz  # PyMuPDF
import faiss
import numpy as np
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import markdown2

# --- Initialization ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load models once at startup
print("Loading models...")
# Using a lightweight, high-performance model for embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
# Using a distilled, faster model for question answering
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
print("Models loaded successfully!")

# In-memory storage for document data
document_stores = {}

# --- Helper Functions ---

def chunk_text(text, chunk_size=300, chunk_overlap=50):
    """Splits text into overlapping chunks."""
    tokens = text.split()  # Simple whitespace tokenization
    chunks = []
    for i in range(0, len(tokens), chunk_size - chunk_overlap):
        chunk = " ".join(tokens[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def extract_text(file_path, file_type):
    """Extracts text from different file types."""
    if file_type == 'pdf':
        doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in doc)
        return text
    elif file_type == 'html':
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            # Remove script/style tags for cleaner text
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()
            return soup.get_text(separator='\n', strip=True)
    elif file_type == 'md':
        with open(file_path, 'r', encoding='utf-8') as f:
            html = markdown2.markdown(f.read())
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text(strip=True)
    return ""

def scrape_text_from_url(url):
    """Scrapes clean text from a URL."""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        # Remove common non-content tags
        for non_content in soup(["script", "style", "nav", "footer", "header"]):
            non_content.decompose()
        return soup.get_text(separator='\n', strip=True)
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

# --- API Endpoints ---

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_source():
    """Handles both file uploads and URL scraping."""
    text = ""
    filename = ""

    # Check if a URL was submitted
    if 'url' in request.form and request.form['url']:
        url = request.form['url']
        print(f"Scraping text from URL: {url}...")
        text = scrape_text_from_url(url)
        if text is None:
            return jsonify({"error": "Failed to scrape or process URL."}), 500
        # Create a filename from the URL
        filename = url.split('/')[-1] or url.replace('https://', '').replace('http://', '').replace('/', '_')

    # Check if a file was uploaded
    elif 'document' in request.files and request.files['document'].filename:
        file = request.files['document']
        filename = file.filename
        file_ext = filename.split('.')[-1].lower()

        if file_ext not in ['pdf', 'md', 'html']:
            return jsonify({"error": "Unsupported file type. Please upload PDF, Markdown, or HTML."}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        print(f"Extracting text from uploaded file: {filename}...")
        text = extract_text(file_path, file_ext)
    else:
        return jsonify({"error": "No document or URL provided"}), 400

    if not text:
        return jsonify({"error": "Could not extract any text from the source."}), 400

    try:
        # 2. Chunk Text
        print("Chunking text...")
        chunks = chunk_text(text)

        # 3. Generate Embeddings & Create Vector Store
        print("Generating embeddings and building FAISS index...")
        embeddings = embedding_model.encode(chunks, convert_to_tensor=False)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(np.array(embeddings))

        # 4. Store in memory
        document_stores[filename] = {
            "chunks": chunks,
            "index": index
        }

        print(f"Source '{filename}' processed successfully.")
        return jsonify({"message": f"Source '{filename}' processed successfully.", "filename": filename})

    except Exception as e:
        print(f"Error processing document: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handles a user's question about an uploaded document."""
    data = request.get_json()
    question = data.get('question')
    filename = data.get('filename')

    if not question or not filename:
        return jsonify({"error": "Missing question or filename"}), 400

    if filename not in document_stores:
        return jsonify({"error": "Document not found or not processed"}), 404

    try:
        doc_store = document_stores[filename]
        chunks = doc_store["chunks"]
        index = doc_store["index"]

        # 1. Retrieve Relevant Chunks
        print(f"Retrieving context for question: '{question}'")
        question_embedding = embedding_model.encode([question])
        k = 3 # Number of chunks to retrieve
        distances, indices = index.search(np.array(question_embedding), k)
        
        retrieved_chunks = [chunks[i] for i in indices[0]]
        context = " ".join(retrieved_chunks)

        # 2. Generate Answer using LLM
        print("Generating answer...")
        result = qa_pipeline(question=question, context=context)
        
        return jsonify({
            "answer": result['answer'],
            "source_context": context,
            "score": result['score']
        })

    except Exception as e:
        print(f"Error asking question: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)