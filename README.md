# 📄 AI PDF Research Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/HuggingFace-BART-yellow?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/FAISS-Vector_Search-green?style=for-the-badge"/>
</p>

<p align="center">
  <b>Upload. Analyze. Summarize. Research Smarter.</b>
</p>

---

# 🚀 Overview

AI PDF Research Assistant is an intelligent document analysis tool that transforms lengthy PDFs into concise, actionable insights.

Powered by state-of-the-art NLP models, the application enables users to:

✅ Extract text from PDFs

✅ Automatically organize content into sections

✅ Generate AI-powered summaries

✅ Store processed content for retrieval

✅ Prepare documents for semantic search and research workflows

Built using **Streamlit**, **Hugging Face Transformers**, **Sentence Transformers**, **FAISS**, and **SQLite**.

---

# 🎯 Why This Project?

Researchers, students, analysts, and professionals often spend hours reading lengthy reports, papers, and technical documentation.

This project helps users:

* Understand documents faster
* Reduce reading time
* Extract key information quickly
* Improve research productivity

---

# ⚡ Features

## 📂 PDF Upload

Upload any PDF document directly through the Streamlit interface.

```text
PDF → Text Extraction → Processing Pipeline
```

---

## 🔍 Intelligent Text Extraction

Using **PyMuPDF (fitz)**, the system extracts text from every page while preserving document structure.

### Benefits

* Fast processing
* Accurate extraction
* Supports multi-page documents

---

## 🧠 Automatic Section Detection

The application identifies probable document headings and organizes content into logical sections.

Example:

```text
Introduction
Methodology
Results
Discussion
Conclusion
```

This improves document navigation and downstream analysis.

---

## 📝 AI-Powered Summarization

Uses:

```python
facebook/bart-large-cnn
```

to generate high-quality summaries.

### Summary Modes

#### Short Summary

Ideal for:

* Quick review
* Executive overview
* Fast understanding

#### Detailed Summary

Ideal for:

* Research papers
* Technical reports
* In-depth analysis

---

## 🗄️ Database Storage

Processed document sections are automatically stored in SQLite.

Benefits:

* Persistent storage
* Structured retrieval
* Future search capabilities

---

## 🔎 Semantic Search Ready

The project uses:

```python
all-MiniLM-L6-v2
```

from Sentence Transformers.

Combined with FAISS indexing, the system is ready for:

* Semantic Search
* RAG Pipelines
* Question Answering Systems
* Knowledge Bases

---

# 🏗️ System Architecture

```text
PDF Upload
    │
    ▼
Text Extraction (PyMuPDF)
    │
    ▼
Section Segmentation
    │
    ▼
SQLite Storage
    │
    ▼
Embedding Generation
(Sentence Transformers)
    │
    ▼
FAISS Indexing
    │
    ▼
AI Summarization
(BART Large CNN)
    │
    ▼
Streamlit Interface
```

---

# 🛠️ Tech Stack

| Category            | Technology                |
| ------------------- | ------------------------- |
| Frontend            | Streamlit                 |
| NLP                 | Hugging Face Transformers |
| Summarization Model | BART Large CNN            |
| Embeddings          | Sentence Transformers     |
| Vector Search       | FAISS                     |
| Database            | SQLite                    |
| PDF Processing      | PyMuPDF                   |
| Language            | Python                    |

---

# 📸 Application Preview

## Home Screen

Upload PDF documents directly from your browser.

---

## Processing Pipeline

The system:

1. Extracts text
2. Detects sections
3. Stores structured content
4. Generates summaries

---

## Summary Generation

Choose between:

* Short Summary
* Detailed Summary

and instantly generate AI-powered insights.

---

# 📂 Project Structure

```text
pdf-research-assistant/
│
├── app.py
├── document_data.db
├── requirements.txt
│
├── models/
│
├── assets/
│
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/pdf-research-assistant.git
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run app.py
```

---

# 📈 Future Enhancements

* Conversational PDF Chat
* RAG Integration
* Multi-PDF Analysis
* Citation Extraction
* Research Paper Comparison
* Keyword Highlighting
* Knowledge Graph Generation
* Cloud Deployment

---

# 💡 Example Use Cases

### 🎓 Students

Summarize lecture notes and research papers.

### 🔬 Researchers

Extract key findings from scientific literature.

### 💼 Professionals

Review reports and technical documents faster.

### ⚖️ Legal Teams

Analyze contracts and policy documents.

---

# 🌟 Key Highlights

* AI-Powered Summarization
* Semantic Search Ready
* Modular Architecture
* Research-Oriented Design
* Streamlit Interface
* Production-Friendly Foundation

---

# 👩‍💻 Author

**Devanshi Das**

Electronics & Communication Engineering Student
AI • Machine Learning • Intelligent Systems

📧 [dasdevanshi7@gmail.com](mailto:dasdevanshi7@gmail.com)

---

<p align="center">
⭐ If you found this project useful, consider starring the repository!
</p>
