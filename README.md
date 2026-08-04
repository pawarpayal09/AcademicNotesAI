# 📚 Academic Notes AI – Intelligent RAG Chatbot for Academic Learning

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
- 🤖 AI-powered question answering using Gemini
- 💬 Chat history stored locally
- ⭐ Save important AI answers for quick access
- 📌 Dedicated Saved Notes page
- 🔍 Search saved notes instantly
- 🗑 Remove saved notes anytime
- 🔊 Text-to-Speech (Listen Answer)
- 📥 Download chat as PDF
- 📑 Source document references
- 🎨 Modern and responsive Streamlit user interface
- ⚡ Fast semantic search using FAISS
- 📂 Organized sidebar navigation

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
- JSON (Local Storage)

---

## 📂 Project Structure

```text
AcademicNotesAI/
│
├── app.py
├── rag.py
├── ingest.py
├── pdf_processor.py
├── pdf_export.py
├── speech.py
├── chat_history_manager.py
├── favourites_manager.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── css/
│   └── style.css
│
├── data/
│   └── (Academic PDF Notes)
│
├── pages/
│   ├── Chatbot.py
│   └── FavouriteNotes.py
│
├── storage/
│   ├── chat_history.json
│   └── favourites.json
│
├── vectorstore/
│   ├── index.faiss
│   └── index.pkl
│
├── .devcontainer/
│   └── devcontainer.json
│
├── test_rag.py
│
└── venv/          (Local Virtual Environment - Not uploaded to GitHub)
```

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
10. Save important answers for future revision.

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
2. Select the desired knowledge source.
3. Upload academic PDF notes (optional).
4. Ask questions in natural language.
5. View AI-generated answers.
6. Save important answers using **Save Note**.
7. Open **Saved Notes** to revisit bookmarked answers.
8. Search saved notes instantly.
9. Listen to answers using Text-to-Speech.
10. Download the complete chat as a PDF.

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

All conversations are automatically stored locally and displayed in the sidebar, allowing users to continue previous discussions without losing context.

---

## ⭐ Saved Notes

The chatbot allows users to save important AI-generated answers for future reference.

Features include:

- 📌 Save important answers with one click
- 📚 Dedicated Saved Notes page
- 🔍 Search saved notes instantly
- 🗑 Remove saved notes when no longer needed
- 📅 Displays save date for each note
- ⚡ Quickly reopen saved academic concepts

This feature helps students build their own personalized revision notes while studying.

---

## 📥 Export Chat

Users can download the complete conversation as a PDF file for future reference or offline study.

---

## 📈 Future Enhancements

- 🎤 Speech-to-Text (Voice Input)
- 🌐 Multi-language Support
- 🧠 AI-generated Quiz Mode
- 🔖 Note Categories & Tags
- 👤 User Authentication
- ☁ Cloud Database Integration
- 📱 Mobile Application
- 🌙 Dark / Light Theme Support

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