# Intelligent Document Q&A System 📚

An interactive web application built for the Mission UpSkill India Hackathon. This project uses a Retrieval-Augmented Generation (RAG) pipeline to allow users to "chat" with their documents and get accurate, sourced answers to their questions.

---

## 🎯 Problem Statement

In today's information-rich world, professionals, students, and customers are often faced with the challenge of extracting specific information from lengthy documents. Manually searching through research papers, technical manuals, or internal knowledge bases is a slow, inefficient, and often frustrating process. This bottleneck hinders productivity and effective decision-making.

---

## ✨ Our Solution

Our application provides a seamless solution by allowing users to upload documents or scrape web pages and ask questions in plain English. The system leverages state-of-the-art AI models to understand the query, retrieve the most relevant passages from the text, and generate a concise, accurate answer, complete with the original source context for verification.



---

## 🛠️ Tech Stack & Architecture

This project is built on a modern, open-source stack designed for building AI-powered applications.

* **Backend:** Flask
* **Document Parsing:** PyMuPDF, BeautifulSoup, Markdown2
* **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` (from Hugging Face)
* **QA Model:** `distilbert-base-cased-distilled-squad` (from Hugging Face)
* **Vector Database:** FAISS (Facebook AI Similarity Search)
* **Core Libraries:** Transformers, PyTorch, NumPy
* **Frontend:** HTML, CSS, JavaScript

The architecture follows a standard RAG pipeline:
1.  **Ingestion:** Text is extracted from the source document/URL.
2.  **Chunking:** The text is split into smaller, overlapping chunks.
3.  **Embedding:** Each chunk is converted into a vector representation.
4.  **Indexing:** The vectors are stored in a FAISS index for fast retrieval.
5.  **Retrieval:** When a user asks a question, the query is embedded, and the most similar chunks are retrieved from the index.
6.  **Generation:** The user's question and the retrieved context are passed to a QA model to generate the final answer.

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

* Python 3.8 or higher
* pip (Python package installer)

### Installation

**1. Clone the repository:**
```bash
git clone <YOUR_GITHUB_REPO_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

**2. Create and activate a virtual environment:**
```bash
# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.\.venv\Scripts\activate
```

**3. Install the required dependencies:**
```Bash
pip install -r requirements.txt
```

### Running the Application

**1. Start the Flask server:**
```Bash
python app.py
```

**2. Open the application:**
Open your web browser and navigate to 
```Bash
http://127.0.0.1:5000.
```

## 📋 Features
1. Multi-Format Document Upload: Supports PDF, HTML, and Markdown files.
2. Web Page Scraping: Ingest content directly from a public URL.
3. RAG-Powered Q&A: Delivers accurate answers by grounding the language model in the provided text.
4. Source Verification: Displays the exact text chunks used to generate the answer, ensuring transparency and trust.
5. Interactive UI: A simple, clean, and intuitive web interface for a smooth user experience.
