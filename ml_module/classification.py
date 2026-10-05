from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate
)

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression

from sklearn.naive_bayes import GaussianNB

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier

from sklearn.svm import SVC

from sklearn.metrics import (
    make_scorer,
    precision_score,
    recall_score,
    f1_score
)

from preprocessing import (
    load_dataset,
    prepare_classification_data
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "models"

RESULT_DIR = BASE_DIR / "results"

MODEL_DIR.mkdir(
    exist_ok=True
)

RESULT_DIR.mkdir(
    exist_ok=True
)


# ============================================================
# CLASSIFICATION MODELS
# ============================================================

models = {

    "Logistic Regression": Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            LogisticRegression(
                max_iter=2000
            )
        )
    ]),

    "Naive Bayes": GaussianNB(),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=5,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42,
        class_weight="balanced"
    ),

    "SVM": Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            SVC(
                kernel="rbf"
            )
        )
    ])
}


# ============================================================
# CROSS-VALIDATION
# ============================================================

cv = StratifiedKFold(
    n_splits=4,
    shuffle=True,
    random_state=42
)


# ============================================================
# EVALUATION METRICS
# ============================================================

scoring = {

    "accuracy": "accuracy",

    "precision": make_scorer(
        precision_score,
        average="weighted",
        zero_division=0
    ),

    "recall": make_scorer(
        recall_score,
        average="weighted",
        zero_division=0
    ),

    "f1": make_scorer(
        f1_score,
        average="weighted",
        zero_division=0
    )
}


# ============================================================
# TRAIN + CROSS VALIDATION
# ============================================================

def run_classification():

    print("\n")
    print("=" * 70)
    print("STUDYNOVA CLASSIFICATION MODEL EVALUATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    df = load_dataset()

    X, y = prepare_classification_data(df)

    print("\nDataset:")
    print(f"Records : {len(X)}")
    print(f"Features: {len(X.columns)}")

    print("\nTarget distribution:")
    print(y.value_counts())

    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    results = []

    # --------------------------------------------------------
    # Train and evaluate each model
    # --------------------------------------------------------

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
            scoring=scoring,
            return_train_score=True
        )

        # ----------------------------------------------------
        # Calculate metrics
        # ----------------------------------------------------

        accuracy_mean = (
            cv_results["test_accuracy"].mean()
        )

        accuracy_std = (
            cv_results["test_accuracy"].std()
        )

        precision_mean = (
            cv_results["test_precision"].mean()
        )

        precision_std = (
            cv_results["test_precision"].std()
        )

        recall_mean = (
            cv_results["test_recall"].mean()
        )

        recall_std = (
            cv_results["test_recall"].std()
        )

        f1_mean = (
            cv_results["test_f1"].mean()
        )

        f1_std = (
            cv_results["test_f1"].std()
        )

        train_accuracy_mean = (
            cv_results["train_accuracy"].mean()
        )

        # ----------------------------------------------------
        # Print results
        # ----------------------------------------------------

        print(
            f"Cross-validation Accuracy : "
            f"{accuracy_mean:.4f} "
            f"(± {accuracy_std:.4f})"
        )

        print(
            f"Precision                 : "
            f"{precision_mean:.4f} "
            f"(± {precision_std:.4f})"
        )

        print(
            f"Recall                    : "
            f"{recall_mean:.4f} "
            f"(± {recall_std:.4f})"
        )

        print(
            f"F1-score                  : "
            f"{f1_mean:.4f} "
            f"(± {f1_std:.4f})"
        )

        print(
            f"Training Accuracy         : "
            f"{train_accuracy_mean:.4f}"
        )

        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        results.append({

            "Model": model_name,

            "Accuracy_Mean": accuracy_mean,

            "Accuracy_Std": accuracy_std,

            "Precision_Mean": precision_mean,

            "Precision_Std": precision_std,

            "Recall_Mean": recall_mean,

            "Recall_Std": recall_std,

            "F1_Mean": f1_mean,

            "F1_Std": f1_std,

            "Training_Accuracy_Mean":
                train_accuracy_mean
        })


    # ========================================================
    # RESULTS TABLE
    # ========================================================

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="F1_Mean",
        ascending=False
    )

    result_path = (
        RESULT_DIR /
        "classification_results.csv"
    )

    results_df.to_csv(
        result_path,
        index=False
    )

    print("\n")
    print("=" * 70)
    print("MODEL COMPARISON")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )

    print("\nResults saved to:")

    print(result_path)


# ============================================================
# TRAIN FINAL MODELS
# ============================================================

def train_final_models():

    print("\n")
    print("=" * 70)
    print("TRAINING FINAL MODELS")
    print("=" * 70)

    df = load_dataset()

    X, y = prepare_classification_data(df)

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

    run_classification()

    train_final_models()

    print("\n")
    print("=" * 70)
    print("CLASSIFICATION PROCESS COMPLETED")
    print("=" * 70)