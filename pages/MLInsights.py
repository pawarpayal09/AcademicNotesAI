import os
import sys
import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ML_MODULE_DIR = BASE_DIR / "ml_module"

if str(ML_MODULE_DIR) not in sys.path:
    sys.path.append(str(ML_MODULE_DIR))


from prediction import (
    get_available_models,
    prepare_input,
    predict_activity
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Machine Learning Insights",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# FIREBASE / AUTHENTICATION
# ==========================================================

from firebase_manager import (
    require_login,
    is_authenticated,
    get_current_user,
    get_user_profile,
    logout_user,
)


# ==========================================================
# LOAD CSS
# ==========================================================

def load_css():

    css_path = Path(__file__).resolve().parent.parent / "css" / "style.css"

    if css_path.exists():

        try:

            with open(
                css_path,
                "r",
                encoding="utf-8"
            ) as file:

                st.markdown(
                    f"<style>{file.read()}</style>",
                    unsafe_allow_html=True
                )

        except Exception:
            pass


load_css()


# ==========================================================
# LOGIN REQUIRED
# ==========================================================

require_login()

# ==========================================================
# USER INFORMATION
# ==========================================================

user = get_current_user() or {}
profile = get_user_profile() or {}

user_name = (
    profile.get("name")
    or user.get("name")
    or "Student"
)

user_email = (
    profile.get("email")
    or user.get("email")
    or ""
)

# ==========================================================
# TOP-RIGHT PROFILE
# ==========================================================

if is_authenticated():

    spacer, profile_area = st.columns(
        [5.8, 1.8],
        gap="small"
    )

    with profile_area:

        with st.container(
            key="data_analysis_user_profile"
        ):

            st.markdown(
                f"""
                <div class="home-profile-name">
                    👤 {user_name}
                </div>

                <div class="home-profile-email">
                    {user_email}
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "🚪 Logout",
                key="data_analysis_logout",
                use_container_width=True
            ):

                logout_user()

                st.rerun()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        # 🧑‍🎓 StudyNova

        ### Learn Smarter with AI
        """
    )

    st.divider()

    st.info(
        """
### 🤖 About

An AI-powered academic assistant that helps students:

- 📚 Search academic notes
- 📄 Chat with uploaded PDFs
- 🖼️ Understand study images
- 🧠 Generate practice quizzes
- 🎥 Find educational YouTube resources
- 📌 Save important AI answers
- 📊 Track learning activity
- 📈 View personal study progress
"""
    )

    st.divider()

    st.markdown(
        "### 🚀 Technologies"
    )

    st.success(
        "🤖 Google Gemini"
    )

    st.success(
        "🦜 LangChain"
    )

    st.success(
        "📚 FAISS"
    )

    st.success(
        "🧠 RAG"
    )

    st.success(
        "🔥 Firebase"
    )

    st.success(
        "🎥 YouTube API"
    )

    st.success(
        "🐼 Pandas"
    )

    st.success(
        "🔢 NumPy"
    )

    st.success(
        "📊 Matplotlib"
    )

    st.success(
        "⚡ Streamlit"
    )

    st.divider()

    st.markdown(
        "### 👩‍💻 Developer"
    )

    st.info(
        """
**Payal Pawar**

🎓 MCA Student

**StudyNova**

Academic Notes AI

Version 1.0
"""
    )


# ============================================================
# PATHS
# ============================================================

RESULT_DIR = ML_MODULE_DIR / "results"
MODEL_DIR = ML_MODULE_DIR / "models"


CLASSIFICATION_RESULTS = (
    RESULT_DIR /
    "classification_results.csv"
)

REGRESSION_RESULTS = (
    RESULT_DIR /
    "regression_results.csv"
)


# ============================================================
# TITLE
# ============================================================

st.title("🤖 Machine Learning Insights")

st.write(
    """
    This page presents the machine learning analysis
    performed on the StudyNova fused dataset.

    The ML module includes classification, regression,
    model evaluation, visualization, and prediction.
    """
)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Classification",
    "📈 Regression",
    "🔮 Prediction",
    "📚 ML Information"
])


# ============================================================
# TAB 1 - CLASSIFICATION
# ============================================================

