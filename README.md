# 🧑‍🎓 StudyNova – Intelligent Academic Learning Assistant

StudyNova is an AI-powered academic learning application developed for students. The project started as an Academic Notes AI chatbot and has been expanded into a complete study assistant with RAG-based question answering, PDF learning, image study, quiz generation, YouTube learning resources, saved notes, Firebase authentication, dashboard tracking, data analysis, and machine learning.

The GitHub repository/project name remains **AcademicNotesAI**, while the application is branded as **StudyNova**.

---

# 📖 Project Overview

StudyNova helps students understand academic content faster by combining Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), vector search, document processing, external APIs, data analysis, and machine learning.

The application can:

* Answer questions from academic PDF notes.
* Allow users to upload and chat with their own PDF files.
* Analyze academic images, diagrams, screenshots, and study material.
* Generate multiple-choice quizzes from academic topics.
* Search educational YouTube resources.
* Save important AI answers for later revision.
* Keep chat history and learning activity records.
* Provide Firebase-based user authentication.
* Show personalized dashboard information.
* Maintain a combined dataset of user activities from multiple JSON files.
* Display the complete multi-user activity dataset in the Dataset page.
* Download the fused dataset as an Excel file for further analysis.
* Perform exploratory data analysis on the fused dataset.
* Apply machine learning classification algorithms to activity data.
* Apply regression algorithms for exploratory continuous-value prediction.
* Provide an interactive ML Insights page for model comparison and prediction.

---

# 🎯 Objectives

The main objectives of StudyNova are:

* Build an AI-based academic learning assistant.
* Provide context-based answers from academic documents.
* Reduce the time required to search through long study materials.
* Demonstrate the practical use of LLM and RAG technologies.
* Provide multiple learning tools in one application.
* Track student learning activities for dashboard and data-analysis purposes.
* Prepare structured project activity data for data-science and machine-learning work.
* Apply machine learning algorithms to the generated activity dataset.
* Compare different classification and regression algorithms.
* Provide an interactive interface for viewing ML results and making predictions.
* Provide a simple and student-friendly interface for academic use.

---

# ❓ Problem Statement

Students often spend a lot of time searching through lengthy PDF notes, books, research papers, and other study material to find specific information.

StudyNova solves this problem by allowing students to ask questions in natural language and receive answers based on relevant academic content.

The system also supports visual learning, practice quizzes, video resources, saved answers, progress tracking, data analysis, and machine-learning-based activity analysis.

---

# ✨ Main Features

## 📚 1. Academic Notes Chatbot

Students can ask questions from the academic PDF notes available in the project.

Features include:

* Semantic search over academic documents.
* RAG-based context retrieval.
* Gemini-generated answers.
* Source document references.
* Student-friendly explanations.
* Chat history.
* Regenerate answer option.
* Feedback option.
* Text-to-Speech for answers.
* PDF export of conversations.

---

## 📄 2. Upload and Chat with Your Own PDF

Users can upload their own academic PDF files and ask questions from them.

The system:

1. Loads the PDF.
2. Extracts the text.
3. Splits the document into smaller chunks.
4. Generates embeddings.
5. Creates a FAISS vector store.
6. Searches the most relevant chunks.
7. Sends the retrieved context to Gemini.
8. Generates the final answer.

This can be used for:

* Notes
* Textbooks
* Assignments
* Research papers
* Other academic documents

---

## 🖼️ 3. Image Study Assistant

Users can upload study images and ask AI to understand the content.

Supported examples include:

* Textbook pages
* Handwritten notes
* Diagrams
* Charts
* Tables
* Questions
* Programming code screenshots
* Academic screenshots

The user can ask the system to:

* Explain the topic.
* Summarize the notes.
* Extract important points.
* Explain a diagram.
* Solve a question step-by-step.

---

## 🧠 4. Automatic Quiz Generator

The Quiz module creates AI-generated multiple-choice questions from an academic topic.

Available settings:

* Easy difficulty
* Medium difficulty
* Hard difficulty
* 5 questions
* 10 questions
* 15 questions

The module calculates:

* Score
* Accuracy/percentage
* Correct answers
* Wrong answers
* Answer explanations

