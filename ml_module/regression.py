import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import (
    StandardScaler,
    PolynomialFeatures
)

from sklearn.pipeline import Pipeline

from sklearn.linear_model import (
    LinearRegression,
    Ridge
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


from preprocessing import (
    load_dataset,
    prepare_regression_data
)


# ==========================================================
# LOAD DATA
# ==========================================================

df = load_dataset()

X, y = prepare_regression_data(
    df
)


print("\n==========================================")
print("STUDYNOVA REGRESSION")
print("==========================================")


print("\nDataset shape:")

print(
    X.shape
)


print("\nTarget statistics:")

print(
    y.describe()
)


# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.25,

    random_state=42
)


# ==========================================================
# MODELS
# ==========================================================

models = {

    "Simple Linear Regression":

        LinearRegression(),

    "Multiple Linear Regression":

        LinearRegression(),

    "Polynomial Regression":

        Pipeline([

            (
                "polynomial_features",

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
                "regression",

                Ridge(
                    alpha=1.0
                )
            )
        ])
}


# ==========================================================
# RESULTS
# ==========================================================

results = []


# ==========================================================
# TRAIN MODELS
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


    mae = mean_absolute_error(

        y_test,

        predictions
    )


    mse = mean_squared_error(

        y_test,

        predictions
    )


    rmse = np.sqrt(

        mse
    )


    r2 = r2_score(

        y_test,

        predictions
    )


    print(

        f"MAE  : {mae:.4f}"
    )


    print(

        f"MSE  : {mse:.4f}"
    )


    print(

        f"RMSE : {rmse:.4f}"
    )


    print(

        f"R²   : {r2:.4f}"
    )


    results.append({

        "Algorithm": name,

        "MAE": mae,

        "MSE": mse,

        "RMSE": rmse,

        "R2 Score": r2
    })


    # ======================================================
    # SAVE MODEL
    # ======================================================

    model_filename = (

        name.lower()

        .replace(
            " ",
            "_"
        )

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

print(
    "REGRESSION MODEL COMPARISON"
)

print("==========================================")


print(

    results_df.to_string(
        index=False
    )
)


results_path = (

    Path(__file__).resolve().parent

    / "regression_results.csv"
)


results_df.to_csv(

    results_path,

    index=False
)


print(

    f"\nResults saved to: {results_path}"
)