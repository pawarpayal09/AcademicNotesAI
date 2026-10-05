from pathlib import Path

import joblib
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
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

RESULT_DIR.mkdir(
    exist_ok=True
)


# ============================================================
# MODEL FILES
# ============================================================

MODEL_FILES = {

    "Logistic Regression":
        MODEL_DIR / "logistic_regression.pkl",

    "Naive Bayes":
        MODEL_DIR / "naive_bayes.pkl",

    "Decision Tree":
        MODEL_DIR / "decision_tree.pkl",

    "Random Forest":
        MODEL_DIR / "random_forest.pkl",

    "SVM":
        MODEL_DIR / "svm.pkl"
}


# ============================================================
# LOAD DATA
# ============================================================

def load_ml_data():

    print("\n" + "=" * 70)
    print("LOADING DATA")
    print("=" * 70)

    df = load_dataset()

    X, y = prepare_classification_data(df)

    print(f"Records : {len(X)}")
    print(f"Features: {len(X.columns)}")

    return X, y


# ============================================================
# CHECK MODEL FILES
# ============================================================

def check_model_files():

    print("\n" + "=" * 70)
    print("CHECKING TRAINED MODELS")
    print("=" * 70)

    for model_name, model_path in MODEL_FILES.items():

        if model_path.exists():

            print(
                f"✓ {model_name}: found"
            )

        else:

            print(
                f"✗ {model_name}: NOT FOUND"
            )


# ============================================================
# CONFUSION MATRIX
# ============================================================

def generate_confusion_matrices(X, y):

    print("\n" + "=" * 70)
    print("GENERATING CONFUSION MATRICES")
    print("=" * 70)

    # Use same CV configuration as classification.py
    cv = StratifiedKFold(
        n_splits=4,
        shuffle=True,
        random_state=42
    )

    class_labels = sorted(
        y.unique()
    )

    for model_name, model_path in MODEL_FILES.items():

        print(
            f"\nProcessing: {model_name}"
        )

        model = joblib.load(
            model_path
        )

        all_true = []
        all_pred = []

        # ----------------------------------------------------
        # Generate out-of-fold predictions
        # ----------------------------------------------------

        for train_index, test_index in cv.split(X, y):

            X_train = X.iloc[train_index]
            X_test = X.iloc[test_index]

            y_train = y.iloc[train_index]
            y_test = y.iloc[test_index]

            # Train model on training fold
            model.fit(
                X_train,
                y_train
            )

            # Predict validation fold
            predictions = model.predict(
                X_test
            )

            all_true.extend(
                y_test.tolist()
            )

            all_pred.extend(
                predictions.tolist()
            )

        # ----------------------------------------------------
        # Confusion matrix
        # ----------------------------------------------------

        cm = confusion_matrix(
            all_true,
            all_pred,
            labels=class_labels
        )

        # ----------------------------------------------------
        # Plot
        # ----------------------------------------------------

        plt.figure(
            figsize=(9, 7)
        )

        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=class_labels,
            yticklabels=class_labels
        )

        plt.title(
            f"Confusion Matrix - {model_name}"
        )

        plt.xlabel(
            "Predicted Activity"
        )

        plt.ylabel(
            "Actual Activity"
        )

        plt.tight_layout()

        filename = (
            model_name
            .lower()
            .replace(" ", "_")
            + "_confusion_matrix.png"
        )

        output_path = (
            RESULT_DIR /
            filename
        )

        plt.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print(
            f"Saved: {output_path}"
        )


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

