from pathlib import Path

import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "StudyNova_Fused_Dataset.xlsx"


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():
    """
    Load the StudyNova fused dataset from Excel.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at:\n{DATA_PATH}"
        )

    df = pd.read_excel(DATA_PATH)

    return df


# ============================================================
# DATASET INFORMATION
# ============================================================

def show_dataset_info(df):
    """
    Display basic information about the dataset.
    """

    print("\n" + "=" * 60)
    print("DATASET INFORMATION")
    print("=" * 60)

    print(f"Number of records : {len(df)}")
    print(f"Number of columns : {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f" - {column}")


# ============================================================
# DATA QUALITY CHECK
# ============================================================

def check_data_quality(df):
    """
    Perform basic data-quality checks.
    """

    print("\n" + "=" * 60)
    print("DATA QUALITY CHECK")
    print("=" * 60)

    # Missing values
    missing_values = df.isnull().sum()

    print("\nMissing values:")
    print(missing_values[missing_values > 0])

    # Duplicate records
    duplicate_count = df.duplicated().sum()

    print(f"\nDuplicate records: {duplicate_count}")

    # Target distribution
    if "activity_type" in df.columns:

        print("\nActivity type distribution:")

        print(
            df["activity_type"]
            .value_counts(dropna=False)
        )


# ============================================================
# CLASSIFICATION DATA PREPARATION
# ============================================================

def prepare_classification_data(df):
    """
    Prepare features (X) and target (y)
    for the classification problem.

    Target:
        activity_type

    Important:
    Columns that directly reveal activity_type are
    excluded to prevent data leakage.
    """

    target_column = "activity_type"

    # Features selected for the classification task
    feature_columns = [
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

    # Check target
    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' not found."
        )

    # Check features
    missing_features = [
        column
        for column in feature_columns
        if column not in df.columns
    ]

    if missing_features:
        raise ValueError(
            "The following feature columns are missing:\n"
            + "\n".join(missing_features)
        )

    # Keep only required rows
    model_df = df[
        feature_columns + [target_column]
    ].copy()

    # Remove rows with missing target
    model_df = model_df.dropna(
        subset=[target_column]
    )

    # Convert features to numeric
    for column in feature_columns:

        model_df[column] = pd.to_numeric(
            model_df[column],
            errors="coerce"
        )

    # Fill missing numeric values using median
    for column in feature_columns:

        median_value = model_df[column].median()

        model_df[column] = model_df[column].fillna(
            median_value
        )

    X = model_df[feature_columns]

    y = model_df[target_column].astype(str)

    return X, y


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    df = load_dataset()

    show_dataset_info(df)

    check_data_quality(df)

    X, y = prepare_classification_data(df)

    print("\n" + "=" * 60)
    print("CLASSIFICATION DATA")
    print("=" * 60)

    print(f"Feature records : {len(X)}")
    print(f"Feature count   : {len(X.columns)}")

    print("\nFeatures:")

    for column in X.columns:
        print(f" - {column}")

    print("\nTarget:")
    print(y.name)

    print("\nTarget distribution:")
    print(y.value_counts())