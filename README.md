🧑‍🎓 StudyNova – Intelligent Academic Learning Assistant

StudyNova is an AI-powered academic learning application developed for students. The project started as an Academic Notes AI chatbot and has been expanded into a complete study assistant with RAG-based question answering, PDF learning, image study, quiz generation, YouTube learning resources, saved notes, Firebase authentication, dashboard tracking, and a user activity dataset for data analysis.

The GitHub repository/project name remains AcademicNotesAI, while the application is branded as StudyNova.

📖 Project Overview

StudyNova helps students understand academic content faster by combining Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), vector search, document processing, and several external APIs.

The application can:

Answer questions from academic PDF notes.

Allow users to upload and chat with their own PDF files.

Analyze academic images, diagrams, screenshots, and study material.

Generate multiple-choice quizzes from academic topics.

Search educational YouTube resources.

Save important AI answers for later revision.

Keep chat history and learning activity records.

Provide Firebase-based user authentication.

Show personalized dashboard information.

Maintain a combined dataset of user activities from multiple JSON files.

Display the complete multi-user activity dataset in the Dataset page.

Download the fused dataset as an Excel file for further analysis.

🎯 Objectives

The main objectives of StudyNova are:

Build an AI-based academic learning assistant.

Provide context-based answers from academic documents.

Reduce the time required to search through long study materials.

Demonstrate the practical use of LLM and RAG technologies.

Provide multiple learning tools in one application.

Track student learning activities for dashboard and data-analysis purposes.

Prepare structured project activity data that can be used for future data-science and machine-learning work.

Provide a simple and student-friendly interface for academic use.

❓ Problem Statement

Students often spend a lot of time searching through lengthy PDF notes, books, research papers, and other study material to find specific information.

StudyNova solves this problem by allowing students to ask questions in natural language and receive answers based on relevant academic content. The system can also support visual learning, practice quizzes, video resources, saved answers, and progress tracking.

✨ Main Features

📚 1. Academic Notes Chatbot

Students can ask questions from the academic PDF notes available in the project.

Features include:

Semantic search over academic documents.

RAG-based context retrieval.

Gemini-generated answers.

Source document references.

Student-friendly explanations.

Chat history.

Regenerate answer option.

Feedback option.

Text-to-Speech for answers.

PDF export of conversations.

📄 2. Upload and Chat with Your Own PDF

Users can upload their own academic PDF files and ask questions from them.

The system:

Loads the PDF.

Extracts the text.

Splits the document into smaller chunks.

Generates embeddings.

Creates a FAISS vector store.

Searches the most relevant chunks.

Sends the retrieved context to Gemini.

Generates the final answer.

This can be used for notes, textbooks, assignments, research papers, and other academic documents.

🖼️ 3. Image Study Assistant

Users can upload study images and ask AI to understand the content.

Supported examples include:

Textbook pages.

Handwritten notes.

Diagrams.

Charts.

Tables.

Questions.

Programming code screenshots.

Academic screenshots.

The user can ask the system to:

Explain the topic.

Summarize the notes.

Extract important points.

Explain a diagram.

Solve a question step-by-step.

🧠 4. Automatic Quiz Generator

The Quiz module creates AI-generated multiple-choice questions from an academic topic.

Available settings:

Easy difficulty.

Medium difficulty.

Hard difficulty.

5 questions.

10 questions.

15 questions.

The module calculates:

Score.

Accuracy/percentage.

Correct answers.

Wrong answers.

Answer explanations.

Quiz activity is also stored for dashboard and dataset analysis.

🎥 5. YouTube Learning Resources

The application uses the YouTube Data API to search for educational videos related to an academic topic.

Returned information can include:

Video title.

Channel name.

Publication date.

Thumbnail.

Description.

YouTube URL.

Number of search results returned.

This provides additional learning resources outside the internal PDF knowledge base.

📌 6. Saved Notes

Users can save useful AI-generated answers for later revision.

Features include:

Save an answer.

Search saved notes.

Open a complete saved note.

View source references.

View saved date.

Remove notes when no longer required.

🔐 7. Firebase Authentication

StudyNova uses Firebase for user authentication and identity management.

Supported functions include:

User signup.

User login.

Password reset.

User identity through Firebase UID.

User profile information.

Logout.

User activity is linked to the logged-in user's UID so that records can be associated with the correct user.

📊 8. Study Dashboard

The dashboard provides a summary of the user's learning activity.