Quiz activity is also stored for dashboard and dataset analysis.

---

## 🎥 5. YouTube Learning Resources

The application uses the YouTube Data API to search for educational videos related to an academic topic.

Returned information can include:

* Video title
* Channel name
* Publication date
* Thumbnail
* Description
* YouTube URL
* Number of search results returned

This provides additional learning resources outside the internal PDF knowledge base.

---

## 📌 6. Saved Notes

Users can save useful AI-generated answers for later revision.

Features include:

* Save an answer.
* Search saved notes.
* Open a complete saved note.
* View source references.
* View saved date.
* Remove notes when no longer required.

---

## 🔐 7. Firebase Authentication

StudyNova uses Firebase for user authentication and identity management.

Supported functions include:

* User signup.
* User login.
* Password reset.
* User identity through Firebase UID.
* User profile information.
* Logout.

User activity is linked to the logged-in user's UID so that records can be associated with the correct user.

---

## 📊 8. Study Dashboard

The dashboard provides a summary of learning activity.

It can use activity information such as:

* Questions asked.
* Quiz activity.
* Quiz performance.
* Image-study activity.
* YouTube searches.
* Saved notes.
* Recent activity.
* Study progress.

---

# 📋 9. Dataset & Data Analysis

The Dataset page combines activity information from the application's JSON storage files into one structured Pandas DataFrame.

The current project collects data from:

```text
users.json
chat_history.json
favourites.json
quiz_history.json
image_study_history.json
youtube_history.json
activity_history.json
```

The dataset page supports:

* Complete multi-user activity records.
* Consistent dataset columns.
* Activity-type information.
* User information.
* Quiz information.
* Image information.
* YouTube information.
* Derived data-science fields.
* Missing-value handling.
* Excel dataset download.

The fused dataset is then used for:

* Data quality analysis.
* Exploratory data analysis.
* Data visualization.
* Machine learning classification.
* Machine learning regression.
* Activity prediction.

---

# 🤖 10. Machine Learning Module

StudyNova has been extended with a dedicated machine learning module using the fused application activity dataset.

The ML module is designed to analyze user activity patterns and demonstrate the practical application of supervised machine learning algorithms.

The ML implementation is located inside:

```text
ml_module/
```

The module contains:

* Data preprocessing.
* Classification.
* Classification evaluation.
* Regression.
* Prediction.
* Saved machine learning models.
* Evaluation results.
* Visualization outputs.

---

# 🧠 Machine Learning Objective

The main classification objective is to predict the type of activity performed in StudyNova.

The classification target is:

```text
activity_type
```

Examples of activity types include:

* chat
* quiz
* image
* youtube
* saved_note
* user

The regression component demonstrates continuous-value prediction using:

```text
activity_hour
```

The regression target is used as an exploratory academic ML target because the current fused dataset contains only a small number of valid quiz percentage values.

Therefore, regression results should be interpreted as an ML demonstration on the current activity dataset rather than as a production prediction system.

---

# 📊 ML Dataset

The current fused StudyNova dataset contains:

```text
Records    : 60
Attributes : 40
```

The dataset combines records from different application activity sources.

Current record types include:

* chat_history
* youtube_history
* image_study_history
* favourites
* users
* quiz_history
* activity_history

The fused dataset is stored as:

```text
ml_module/data/StudyNova_Fused_Dataset.xlsx
```

---

# 🔎 Classification Features

The classification model uses activity-related numerical and derived features.

The current classification features are:

```text
activity_hour
question_length
answer_length
instruction_length
description_length
results_count
message_count
has_question
has_answer
has_source
has_instruction
```

The target variable is:

```text
activity_type
```

---

# 🛡️ Data Leakage Prevention

Some columns directly identify the activity type and therefore should not be used as classification features.

The following fields are excluded from the classification model:

```text
is_chat
is_quiz
is_image
is_youtube
is_saved_note
is_user_record
record_type
source_file
```

These columns can reveal the target activity type directly and may result in data leakage.

Therefore, the ML module uses activity-related behavioral and derived features instead.

---

# 🤖 Classification Algorithms

The project implements five classification algorithms.