with tab1:

    st.header(
        "📊 Classification Analysis"
    )

    st.write(
        """
        Classification models predict the type of
        StudyNova activity using application activity
        features.
        """
    )


    # --------------------------------------------------------
    # MODEL PERFORMANCE
    # --------------------------------------------------------

    if CLASSIFICATION_RESULTS.exists():

        results_df = pd.read_csv(
            CLASSIFICATION_RESULTS
        )


        st.subheader(
            "📈 Classification Model Performance"
        )


        display_df = results_df[
            [
                "Model",
                "Accuracy_Mean",
                "Precision_Mean",
                "Recall_Mean",
                "F1_Mean"
            ]
        ].copy()


        display_df[
            "Accuracy_Mean"
        ] = (
            display_df[
                "Accuracy_Mean"
            ] * 100
        ).round(2)


        display_df[
            "Precision_Mean"
        ] = (
            display_df[
                "Precision_Mean"
            ] * 100
        ).round(2)


        display_df[
            "Recall_Mean"
        ] = (
            display_df[
                "Recall_Mean"
            ] * 100
        ).round(2)


        display_df[
            "F1_Mean"
        ] = (
            display_df[
                "F1_Mean"
            ] * 100
        ).round(2)


        display_df.columns = [
            "Model",
            "Accuracy (%)",
            "Precision (%)",
            "Recall (%)",
            "F1 Score (%)"
        ]


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.warning(
            "Classification results file was not found."
        )


    # --------------------------------------------------------
    # MODEL COMPARISON
    # --------------------------------------------------------

    comparison_image = (
        RESULT_DIR /
        "model_comparison.png"
    )


    if comparison_image.exists():

        st.subheader(
            "📊 Model Comparison"
        )


        st.image(
            str(comparison_image),
            use_container_width=True
        )


    # --------------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------------

    st.subheader(
        "🔍 Confusion Matrix"
    )


    classification_models = (
        get_available_models()
    )


    selected_cm_model = st.selectbox(
        "Select Model",
        classification_models,
        key="classification_confusion_model"
    )


    cm_filename = (
        selected_cm_model
        .lower()
        .replace(" ", "_")
        + "_confusion_matrix.png"
    )


    cm_path = (
        RESULT_DIR /
        cm_filename
    )


    if cm_path.exists():

        st.image(
            str(cm_path),
            use_container_width=True
        )

    else:

        st.warning(
            "Confusion matrix not found."
        )


    # --------------------------------------------------------
    # FEATURE IMPORTANCE
    # --------------------------------------------------------

    feature_image = (
        RESULT_DIR /
        "random_forest_feature_importance.png"
    )


    if feature_image.exists():

        st.subheader(
            "📌 Random Forest Feature Importance"
        )


        st.image(
            str(feature_image),
            use_container_width=True
        )


# ============================================================
# TAB 2 - REGRESSION
# ============================================================