It can use activity information such as:

Questions asked.

Quiz activity.

Quiz performance.

Image-study activity.

YouTube searches.

Saved notes.

Recent activity.

Study progress.

📋 9. Dataset & Analysis

The Dataset page combines activity information from the application's JSON storage files into one structured Pandas DataFrame.

The current project collects data from:

users.json

chat_history.json

favourites.json

quiz_history.json

image_study_history.json

youtube_history.json

activity_history.json

The dataset page supports:

Complete multi-user activity records.

Consistent dataset columns.

Activity-type information.

User information.

Quiz information.

Image information.

YouTube information.

Derived data-science fields.

Consistent missing-value handling.

Excel dataset download.

The dataset is prepared for future data-analysis and machine-learning work.

🔌 APIs Used in the Project

StudyNova uses five main API credentials/configurations.

1. MAIN_CHAT_API_KEY_1

Used for: Main academic chatbot.

Purpose: Sends the user question and retrieved academic context to Gemini to generate the final answer.

Data provided/used:

User question.

Retrieved document context.

Prompt instructions.

Processing:

The RAG pipeline first retrieves relevant document chunks using vector similarity search. The retrieved information is then combined with the user's question and sent to the Gemini model.

2. MAIN_CHAT_API_KEY_2

Used for: Main academic chatbot as the second configured Gemini API credential.

Purpose: Provides an additional configured Gemini key for the main chat generation flow.

The application can use the configured Gemini credentials as part of its chat-generation setup without changing the RAG workflow.

3. IMAGE_STUDY_API_KEY

Used for: Image Study Assistant.

Purpose: Sends an uploaded image and the user's instruction to a Gemini multimodal model.

Data provided:

Image bytes.

Image MIME type.

User instruction.

Returned data:

A text-based academic explanation generated from the visible image content.

4. YOUTUBE_DATA_API_KEY

Used for: YouTube Learning Resources.

Purpose: Searches educational videos related to the entered academic topic.

Returned data can include:

Video title.

Channel.

Publication date.

Thumbnail.

Description.

Video URL.

The returned search information is displayed as learning resources and search activity can also be recorded in the project dataset.

5. FIREBASE_API_KEY

Used for: Firebase Authentication.

Purpose: Supports email/password authentication operations through Firebase Authentication APIs.

Used for operations such as:

Signup.

Login.

Password reset.

User identity.

Firebase UID is used to connect activity data to the correct user.

Security note: API keys, Firebase service-account credentials, .env, and other secrets must not be committed to GitHub. Use .gitignore locally and Streamlit Secrets or environment variables for deployment.

🧠 AI and RAG Architecture

The main chatbot uses the following flow:

Academic PDF Notes
       ↓
Document Loading
       ↓
Text Extraction
       ↓
Text Chunking
       ↓
Sentence Transformer Embeddings
       ↓
FAISS Vector Store
       ↓
User Question
       ↓
Similarity Search
       ↓
Relevant Context
       ↓
Prompt Construction
       ↓
Gemini LLM
       ↓
Final Student-Friendly Answer
       ↓
Source References

For uploaded PDFs, a similar process is performed dynamically for the user's selected documents.

🔍 FAISS Vector Search

FAISS is used to store and search vector embeddings.

The academic PDF text is converted into numerical vectors using a Sentence Transformer embedding model. FAISS then performs similarity search to identify the most relevant chunks for a user's question.

This helps the LLM receive useful context instead of depending only on general model knowledge.

🧩 LangChain

LangChain is used as part of the document and RAG workflow.

It helps connect document processing, chunking, embeddings, retrieval, and LLM-based response generation into an application workflow.

🤖 Google Gemini

Google Gemini is the main generative AI service used in StudyNova.

It is used for:

Academic question answering.

RAG response generation.

Image understanding.

Quiz generation.

Student-friendly explanations.

The model receives the appropriate input and context for each feature and returns generated content to the Streamlit interface.

🔊 Text-to-Speech

The chatbot can convert generated answers into speech using the gTTS library.

This allows students to listen to an AI-generated answer instead of reading it only as text.

📥 PDF Export

The chat module can generate a PDF file containing the conversation.

The application uses the ReportLab library for PDF generation.

This can be useful for:

Offline study.

Revision.

Printing.

Saving conversations.

💬 Chat History

Chat conversations are stored locally in JSON format and displayed in the application's sidebar.