## 1. Logistic Regression

Logistic Regression is used as a simple and interpretable classification model.

It predicts the probability of an input belonging to a particular activity class.

---

## 2. Naive Bayes

Gaussian Naive Bayes is used as a probabilistic classification algorithm.

It estimates the probability of each activity class based on the available features.

---

## 3. Decision Tree

Decision Tree Classifier uses a tree-like structure to make classification decisions.

The model splits the data based on feature conditions and reaches a final activity class.

---

## 4. Random Forest

Random Forest combines multiple decision trees to make a more robust classification prediction.

The project uses:

```text
n_estimators = 100
max_depth = 8
class_weight = balanced
```

Random Forest feature importance is also analyzed to identify which input features contribute most to the model's decisions.

---

## 5. Support Vector Machine

Support Vector Machine (SVM) is used for classification using a non-linear RBF kernel.

Feature scaling is applied before the SVM model.

---

# 🔄 Classification Evaluation

Because the dataset is relatively small and the smallest activity classes contain only a few records, the project uses:

```text
4-Fold Stratified Cross-Validation
```

The same folds are used to compare the classification models.

The evaluation metrics include:

* Accuracy
* Precision
* Recall
* F1-score
* Training accuracy

Weighted averaging is used for precision, recall, and F1-score.

---

# 📈 Classification Results

The current experimental results obtained from the 60-record fused dataset are:

| Model               | Accuracy | Precision | Recall | F1-score |
| ------------------- | -------: | --------: | -----: | -------: |
| Logistic Regression |   0.9167 |    0.8938 | 0.9167 |   0.9033 |
| Naive Bayes         |   0.9167 |    0.8917 | 0.9167 |   0.9000 |
| Decision Tree       |   0.9167 |    0.8972 | 0.9167 |   0.8994 |
| Random Forest       |   0.8667 |    0.8750 | 0.8667 |   0.8688 |
| SVM                 |   0.9000 |    0.8542 | 0.9000 |   0.8733 |

Based on mean F1-score, Logistic Regression currently has the highest score among the tested models.

However, because the dataset contains only 60 records and has an uneven class distribution, the results should be considered exploratory rather than production-grade.

---

# 📊 Classification Diagnostic Analysis

The project generates additional diagnostic outputs for the classification models.

These include:

* Confusion matrices.
* Classification reports.
* Model comparison visualization.
* Random Forest feature importance.
* Overfitting analysis.
* Out-of-fold predictions.

The generated files are stored in:

```text
ml_module/results/
```

---

# 🔲 Confusion Matrix

A confusion matrix is generated for each classification algorithm.

The project generates:

```text
logistic_regression_confusion_matrix.png
naive_bayes_confusion_matrix.png
decision_tree_confusion_matrix.png
random_forest_confusion_matrix.png
svm_confusion_matrix.png
```

A confusion matrix helps compare:

* Actual activity types.
* Predicted activity types.
* Correct predictions.
* Incorrect predictions.

---

# 🌲 Random Forest Feature Importance

The project also calculates Random Forest feature importance.

This provides a descriptive view of which input features were more influential for the Random Forest model.

The results are saved as:

```text
random_forest_feature_importance.csv
```

A visualization is also generated for easier interpretation.

Feature importance should be interpreted as a model-specific measure and not as proof of causal relationships.

---

# ⚠️ Overfitting Analysis

The classification module compares training performance with cross-validation performance.

For example, Random Forest achieved a higher training accuracy than its cross-validation accuracy.

This difference can indicate possible overfitting.

However, because the dataset contains only 60 records, the observed difference should be interpreted cautiously.

The overfitting analysis is saved as:

```text
overfitting_analysis.csv
```

---

# 📉 Regression Module

The project also contains a regression module.

The regression target is:

```text
activity_hour
```

The regression target represents the hour associated with the activity record.

The regression module is mainly included to demonstrate different regression techniques on the fused activity dataset.

---

# 📐 Regression Features

The regression models use:

```text
question_length
answer_length
instruction_length
description_length
results_count
message_count
has_question
has_answer
has_source
has_instruction
```

The target is:

```text
activity_hour
```

