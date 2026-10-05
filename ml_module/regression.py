from pathlib import Path

import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import KFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "models"
RESULT_DIR = BASE_DIR / "results"

MODEL_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)


# ============================================================
# REGRESSION FEATURES
# ============================================================

FEATURE_COLUMNS = [
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


TARGET_COLUMN = "activity_hour"


# ============================================================
# LOAD DATASET
# ============================================================

def load_regression_data():

    data_path = (
        BASE_DIR /
        "data" /
        "StudyNova_Fused_Dataset.xlsx"
    )

    if not data_path.exists():

        raise FileNotFoundError(
            f"Dataset not found:\n{data_path}"
        )

    df = pd.read_excel(data_path)

    required_columns = FEATURE_COLUMNS + [
        TARGET_COLUMN
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing columns:\n"
            + "\n".join(missing_columns)
        )

    regression_df = df[
        required_columns
    ].copy()

    # Convert values to numeric
    for column in required_columns:

        regression_df[column] = pd.to_numeric(
            regression_df[column],
            errors="coerce"
        )

    # Remove rows where target is missing
    regression_df = regression_df.dropna(
        subset=[TARGET_COLUMN]
    )

    # Fill missing feature values
    for column in FEATURE_COLUMNS:

        median_value = regression_df[
            column
        ].median()

        regression_df[column] = (
            regression_df[column]
            .fillna(median_value)
        )

    X = regression_df[
        FEATURE_COLUMNS
    ]

    y = regression_df[
        TARGET_COLUMN
    ]

    return X, y


# ============================================================
# MODELS
# ============================================================

models = {

    "Simple Linear Regression": Pipeline([
        (
            "model",
            LinearRegression()
        )
    ]),

    "Multiple Linear Regression": Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            LinearRegression()
        )
    ]),

    "Polynomial Regression": Pipeline([
        (
            "polynomial",
            PolynomialFeatures(
                degree=2,
                include_bias=False
            )
        ),
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            LinearRegression()
        )
    ])
}


# ============================================================
# EVALUATION
# ============================================================

def evaluate_models(X, y):

    print("\n")
    print("=" * 70)
    print("STUDYNOVA REGRESSION MODEL EVALUATION")
    print("=" * 70)

    print(f"\nRecords : {len(X)}")
    print(f"Features: {len(X.columns)}")
    print(f"Target  : {TARGET_COLUMN}")

    print("\nFeatures:")

    for column in X.columns:
        print(f" - {column}")


    # 4-fold cross validation
    cv = KFold(
        n_splits=4,
        shuffle=True,
        random_state=42
    )


    results = []


    for model_name, model in models.items():

        print("\n")
        print("-" * 70)
        print(f"MODEL: {model_name}")
        print("-" * 70)


        cv_results = cross_validate(
            model,
            X,
            y,
            cv=cv,
            scoring={
                "mae": "neg_mean_absolute_error",
                "mse": "neg_mean_squared_error",
                "r2": "r2"
            },
            return_train_score=True
        )


        mae = (
            -cv_results[
                "test_mae"
            ].mean()
        )

        mse = (
            -cv_results[
                "test_mse"
            ].mean()
        )

        rmse = np.sqrt(mse)

        r2 = (
            cv_results[
                "test_r2"
            ].mean()
        )

        train_r2 = (
            cv_results[
                "train_r2"
            ].mean()
        )


        print(
            f"MAE              : {mae:.4f}"
        )

        print(
            f"MSE              : {mse:.4f}"
        )

        print(
            f"RMSE             : {rmse:.4f}"
        )

        print(
            f"R² Score         : {r2:.4f}"
        )

        print(
            f"Training R²      : {train_r2:.4f}"
        )


        results.append({

            "Model": model_name,

            "MAE": mae,

            "MSE": mse,

            "RMSE": rmse,

            "R2_Mean": r2,

            "Training_R2_Mean": train_r2

        })


    results_df = pd.DataFrame(
        results
    )


    # Sort by R2
    results_df = results_df.sort_values(
        by="R2_Mean",
        ascending=False
    )


    result_path = (
        RESULT_DIR /
        "regression_results.csv"
    )


    results_df.to_csv(
        result_path,
        index=False
    )


    print("\n")
    print("=" * 70)
    print("REGRESSION MODEL COMPARISON")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )


    print("\nResults saved to:")
    print(result_path)


    return results_df


# ============================================================
# TRAIN FINAL MODELS
# ============================================================

def train_final_models(X, y):

    print("\n")
    print("=" * 70)
    print("TRAINING FINAL REGRESSION MODELS")
    print("=" * 70)


    for model_name, model in models.items():

        print(
            f"\nTraining {model_name}..."
        )


        model.fit(
            X,
            y
        )


        filename = (
            model_name
            .lower()
            .replace(" ", "_")
            + ".pkl"
        )


        model_path = (
            MODEL_DIR /
            filename
        )


        joblib.dump(
            model,
            model_path
        )


        print(
            f"Saved: {model_path}"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    X, y = load_regression_data()

    evaluate_models(
        X,
        y
    )

    train_final_models(
        X,
        y
    )


    print("\n")
    print("=" * 70)
    print("REGRESSION PROCESS COMPLETED")
    print("=" * 70)