def generate_classification_reports(X, y):

    print("\n" + "=" * 70)
    print("GENERATING CLASSIFICATION REPORTS")
    print("=" * 70)

    cv = StratifiedKFold(
        n_splits=4,
        shuffle=True,
        random_state=42
    )

    all_reports = []

    for model_name, model_path in MODEL_FILES.items():

        print(
            f"\nProcessing: {model_name}"
        )

        model = joblib.load(
            model_path
        )

        all_true = []
        all_pred = []

        for train_index, test_index in cv.split(X, y):

            X_train = X.iloc[train_index]
            X_test = X.iloc[test_index]

            y_train = y.iloc[train_index]
            y_test = y.iloc[test_index]

            model.fit(
                X_train,
                y_train
            )

            predictions = model.predict(
                X_test
            )

            all_true.extend(
                y_test.tolist()
            )

            all_pred.extend(
                predictions.tolist()
            )

        # ----------------------------------------------------
        # Generate detailed classification report
        # ----------------------------------------------------

        report = classification_report(
            all_true,
            all_pred,
            labels=sorted(y.unique()),
            output_dict=True,
            zero_division=0
        )

        report_df = pd.DataFrame(
            report
        ).transpose()

        report_filename = (
            model_name
            .lower()
            .replace(" ", "_")
            + "_classification_report.csv"
        )

        report_path = (
            RESULT_DIR /
            report_filename
        )

        report_df.to_csv(
            report_path
        )

        print(
            f"Saved: {report_path}"
        )

        # ----------------------------------------------------
        # Store overall metrics
        # ----------------------------------------------------

        accuracy = accuracy_score(
            all_true,
            all_pred
        )

        precision = precision_score(
            all_true,
            all_pred,
            average="weighted",
            zero_division=0
        )

        recall = recall_score(
            all_true,
            all_pred,
            average="weighted",
            zero_division=0
        )

        f1 = f1_score(
            all_true,
            all_pred,
            average="weighted",
            zero_division=0
        )

        all_reports.append({

            "Model": model_name,

            "Accuracy": accuracy,

            "Precision": precision,

            "Recall": recall,

            "F1": f1
        })

    # --------------------------------------------------------
    # Save combined report
    # --------------------------------------------------------

    combined_df = pd.DataFrame(
        all_reports
    )

    combined_path = (
        RESULT_DIR /
        "classification_diagnostic_summary.csv"
    )

    combined_df.to_csv(
        combined_path,
        index=False
    )

    print(
        f"\nCombined report saved: {combined_path}"
    )


# ============================================================
# MODEL COMPARISON GRAPH
# ============================================================

def generate_model_comparison():

    print("\n" + "=" * 70)
    print("GENERATING MODEL COMPARISON GRAPH")
    print("=" * 70)

    results_path = (
        RESULT_DIR /
        "classification_results.csv"
    )

    if not results_path.exists():

        print(
            "classification_results.csv not found."
        )

        return

    results = pd.read_csv(
        results_path
    )

    # --------------------------------------------------------
    # Convert model results into long format
    # --------------------------------------------------------

    metric_columns = [
        "Accuracy_Mean",
        "Precision_Mean",
        "Recall_Mean",
        "F1_Mean"
    ]

    comparison = results[
        ["Model"] + metric_columns
    ].copy()

    comparison = comparison.set_index(
        "Model"
    )

    comparison.columns = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1"
    ]

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    ax = comparison.plot(
        kind="bar",
        figsize=(12, 7)
    )

    plt.title(
        "StudyNova Classification Model Comparison"
    )

    plt.ylabel(
        "Score"
    )

    plt.xlabel(
        "Machine Learning Model"
    )

    plt.ylim(
        0,
        1
    )

    plt.xticks(
        rotation=30,
        ha="right"
    )

    plt.legend(
        title="Metrics"
    )

    plt.tight_layout()

    output_path = (
        RESULT_DIR /
        "model_comparison.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output_path}"
    )


# ============================================================
# RANDOM FOREST FEATURE IMPORTANCE
# ============================================================