Date and timestamp fields are not used as predictors because they would directly reveal the target hour.

---

# 🤖 Regression Algorithms

The project implements three regression algorithms.

## 1. Simple Linear Regression

Simple Linear Regression demonstrates the relationship between a single input feature and the continuous target.

It is useful for understanding the basic concept of linear prediction.

---

## 2. Multiple Linear Regression

Multiple Linear Regression uses multiple input features to predict the continuous target.

The model considers several activity-related attributes simultaneously.

---

## 3. Polynomial Regression

Polynomial Regression extends the linear relationship by adding polynomial terms.

The current implementation uses:

```text
Polynomial Degree = 2
```

This allows the model to represent simple non-linear relationships between the input features and the target.

---

# 📊 Regression Evaluation

The regression models are evaluated using:

* MAE – Mean Absolute Error
* MSE – Mean Squared Error
* RMSE – Root Mean Squared Error
* R² – R-squared

The regression results are saved in:

```text
ml_module/results/regression_results.csv
```

---

# ⚠️ Regression Dataset Limitation

The current fused dataset contains only four records with non-zero quiz percentages.

Therefore, using `percentage` as a regression target would not provide a meaningful regression experiment with the current dataset.

For this reason, `activity_hour` is used as an exploratory continuous target for demonstrating the required regression algorithms.

Future versions can use a larger dataset with more meaningful continuous academic or engagement measurements.

---

# 🔮 ML Prediction Module

The project includes a prediction module that loads the trained classification models and predicts the activity type for new input data.

The prediction module is:

```text
ml_module/prediction.py
```

It supports:

```text
Logistic Regression
Naive Bayes
Decision Tree
Random Forest
SVM
```

The prediction process is:

```text
User Input
     ↓
Feature Preparation
     ↓
Load Saved ML Model
     ↓
Model Prediction
     ↓
Predicted Activity Type
```

The models are saved as `.pkl` files using Joblib.

---

# 📦 Saved ML Models

The classification models are stored in:

```text
ml_module/models/
```

Files include:

```text
logistic_regression.pkl
naive_bayes.pkl
decision_tree.pkl
random_forest.pkl
svm.pkl
```

The regression models are:

```text
simple_linear_regression.pkl
multiple_linear_regression.pkl
polynomial_regression.pkl
```

These saved models allow the Streamlit application to load trained models instead of retraining them every time the application starts.

---

# 🖥️ ML Insights Page

StudyNova contains a dedicated:

```text
pages/MLInsights.py
```

page for interacting with the machine learning module.

The ML Insights page provides four major sections.

## Classification

Displays:

* Classification model comparison.
* Accuracy.
* Precision.
* Recall.
* F1-score.
* Model comparison graph.
* Confusion matrix.
* Random Forest feature importance.

## Regression

Displays:

* Regression model results.
* MAE.
* MSE.
* RMSE.
* R².
* Explanation of the regression target.

## Prediction

Allows the user to enter activity-related feature values and select a trained classification model.

The application then predicts the activity type.

## ML Information

Provides an explanation of:

* Classification.
* Regression.
* Evaluation metrics.
* Dataset limitations.
* ML workflow.

---

# 🔄 Complete Machine Learning Workflow

The ML workflow is:

```text
StudyNova Application
        ↓
User Activity
        ↓
JSON Activity Sources
        ↓
Data Fusion
        ↓
Pandas DataFrame
        ↓
Excel Fused Dataset
        ↓
Data Preprocessing
        ↓
Feature Selection
        ↓
Leakage Prevention
        ↓
Classification / Regression
        ↓
Cross-Validation
        ↓
Model Evaluation
        ↓
Visualization & Diagnostics
        ↓
Save Trained Models
        ↓
Streamlit ML Insights
        ↓
New Input Prediction
```

---

# 🧩 ML Project Structure

The machine learning part of the project is organized as follows:

