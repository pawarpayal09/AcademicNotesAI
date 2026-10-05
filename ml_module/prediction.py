from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"


MODEL_FILES = {
    "Logistic Regression": MODEL_DIR / "logistic_regression.pkl",
    "Naive Bayes": MODEL_DIR / "naive_bayes.pkl",
    "Decision Tree": MODEL_DIR / "decision_tree.pkl",
    "Random Forest": MODEL_DIR / "random_forest.pkl",
    "SVM": MODEL_DIR / "svm.pkl"
}


FEATURE_COLUMNS = [
    "activity_hour",
    "question_length",
    "answer_length",
    "instruction_length",
    "description_length",
    "results_count",
    "message_count",
    "has_question",
    "has_answer",
    "has_source",
    "has_instruction",
]


def load_model(model_name):
    if model_name not in MODEL_FILES:
        raise ValueError(f"Unknown model: {model_name}")

    model_path = MODEL_FILES[model_name]

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found:\n{model_path}"
        )

    return joblib.load(model_path)


def prepare_input(
    activity_hour,
    question_length,
    answer_length,
    instruction_length,
    description_length,
    results_count,
    message_count,
    has_question,
    has_answer,
    has_source,
    has_instruction
):
    data = {
        "activity_hour": activity_hour,
        "question_length": question_length,
        "answer_length": answer_length,
        "instruction_length": instruction_length,
        "description_length": description_length,
        "results_count": results_count,
        "message_count": message_count,
        "has_question": has_question,
        "has_answer": has_answer,
        "has_source": has_source,
        "has_instruction": has_instruction,
    }

    return pd.DataFrame([data], columns=FEATURE_COLUMNS)


def predict_activity(model_name, input_data):

    model = load_model(model_name)

    prediction = model.predict(input_data)

    return prediction[0]


def get_available_models():

    return list(MODEL_FILES.keys())

if __name__ == "__main__":

    sample_data = prepare_input(
        activity_hour=14,
        question_length=100,
        answer_length=500,
        instruction_length=0,
        description_length=0,
        results_count=0,
        message_count=2,
        has_question=1,
        has_answer=1,
        has_source=1,
        has_instruction=0
    )

    print("\nSample Input:")
    print(sample_data)

    print("\nPredictions:")

    for model_name in get_available_models():

        prediction = predict_activity(
            model_name,
            sample_data
        )

        print(
            f"{model_name}: {prediction}"
        )