def generate_feature_importance(X, y):

    print("\n" + "=" * 70)
    print("GENERATING FEATURE IMPORTANCE")
    print("=" * 70)

    model_path = (
        MODEL_DIR /
        "random_forest.pkl"
    )

    if not model_path.exists():

        print(
            "Random Forest model not found."
        )

        return

    model = joblib.load(
        model_path
    )

    # Retrain on complete dataset
    model.fit(
        X,
        y
    )

    # --------------------------------------------------------
    # Access underlying Random Forest
    # --------------------------------------------------------

    if hasattr(
        model,
        "feature_importances_"
    ):

        importances = (
            model.feature_importances_
        )

    else:

        # If model is wrapped in Pipeline
        if hasattr(
            model,
            "named_steps"
        ):

            rf_model = (
                model.named_steps.get(
                    "model"
                )
            )

            if rf_model is None:

                print(
                    "Random Forest estimator not found."
                )

                return

            importances = (
                rf_model.feature_importances_
            )

        else:

            print(
                "Could not access feature importance."
            )

            return

    # --------------------------------------------------------
    # Create feature importance table
    # --------------------------------------------------------

    importance_df = pd.DataFrame({

        "Feature":
            X.columns,

        "Importance":
            importances
    })

    importance_df = (
        importance_df
        .sort_values(
            by="Importance",
            ascending=False
        )
    )

    output_csv = (
        RESULT_DIR /
        "random_forest_feature_importance.csv"
    )

    importance_df.to_csv(
        output_csv,
        index=False
    )

    print(
        f"Saved: {output_csv}"
    )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(
        figsize=(10, 7)
    )

    plt.barh(
        importance_df["Feature"],
        importance_df["Importance"]
    )

    plt.gca().invert_yaxis()

    plt.title(
        "Random Forest Feature Importance"
    )

    plt.xlabel(
        "Importance"
    )

    plt.ylabel(
        "Feature"
    )

    plt.tight_layout()

    output_png = (
        RESULT_DIR /
        "random_forest_feature_importance.png"
    )

    plt.savefig(
        output_png,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output_png}"
    )


# ============================================================
# OVERFITTING ANALYSIS
# ============================================================

def generate_overfitting_analysis():

    print("\n" + "=" * 70)
    print("ANALYZING TRAINING VS VALIDATION PERFORMANCE")
    print("=" * 70)

    results_path = (
        RESULT_DIR /
        "classification_results.csv"
    )

    if not results_path.exists():

        print(
            "classification_results.csv not found."
        )

        return

    results = pd.read_csv(
        results_path
    )

    results["Accuracy_Gap"] = (
        results["Training_Accuracy_Mean"]
        -
        results["Accuracy_Mean"]
    )

    output_path = (
        RESULT_DIR /
        "overfitting_analysis.csv"
    )

    results[
        [
            "Model",
            "Training_Accuracy_Mean",
            "Accuracy_Mean",
            "Accuracy_Gap"
        ]
    ].to_csv(
        output_path,
        index=False
    )

    print(
        f"\nSaved: {output_path}"
    )

    print("\nTraining vs Validation:")

    print(
        results[
            [
                "Model",
                "Training_Accuracy_Mean",
                "Accuracy_Mean",
                "Accuracy_Gap"
            ]
        ].to_string(
            index=False
        )
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("STUDYNOVA CLASSIFICATION DIAGNOSTIC ANALYSIS")
    print("=" * 70)

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    X, y = load_ml_data()

    # --------------------------------------------------------
    # Check model files
    # --------------------------------------------------------

    check_model_files()

    # --------------------------------------------------------
    # Generate confusion matrices
    # --------------------------------------------------------

    generate_confusion_matrices(
        X,
        y
    )

    # --------------------------------------------------------
    # Generate detailed classification reports
    # --------------------------------------------------------

    generate_classification_reports(
        X,
        y
    )

    # --------------------------------------------------------
    # Model comparison
    # --------------------------------------------------------

    generate_model_comparison()

    # --------------------------------------------------------
    # Feature importance
    # --------------------------------------------------------

    generate_feature_importance(
        X,
        y
    )

    # --------------------------------------------------------
    # Overfitting analysis
    # --------------------------------------------------------

    generate_overfitting_analysis()

    print("\n")
    print("=" * 70)
    print("DIAGNOSTIC ANALYSIS COMPLETED")
    print("=" * 70)