```text
ml_module/
│
├── __init__.py
├── preprocessing.py
├── classification.py
├── classification_analysis.py
├── prediction.py
├── regression.py
│
├── data/
│   └── StudyNova_Fused_Dataset.xlsx
│
├── models/
│   ├── logistic_regression.pkl
│   ├── naive_bayes.pkl
│   ├── decision_tree.pkl
│   ├── random_forest.pkl
│   ├── svm.pkl
│   ├── simple_linear_regression.pkl
│   ├── multiple_linear_regression.pkl
│   └── polynomial_regression.pkl
│
└── results/
    ├── classification_results.csv
    ├── classification_diagnostic_summary.csv
    ├── overfitting_analysis.csv
    ├── random_forest_feature_importance.csv
    ├── model_comparison.png
    ├── logistic_regression_confusion_matrix.png
    ├── naive_bayes_confusion_matrix.png
    ├── decision_tree_confusion_matrix.png
    ├── random_forest_confusion_matrix.png
    ├── svm_confusion_matrix.png
    └── regression_results.csv
```

---

# 🔌 APIs Used in the Project

StudyNova uses five main API credentials/configurations.

## 1. MAIN_CHAT_API_KEY_1

Used for:

**Main academic chatbot**

Purpose:

Sends the user question and retrieved academic context to Gemini to generate the final answer.

Data provided/used:

* User question.
* Retrieved document context.
* Prompt instructions.

Processing:

The RAG pipeline first retrieves relevant document chunks using vector similarity search. The retrieved information is then combined with the user's question and sent to the Gemini model.

---

## 2. MAIN_CHAT_API_KEY_2

Used for:

**Main academic chatbot as the second configured Gemini API credential.**

Purpose:

Provides an additional configured Gemini key for the main chat generation flow.

The application can use the configured Gemini credentials as part of its chat-generation setup without changing the RAG workflow.

---

## 3. IMAGE_STUDY_API_KEY

Used for:

**Image Study Assistant**

Purpose:

Sends an uploaded image and the user's instruction to a Gemini multimodal model.

Data provided:

* Image bytes.
* Image MIME type.
* User instruction.

Returned data:

A text-based academic explanation generated from the visible image content.

---

## 4. YOUTUBE_DATA_API_KEY

Used for:

**YouTube Learning Resources**

Purpose:

Searches educational videos related to the entered academic topic.

Returned data can include:

* Video title.
* Channel.
* Publication date.
* Thumbnail.
* Description.
* Video URL.

The returned search information is displayed as learning resources and search activity can also be recorded in the project dataset.

---

## 5. FIREBASE_API_KEY

Used for:

**Firebase Authentication**

Purpose:

Supports email/password authentication operations through Firebase Authentication APIs.

Used for operations such as:

* Signup.
* Login.
* Password reset.
* User identity.

Firebase UID is used to connect activity data to the correct user.

---

## 🔐 Security Note

API keys, Firebase service-account credentials, `.env`, and other secrets must not be committed to GitHub.

Use:

* `.gitignore` for local development.
* Environment variables where appropriate.
* Streamlit Secrets for Streamlit Cloud deployment.

---

# 🧠 AI and RAG Architecture

The main chatbot uses the following flow:

```text
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
```

For uploaded PDFs, a similar process is performed dynamically for the user's selected documents.

---

# 🔍 FAISS Vector Search

FAISS is used to store and search vector embeddings.

The academic PDF text is converted into numerical vectors using a Sentence Transformer embedding model.

FAISS then performs similarity search to identify the most relevant chunks for a user's question.

This helps the LLM receive useful context instead of depending only on general model knowledge.

---

# 🧩 LangChain

LangChain is used as part of the document and RAG workflow.

It helps connect:

* Document processing.
* Chunking.
* Embeddings.
* Retrieval.
* LLM-based response generation.

---

# 🤖 Google Gemini

Google Gemini is the main generative AI service used in StudyNova.

It is used for:

* Academic question answering.
* RAG response generation.
* Image understanding.
* Quiz generation.
* Student-friendly explanations.

The model receives the appropriate input and context for each feature and returns generated content to the Streamlit interface.

---

# 🔊 Text-to-Speech

The chatbot can convert generated answers into speech using the gTTS library.

This allows students to listen to an AI-generated answer instead of reading it only as text.

---

# 📥 PDF Export

The chat module can generate a PDF file containing the conversation.

The application uses the ReportLab library for PDF generation.

