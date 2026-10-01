import pandas as pd
import numpy as np
from pathlib import Path


# ==========================================================
# LOAD DATASET
# ==========================================================

def load_dataset():

    current_dir = Path(__file__).resolve().parent

    file_path = (
        current_dir
        / "data"
        / "StudyNova_Fused_Dataset.xlsx"
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"Dataset not found:\n{file_path}"
        )

    df = pd.read_excel(file_path)

    return df


# ==========================================================
# CLASSIFICATION DATA
# ==========================================================

def prepare_classification_data(df):

    # Target
    target = "activity_type"

    # Numerical / useful behavioral features
    features = [
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
        "has_instruction"
    ]

    X = df[features].copy()

    y = df[target].copy()

    # Convert everything to numeric
    X = X.apply(
        pd.to_numeric,
        errors="coerce"
    )

    X = X.fillna(0)

    y = y.fillna("unknown")

    return X, y


# ==========================================================
# REGRESSION DATA
# ==========================================================

def prepare_regression_data(df):

    # We use activity_hour as a continuous
    # exploratory regression target.

    target = "activity_hour"

    features = [
        "question_length",
        "answer_length",
        "instruction_length",
        "description_length",
        "results_count",
        "message_count",
        "has_question",
        "has_answer",
        "has_source",
        "has_instruction"
    ]

    X = df[features].copy()

    y = df[target].copy()

    X = X.apply(
        pd.to_numeric,
        errors="coerce"
    )

    y = pd.to_numeric(
        y,
        errors="coerce"
    )

    X = X.fillna(0)

    y = y.fillna(y.median())

    return X, y