with tab2:

    st.header(
        "📈 Regression Analysis"
    )


    st.write(
        """
        Regression models are used here as an exploratory
        analysis to predict the continuous variable
        activity_hour.
        """
    )


    st.info(
        """
        Note: activity_hour is used as an exploratory
        regression target because the fused dataset contains
        only four meaningful percentage observations.
        Therefore, percentage is not suitable for a reliable
        regression experiment on this dataset.
        """
    )


    if REGRESSION_RESULTS.exists():

        regression_df = pd.read_csv(
            REGRESSION_RESULTS
        )


        st.subheader(
            "📊 Regression Model Performance"
        )


        display_regression = regression_df[
            [
                "Model",
                "MAE",
                "MSE",
                "RMSE",
                "R2_Mean",
                "Training_R2_Mean"
            ]
        ].copy()


        display_regression[
            "MAE"
        ] = display_regression[
            "MAE"
        ].round(4)


        display_regression[
            "MSE"
        ] = display_regression[
            "MSE"
        ].round(4)


        display_regression[
            "RMSE"
        ] = display_regression[
            "RMSE"
        ].round(4)


        display_regression[
            "R2_Mean"
        ] = display_regression[
            "R2_Mean"
        ].round(4)


        display_regression[
            "Training_R2_Mean"
        ] = display_regression[
            "Training_R2_Mean"
        ].round(4)


        display_regression.columns = [
            "Model",
            "MAE",
            "MSE",
            "RMSE",
            "R² Score",
            "Training R²"
        ]


        st.dataframe(
            display_regression,
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # EXPLANATION
        # ----------------------------------------------------

        st.subheader(
            "📚 Regression Metrics"
        )


        st.markdown(
            """
            **MAE:** Average absolute prediction error.

            **MSE:** Average squared prediction error.

            **RMSE:** Square root of MSE and represents
            prediction error in the target's scale.

            **R² Score:** Indicates how well the model
            explains variation in the target variable.
            """
        )


    else:

        st.warning(
            """
            Regression results were not found.

            Run:

            python ml_module/regression.py
            """
        )


# ============================================================
# TAB 3 - PREDICTION
# ============================================================

with tab3:

    st.header(
        "🔮 Activity Prediction"
    )


    st.write(
        """
        Enter activity characteristics and select a
        trained classification model to predict the
        activity type.
        """
    )


    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    models = get_available_models()


    selected_model = st.selectbox(
        "Choose Classification Model",
        models,
        key="prediction_model"
    )


    st.info(
        f"Selected Model: {selected_model}"
    )


    # --------------------------------------------------------
    # INPUTS
    # --------------------------------------------------------

    st.subheader(
        "📊 Activity Information"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        activity_hour = st.number_input(
            "Activity Hour",
            min_value=0,
            max_value=23,
            value=12
        )


        question_length = st.number_input(
            "Question Length",
            min_value=0,
            value=100
        )


        answer_length = st.number_input(
            "Answer Length",
            min_value=0,
            value=500
        )


        instruction_length = st.number_input(
            "Instruction Length",
            min_value=0,
            value=0
        )


    with col2:

        description_length = st.number_input(
            "Description Length",
            min_value=0,
            value=0
        )


        results_count = st.number_input(
            "Results Count",
            min_value=0,
            value=0
        )


        message_count = st.number_input(
            "Message Count",
            min_value=0,
            value=1
        )


    with col3:

        has_question = st.selectbox(
            "Has Question?",
            [0, 1]
        )


        has_answer = st.selectbox(
            "Has Answer?",
            [0, 1]
        )


        has_source = st.selectbox(
            "Has Source?",
            [0, 1]
        )


        has_instruction = st.selectbox(
            "Has Instruction?",
            [0, 1]
        )


    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    if st.button(
        "🔮 Predict Activity",
        type="primary"
    ):


        input_data = prepare_input(

            activity_hour=activity_hour,

            question_length=question_length,

            answer_length=answer_length,

            instruction_length=instruction_length,

            description_length=description_length,

            results_count=results_count,

            message_count=message_count,

            has_question=has_question,

            has_answer=has_answer,

            has_source=has_source,

            has_instruction=has_instruction

        )


        prediction = predict_activity(
            selected_model,
            input_data
        )


        st.success(
            f"Predicted Activity: **{prediction.upper()}**"
        )


        st.subheader(
            "Input Used for Prediction"
        )


        st.dataframe(
            input_data,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# TAB 4 - INFORMATION
# ============================================================

with tab4:

    st.header(
        "📚 About the ML Module"
    )


    st.subheader(
        "🎯 Classification"
    )


    st.write(
        """
        Classification predicts the type of StudyNova
        activity.

        The target variable is:

        activity_type

        Possible activity types include:

        • chat
        • image
        • youtube
        • saved_note
        • user
        • quiz
        """
    )


    st.subheader(
        "🤖 Classification Algorithms"
    )


    st.write(
        """
        The following algorithms are evaluated:

        • Logistic Regression
        • Naive Bayes
        • Decision Tree
        • Random Forest
        • Support Vector Machine (SVM)
        """
    )


    st.subheader(
        "📈 Regression"
    )


    st.write(
        """
        The regression module demonstrates:

        • Simple Linear Regression
        • Multiple Linear Regression
        • Polynomial Regression

        The current exploratory target is activity_hour.
        """
    )


    st.subheader(
        "📊 Evaluation Techniques"
    )


    st.write(
        """
        Classification:

        • Accuracy
        • Precision
        • Recall
        • F1-score
        • Confusion Matrix
        • Cross-validation
        • Feature Importance


        Regression:

        • MAE
        • MSE
        • RMSE
        • R² Score
        • Cross-validation
        """
    )


    st.subheader(
        "⚠️ Dataset Limitation"
    )


    st.warning(
        """
        The current fused dataset contains only 60 records.

        Therefore, the ML results should be interpreted
        as an academic/exploratory experiment rather than
        production-level predictive performance.

        A larger and more balanced dataset would be required
        for stronger real-world generalization.
        """
    )

    # ==========================================================
# FOOTER
# ==========================================================

st.divider()

footer1, footer2, footer3 = st.columns(
    3
)

with footer1:

    st.caption(
        "📈 StudyNova Data Science EDA"
    )

with footer2:

    st.caption(
        " • 🐼 Pandas • 🔢 NumPy • 📊 Matplotlib "
    )

with footer3:

    st.caption(
        "👩‍💻 Developed by Payal Pawar"
    )