This can be useful for:

* Offline study.
* Revision.
* Printing.
* Saving conversations.

---

# 💬 Chat History

Chat conversations are stored locally in JSON format and displayed in the application's sidebar.

The stored information allows users to revisit previous discussions and continue their study sessions.

The project also keeps separate activity records for dataset and progress tracking.

---

# 📌 Activity and Data Tracking

StudyNova records activity related to different features.

Examples include:

* Chat questions.
* Quiz results.
* Image-study activities.
* YouTube searches.
* Saved notes.
* User account information.

The activity information is associated with the logged-in user's Firebase UID.

The project uses JSON storage for local project data and can also use Firebase/Firestore for user-specific statistics and activity information.

---

# 📊 Dataset Creation and Data Science Preparation

The project contains seven main JSON activity sources:

```text
storage/
├── users.json
├── chat_history.json
├── favourites.json
├── quiz_history.json
├── image_study_history.json
├── youtube_history.json
└── activity_history.json
```

A dataset manager reads these files, normalizes the records, extracts useful fields, handles missing values, and creates a combined Pandas DataFrame.

The dataset includes fields such as:

* User UID.
* User name.
* User email.
* Activity type.
* Date.
* Topic.
* Question.
* Answer.
* Quiz difficulty.
* Quiz score.
* Percentage.
* Image name.
* YouTube result count.
* Chat message count.
* Derived text lengths.
* Activity flags.

Missing text values are normalized to `Not Applicable` and numeric values are normalized to suitable numeric values so the dataset is easier to use for further analysis.

The Dataset page can export the combined activity data as an Excel workbook.

---

# 📂 Project Structure

```text
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
├── ml_module/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── classification.py
│   ├── classification_analysis.py
│   ├── prediction.py
│   ├── regression.py
│   │
│   ├── data/
│   │   └── StudyNova_Fused_Dataset.xlsx
│   │
│   ├── models/
│   │   ├── logistic_regression.pkl
│   │   ├── naive_bayes.pkl
│   │   ├── decision_tree.pkl
│   │   ├── random_forest.pkl
│   │   ├── svm.pkl
│   │   ├── simple_linear_regression.pkl
│   │   ├── multiple_linear_regression.pkl
│   │   └── polynomial_regression.pkl
│   │
│   └── results/
│       ├── classification_results.csv
│       ├── classification_diagnostic_summary.csv
│       ├── overfitting_analysis.csv
│       ├── random_forest_feature_importance.csv
│       ├── model_comparison.png
│       ├── logistic_regression_confusion_matrix.png
│       ├── naive_bayes_confusion_matrix.png
│       ├── decision_tree_confusion_matrix.png
│       ├── random_forest_confusion_matrix.png
│       ├── svm_confusion_matrix.png
│       └── regression_results.csv
│
├── pages/
│   ├── Chatbot.py
│   ├── Dashboard.py
│   ├── Dataset.py
│   ├── FavouriteNotes.py
│   ├── ImageStudy.py
│   ├── Login.py
│   ├── MLInsights.py
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
```

Generated files, secrets, credentials, virtual environments, and other local-only files should be excluded from GitHub using `.gitignore`.

---

# ⚙️ Complete Project Workflow

## Academic Notes Mode

1. Academic PDFs are stored in the project.
2. PDF content is extracted.
3. Text is divided into chunks.
4. Embeddings are generated.
5. Embeddings are stored in FAISS.
6. The user enters a question.
7. The system performs similarity search.
8. Relevant chunks are retrieved.
9. The context is sent to Gemini.
10. Gemini generates the final answer.
11. Source documents are displayed.
12. The user can save, listen to, regenerate, or export the answer.

---

## Own PDF Mode

1. User uploads a PDF.
2. Text is extracted.
3. Chunks are created.
4. Embeddings are generated.
5. A temporary FAISS vector store is created.
6. User asks a question.
7. Relevant chunks are retrieved.
8. Gemini generates the answer.
9. The answer is displayed with relevant source information.

---

## Image Study Mode

