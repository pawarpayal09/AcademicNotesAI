import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from preprocessing import (
    load_dataset,
    prepare_classification_data
)


# ==========================================================
# LOAD DATA
# ==========================================================

df = load_dataset()

X, y = prepare_classification_data(df)


print("\n==========================================")
print("STUDYNOVA CLASSIFICATION")
print("==========================================")

print("\nDataset shape:")
print(X.shape)

print("\nTarget distribution:")
print(y.value_counts())


# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# ==========================================================
# MODELS
# ==========================================================

models = {

    "Logistic Regression":

        Pipeline([
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

    "Naive Bayes":

        GaussianNB(),

    "Decision Tree":

        DecisionTreeClassifier(
            random_state=42,
            max_depth=5
        ),

    "Random Forest":

        RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=8
        ),

    "SVM":

        Pipeline([
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


# ==========================================================
# RESULTS
# ==========================================================

results = []


# ==========================================================
# TRAIN EACH MODEL
# ==========================================================

for name, model in models.items():

    print("\n------------------------------------------")
    print(name)
    print("------------------------------------------")

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print(
        f"Accuracy  : {accuracy:.4f}"
    )

    print(
        f"Precision : {precision:.4f}"
    )

    print(
        f"Recall    : {recall:.4f}"
    )

    print(
        f"F1 Score  : {f1:.4f}"
    )

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    results.append({

        "Algorithm": name,

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1 Score": f1
    })

    # ------------------------------------------------------
    # SAVE MODEL
    # ------------------------------------------------------

    model_filename = (
        name.lower()
        .replace(" ", "_")
        + ".pkl"
    )

    model_path = (
        Path(__file__).resolve().parent
        / "models"
        / model_filename
    )

    joblib.dump(
        model,
        model_path
    )

    print(
        f"Model saved: {model_path}"
    )


# ==========================================================
# SAVE RESULTS
# ==========================================================

results_df = pd.DataFrame(
    results
)

print("\n==========================================")
print("MODEL COMPARISON")
print("==========================================")

print(
    results_df.to_string(
        index=False
    )
)

results_path = (
    Path(__file__).resolve().parent
    / "classification_results.csv"
)

results_df.to_csv(
    results_path,
    index=False
)

print(
    f"\nResults saved to: {results_path}"
)