The stored information allows users to revisit previous discussions and continue their study sessions.

The project also keeps separate activity records for dataset and progress tracking.

📌 Activity and Data Tracking

StudyNova records activity related to different features.

Examples include:

Chat questions.

Quiz results.

Image-study activities.

YouTube searches.

Saved notes.

User account information.

The activity information is associated with the logged-in user's Firebase UID.

The project uses JSON storage for local project data and can also use Firebase/Firestore for user-specific statistics and activity information.

📊 Dataset Creation and Data Science Preparation

The project contains seven main JSON activity sources:

storage/
├── users.json
├── chat_history.json
├── favourites.json
├── quiz_history.json
├── image_study_history.json
├── youtube_history.json
└── activity_history.json

A dataset manager reads these files, normalizes the records, extracts useful fields, handles missing values, and creates a combined Pandas DataFrame.

The dataset includes fields such as:

User UID.

User name.

User email.

Activity type.

Date.

Topic.

Question.

Answer.

Quiz difficulty.

Quiz score.

Percentage.

Image name.

YouTube result count.

Chat message count.

Derived text lengths.

Activity flags.

Missing text values are normalized to Not Applicable and numeric values are normalized to suitable numeric values so the dataset is easier to use for further analysis.

The Dataset page can export the combined activity data as an Excel workbook.

📂 Project Structure

AcademicNotesAI/
│
├── app.py
├── rag.py
├── ingest.py
├── image_processor.py
├── pdf_processor.py
├── pdf_export.py
├── speech.py
├── speech_to_text.py
├── youtube_service.py
├── quiz_generator.py
├── firebase_manager.py
├── progress_manager.py
├── chat_history_manager.py
├── favourites_manager.py
├── requirements.txt
├── README.md
├── .env                  # Local only - do not upload
├── .gitignore
│
├── css/
│   └── style.css
│
├── data/
│   └── (Academic PDF Notes)
│
├── data_science/
│   └── dataset_manager.py
│
├── pages/
│   ├── Chatbot.py
│   ├── Dashboard.py
│   ├── Dataset.py
│   ├── FavouriteNotes.py
│   ├── ImageStudy.py
│   ├── Login.py
│   ├── Quiz.py
│   ├── Signup.py
│   └── YouTubeResources.py
│
├── storage/
│   ├── users.json
│   ├── chat_history.json
│   ├── favourites.json
│   ├── quiz_history.json
│   ├── image_study_history.json
│   ├── youtube_history.json
│   └── activity_history.json
│
├── vectorstore/
│   ├── index.faiss
│   └── index.pkl
│
├── combine_json_to_csv.py
│
├── test_rag.py              # Optional local testing file
├── test_firebase.py         # Optional local testing file
├── test_sppech_to_text.py   # Optional local testing file
│
└── venv/                    # Local virtual environment - not uploaded

Generated files, secrets, credentials, virtual environments, and other local-only files should be excluded from GitHub using .gitignore.

⚙️ Complete Project Workflow

Academic Notes Mode

Academic PDFs are stored in the project.

PDF content is extracted.

Text is divided into chunks.

Embeddings are generated.

Embeddings are stored in FAISS.

The user enters a question.

The system performs similarity search.

Relevant chunks are retrieved.

The context is sent to Gemini.

Gemini generates the final answer.

Source documents are displayed.

The user can save, listen to, regenerate, or export the answer.

Own PDF Mode

User uploads a PDF.

Text is extracted.

Chunks are created.

Embeddings are generated.

A temporary FAISS vector store is created.

User asks a question.

Relevant chunks are retrieved.

Gemini generates the answer.

The answer is displayed with relevant source information.

Image Study Mode

User uploads an image.

User enters an instruction.

Image data is sent to the image-study Gemini service.

Gemini analyzes the visible academic content.

The answer is displayed in student-friendly language.

The image-study activity is recorded once per successful analysis.

Quiz Mode

User selects a topic.

User selects question count.

User selects difficulty.

Gemini generates the quiz.

User answers the questions.

The application calculates the score.

Quiz result is stored for progress and dataset tracking.

YouTube Mode

User enters an academic topic.

The YouTube Data API is called.

Educational video results are returned.

The resources are displayed.

The search activity is recorded.

🚀 Installation

1. Clone the repository

git clone https://github.com/pawarpayal09/AcademicNotesAI.git
cd AcademicNotesAI

2. Create a virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