1. User uploads an image.
2. User enters an instruction.
3. Image data is sent to the image-study Gemini service.
4. Gemini analyzes the visible academic content.
5. The answer is displayed in student-friendly language.
6. The image-study activity is recorded once per successful analysis.

---

## Quiz Mode

1. User selects a topic.
2. User selects question count.
3. User selects difficulty.
4. Gemini generates the quiz.
5. User answers the questions.
6. The application calculates the score.
7. Quiz result is stored for progress and dataset tracking.

---

## YouTube Mode

1. User enters an academic topic.
2. The YouTube Data API is called.
3. Educational video results are returned.
4. The resources are displayed.
5. The search activity is recorded.

---

## Machine Learning Mode

1. StudyNova collects user activity.
2. Activity data is stored in JSON files.
3. Multiple JSON files are combined.
4. A fused dataset is created.
5. The dataset is exported to Excel.
6. The ML preprocessing module loads the dataset.
7. Features are selected.
8. Leakage-prone columns are removed.
9. Classification models are evaluated using cross-validation.
10. Regression models are evaluated using cross-validation.
11. Diagnostic visualizations are generated.
12. Final models are trained on the available dataset.
13. Models are saved using Joblib.
14. MLInsights loads the saved models and results.
15. Users can compare models and make new predictions.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/pawarpayal09/AcademicNotesAI.git
cd AcademicNotesAI
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

The requirements file includes dependencies for:

* Streamlit
* LangChain
* Google Gemini
* FAISS
* Sentence Transformers
* Hugging Face
* PyPDF
* Firebase
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* Joblib
* OpenPyXL
* Plotly
* Pillow
* ReportLab
* gTTS
* Speech Recognition
* Other application components

---

# 📦 Machine Learning Dependencies

The ML module uses the following important Python packages:

```text
pandas
numpy
scikit-learn
matplotlib
seaborn
openpyxl
joblib
```

These packages are already included in the project's `requirements.txt`.

---

# 🔑 Environment Variables and Secrets

For local development, create a `.env` file containing the required project secrets.

A typical configuration includes:

```env
MAIN_CHAT_API_KEY_1=YOUR_GEMINI_API_KEY_1
MAIN_CHAT_API_KEY_2=YOUR_GEMINI_API_KEY_2
IMAGE_STUDY_API_KEY=YOUR_IMAGE_STUDY_API_KEY
YOUTUBE_DATA_API_KEY=YOUR_YOUTUBE_DATA_API_KEY
FIREBASE_API_KEY=YOUR_FIREBASE_API_KEY
```

Depending on the Firebase configuration, the local project may also require the Firebase service-account information used by the Firebase Admin SDK.

Never upload real keys or service-account credentials to GitHub.

For Streamlit Cloud, configure secrets through the Streamlit app's Secrets settings instead of committing secrets to the repository.

---

# ▶️ Run the Project

Start the application using:

```bash
streamlit run app.py
```

The application opens in the browser through Streamlit.

---

# 📌 How to Use StudyNova

1. Start the Streamlit application.
2. Create an account or log in.
3. Use the Academic Notes chatbot or select the required learning feature.
4. Ask questions from academic notes.
5. Upload your own PDF when required.
6. Use Image Study for visual academic material.
7. Generate quizzes for practice.
8. Search YouTube resources for additional learning.
9. Save important AI answers.
10. Open Dashboard to view learning progress.
11. Open Dataset to view activity data.
12. Open ML Insights to view machine learning results.
13. Compare classification and regression models.
14. Use the prediction section to predict activity type.
15. Download the fused dataset as Excel when required.

---

# 🖥️ Main Application Pages

| Page                  | Purpose                                             |
| --------------------- | --------------------------------------------------- |
| `app.py`              | StudyNova home page and project entry point         |
| `Chatbot.py`          | Academic Notes and uploaded PDF chatbot             |
| `Dashboard.py`        | Personal study progress and activity dashboard      |
| `Dataset.py`          | Combined multi-user activity dataset                |
| `FavouriteNotes.py`   | Saved AI answers and revision notes                 |
| `ImageStudy.py`       | Image-based academic study assistant                |
| `Login.py`            | Firebase login                                      |
| `Signup.py`           | Firebase signup                                     |
| `Quiz.py`             | AI-generated academic quizzes                       |
| `YouTubeResources.py` | Educational YouTube search                          |
| `MLInsights.py`       | Machine learning results, comparison and prediction |

