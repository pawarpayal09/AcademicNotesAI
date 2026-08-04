# 📚 Academic Notes AI

## 📖 Project Overview
Academic Notes AI is an AI-powered educational chatbot that helps students ask questions from academic PDF notes and receive accurate, context-based answers using Retrieval-Augmented Generation (RAG). It combines Google's Gemini LLM, LangChain, FAISS, and Sentence Transformer embeddings to provide intelligent responses.

---

## 🎯 Objectives
- Develop an AI chatbot for academic learning.
- Provide accurate answers from uploaded PDF notes.
- Reduce manual searching through study materials.
- Demonstrate the implementation of RAG and LLM technologies.
- Improve students' learning experience using AI.

---

## ❓ Problem Statement
Students spend significant time searching through lengthy PDF notes to find relevant information. This project solves the problem by allowing students to ask questions in natural language and instantly receive answers extracted from their study materials.

---

## ✨ Features
- 📚 Ask questions from academic notes
- 📄 Upload custom PDF documents
- 🤖 AI-powered question answering
- 💬 Chat history stored locally
- 🔊 Text-to-Speech (Listen Answer)
- 📥 Download chat as PDF
- 📑 Source document references
- 🎨 Modern Streamlit user interface
- ⚡ Fast semantic search using FAISS

---

## 🛠️ Technology Stack

### Frontend
- Streamlit
- HTML
- CSS

### Backend
- Python

### AI & Machine Learning
- Google Gemini
- LangChain
- Sentence Transformers
- FAISS

### Libraries
- PyPDF
- gTTS
- ReportLab
- python-dotenv

---

## 🏗️ Project Architecture

PDF Files
⬇
Text Extraction
⬇
Text Chunking
⬇
Embeddings Generation
⬇
FAISS Vector Database
⬇
User Question
⬇
Similarity Search
⬇
Gemini LLM
⬇
Final Answer

---

## ⚙️ Project Workflow
1. Upload academic PDF notes.
2. Extract text from PDFs.
3. Split text into chunks.
4. Generate embeddings.
5. Store embeddings in FAISS.
6. User asks a question.
7. Retrieve relevant chunks.
8. Gemini generates the final answer.
9. Display answer with source documents.

---

## 📂 Project Structure

```text
AcademicNotesChatbot/
│
├── app.py
├── rag.py
├── ingest.py
├── pdf_processor.py
├── speech.py
├── pdf_export.py
├── requirements.txt
├── .env
├── assets/
├── css/
├── data/
├── pages/
│   └── Chatbot.py
├── vectorstore/
└── README.md
```

---

## 🚀 Installation

```bash
git clone https://github.com/pawarpayal09/AcademicNotesAI.git

cd AcademicNotesAI

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file and add:

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run the Project

```bash
streamlit run app.py
```

---

## 📌 How to Use

1. Start the Streamlit application.
2. Select the knowledge source.
3. Upload a PDF (optional).
4. Ask a question.
5. View the AI-generated answer.
6. Listen to the answer using Text-to-Speech.
7. Download the chat as a PDF.

---

## 🧠 RAG Pipeline

- Document Loading
- Text Chunking
- Embedding Generation
- Vector Storage (FAISS)
- Similarity Search
- Prompt Generation
- Gemini Response

---

## 🔍 FAISS

FAISS stores vector embeddings of PDF text and performs fast similarity searches to retrieve the most relevant content before sending it to the LLM.

---

## 🔊 Text-to-Speech

The chatbot converts AI-generated answers into speech using the Google Text-to-Speech (gTTS) library, allowing users to listen to responses.

---

## 💬 Chat History

Previous conversations are stored locally and displayed in the sidebar, enabling users to revisit earlier chats.

---

## 📥 Export Chat

Users can download the complete conversation as a PDF file for future reference or offline study.

---

## 📈 Future Enhancements

- Speech-to-Text (Voice Input)
- Multi-language Support
- OCR for Image PDFs
- User Authentication
- Cloud Database Integration
- Mobile Application

---

## 👩‍💻 Developer

**Payal Pramod Pawar**

Master of Computer Applications (MCA)

---

## 🙏 Acknowledgements

- Google Gemini
- LangChain
- Hugging Face
- FAISS
- Streamlit
- ReportLab
- gTTS

---

## 📄 License

This project is developed for educational and academic purposes.