🔑 Environment Variables and Secrets

For local development, create a .env file containing the required project secrets.

A typical configuration includes:

MAIN_CHAT_API_KEY_1=YOUR_GEMINI_API_KEY_1
MAIN_CHAT_API_KEY_2=YOUR_GEMINI_API_KEY_2
IMAGE_STUDY_API_KEY=YOUR_IMAGE_STUDY_API_KEY
YOUTUBE_DATA_API_KEY=YOUR_YOUTUBE_DATA_API_KEY
FIREBASE_API_KEY=YOUR_FIREBASE_API_KEY

Depending on the Firebase configuration, the local project may also require the Firebase service-account information used by the Firebase Admin SDK.

Never upload real keys or service-account credentials to GitHub.

For Streamlit Cloud, configure secrets through the Streamlit app's Secrets settings instead of committing secrets to the repository.

▶️ Run the Project

Start the application using:

streamlit run app.py

The application opens in the browser through Streamlit.

📌 How to Use StudyNova

Start the Streamlit application.

Create an account or log in.

Use the Academic Notes chatbot or select your required learning feature.

Ask questions from academic notes.

Upload your own PDF when required.

Use Image Study for visual academic material.

Generate quizzes for practice.

Search YouTube resources for additional learning.

Save important AI answers.

Open Dashboard to view learning progress.

Open Dataset to view activity data.

Download the fused dataset as Excel when required.

🖥️ Main Application Pages

Page

Purpose

app.py

StudyNova home page and project entry point

Chatbot.py

Academic Notes and uploaded PDF chatbot

Dashboard.py

Personal study progress and activity dashboard

Dataset.py

Combined multi-user activity dataset

FavouriteNotes.py

Saved AI answers and revision notes

ImageStudy.py

Image-based academic study assistant

Login.py

Firebase login

Signup.py

Firebase signup

Quiz.py

AI-generated academic quizzes

YouTubeResources.py

Educational YouTube search

🔐 User Data and Privacy

The application connects activity data with the authenticated user's Firebase UID.

Examples of stored activity information include:

User identity information.

Questions asked.

Quiz results.

Image-study instructions.

YouTube searches.

Saved-note activity.

General activity records.

Local JSON data is intended for the project environment. When the application is deployed, secrets and credentials must be configured securely.

📈 Data Science and Analysis Use

The project now provides a structured activity dataset that can be used for future data-science work.

Possible analysis includes:

User activity distribution.

Most studied topics.

Quiz performance analysis.

Learning activity by day or time.

Feature usage patterns.

User engagement analysis.

Activity-type classification.

Topic clustering.

Predictive modelling based on future project requirements.

The current dataset is generated from the real activity created while using StudyNova rather than from a separate student-performance project.

🧪 Testing Files

The project may contain separate local testing files for individual components, such as:

test_rag.py

test_firebase.py

test_sppech_to_text.py

These are intended for testing individual functionality and are not required for the main application's runtime flow when their functionality is already integrated into the corresponding modules.

🚀 Deployment

The application can be deployed using Streamlit Cloud.

General deployment steps:

Push the project to GitHub.

Connect the GitHub repository to Streamlit Cloud.

Select app.py as the main file.

Add required secrets in Streamlit Cloud.

Confirm requirements.txt contains the required dependencies.

Deploy the application.

Do not commit:

.env
firebase_service_account.json
service-account credentials
venv/
private keys
other secret files

🧩 Future Enhancements

Possible future improvements include:

🎤 Improved voice interaction.

🌐 Multi-language learning support.

🧠 More advanced quiz and practice modes.

🏷️ Better note categories and tags.

📱 Mobile application.

☁️ Expanded cloud storage.

📈 More advanced data-science analysis.

🤖 A dedicated project-specific API for academic learning data or services.

🔎 More advanced personalized study recommendations.

👩‍💻 Developer

Payal Pramod Pawar
Master of Computer Applications (MCA)

StudyNova / Academic Notes AI

Developed as an academic and educational AI project.

🙏 Acknowledgements

This project uses and integrates technologies and services including:

Google Gemini

LangChain

Hugging Face Sentence Transformers

FAISS

Firebase

YouTube Data API

Streamlit

Pandas

OpenPyXL

ReportLab

gTTS

PyPDF

📄 License

This project is developed for educational and academic purposes.

If this repository is reused or extended, please provide appropriate credit to the original project and developer.