---

# 🔐 User Data and Privacy

The application connects activity data with the authenticated user's Firebase UID.

Examples of stored activity information include:

* User identity information.
* Questions asked.
* Quiz results.
* Image-study instructions.
* YouTube searches.
* Saved-note activity.
* General activity records.

Local JSON data is intended for the project environment.

When the application is deployed, secrets and credentials must be configured securely.

For shared datasets or reports, personally identifiable information such as email addresses and Firebase UIDs should be handled carefully and masked where appropriate.

---

# 📈 Data Science and Machine Learning Use

The project provides a structured activity dataset that can be used for data-science and machine-learning work.

Possible analysis includes:

* User activity distribution.
* Most studied topics.
* Quiz performance analysis.
* Learning activity by day or time.
* Feature usage patterns.
* User engagement analysis.
* Activity-type classification.
* Feature importance analysis.
* Model comparison.
* Regression analysis.
* Predictive modelling.
* Future personalized study recommendations.

The current dataset is generated from activity created while using StudyNova rather than from a separate student-performance project.

---

# ⚠️ Machine Learning Limitations

The current ML implementation is intended primarily for academic and exploratory purposes.

Important limitations include:

* The current fused dataset contains only 60 records.
* Activity classes are not equally distributed.
* Some classes contain relatively few records.
* Small datasets can cause performance estimates to vary.
* Classification results should not be considered production-grade.
* Random Forest shows a noticeable difference between training and cross-validation performance.
* Regression using `activity_hour` is exploratory.
* The current dataset has too few non-zero quiz percentage records for meaningful percentage regression.
* More real-world StudyNova activity records would improve future ML experiments.

Future versions can use a larger and more balanced dataset for more reliable machine-learning evaluation.

---

# 🧪 Testing Files

The project may contain separate local testing files for individual components, such as:

```text
test_rag.py
test_firebase.py
test_sppech_to_text.py
```

These are intended for testing individual functionality and are not required for the main application's runtime flow when their functionality is already integrated into the corresponding modules.

---

# 🚀 Deployment

The application can be deployed using Streamlit Cloud.

General deployment steps:

1. Push the project to GitHub.
2. Connect the GitHub repository to Streamlit Cloud.
3. Select `app.py` as the main file.
4. Add required secrets in Streamlit Cloud.
5. Confirm `requirements.txt` contains the required dependencies.
6. Confirm the ML module and required model files are included.
7. Deploy the application.
8. Test all major application pages after deployment.

Do not commit:

```text
.env
firebase_service_account.json
service-account credentials
venv/
private keys
other secret files
```

---

# 🧩 Future Enhancements

Possible future improvements include:

* 🎤 Improved voice interaction.
* 🌐 Multi-language learning support.
* 🧠 More advanced quiz and practice modes.
* 🏷️ Better note categories and tags.
* 📱 Mobile application.
* ☁️ Expanded cloud storage.
* 📈 More advanced data-science analysis.
* 🤖 More advanced machine-learning models.
* 📊 Larger and more balanced activity dataset.
* 🎯 Personalized study recommendations.
* 🔎 Advanced student engagement analysis.
* 🧠 More explainable ML predictions.
* 📚 Personalized learning paths.
* 👩‍🎓 Student performance prediction using richer academic data.

---

# 👩‍💻 Developer

**Payal Pramod Pawar**

Master of Computer Applications (MCA)

**StudyNova / Academic Notes AI**

Developed as an academic and educational AI, data-analysis, and machine-learning project.

---

# 🙏 Acknowledgements

This project uses and integrates technologies and services including:

* Google Gemini
* LangChain
* Hugging Face Sentence Transformers
* FAISS
* Firebase
* YouTube Data API
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* Joblib
* OpenPyXL
* Plotly
* Pillow
* ReportLab
* gTTS
* PyPDF

---

# 📄 License

This project is developed for educational and academic purposes.

If this repository is reused or extended, please provide appropriate credit to the original project and developer.
