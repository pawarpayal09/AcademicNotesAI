# ==========================================================
# StudyNova
# DATA SCIENCE & EXPLORATORY DATA ANALYSIS
# ==========================================================

import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ==========================================================
# PAGE CONFIG
# MUST BE THE FIRST STREAMLIT COMMAND
# ==========================================================

st.set_page_config(
    page_title="Data Science & EDA",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
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
# DATASET MANAGER
# ==========================================================

try:

    from data_science.dataset_manager import (
        load_combined_dataset
    )

except ImportError as error:

    st.error(
        "Unable to load the existing dataset manager."
    )

    st.code(str(error))

    st.stop()


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

    st.info(
    """
### 📌 Purpose

This page performs:

- 🔎 Data Quality Assessment
- 📋 Missing Data Analysis
- 🔄 Consistency Checks
- 📊 Outlier Detection
- 📈 Univariate Analysis
- 🔗 Bivariate Analysis
- 🧠 Multivariate Analysis
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

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "📈 Data Science & Exploratory Data Analysis"
)

st.markdown(
    """
    Analyze the current **AcademicNotesAI fused activity
    dataset** automatically generated from StudyNova's
    existing learning activities.
    """
)

# ==========================================================
# LOAD FUSED DATASET
# ==========================================================

try:

    dataframe = load_combined_dataset()

except Exception as error:

    st.error(
        "Unable to load the fused dataset."
    )

    st.exception(error)

    st.stop()


# ==========================================================
# REFRESH
# ==========================================================

refresh_left, refresh_right = st.columns(
    [6, 1]
)

with refresh_right:

    if st.button(
        "🔄 Refresh",
        use_container_width=True,
        key="refresh_data_analysis"
    ):

        st.cache_data.clear()

        st.rerun()


# ==========================================================
# EMPTY DATASET
# ==========================================================

if dataframe is None or dataframe.empty:

    st.warning(
        """
        📭 **No activity data is available yet.**

        Start using StudyNova features such as:

        • Chatbot  
        • Quiz  
        • Image Study  
        • YouTube Resources  
        • Saved Notes  

        The fused dataset will update as activities are recorded.
        """
    )

    st.stop()


# ==========================================================
# ANALYSIS COPY
# ==========================================================

df = dataframe.copy()


# ==========================================================
# BASIC CLEANING FOR ANALYSIS ONLY
# ORIGINAL DATASET IS NOT MODIFIED
# ==========================================================

df.columns = [
    str(column).strip()
    for column in df.columns
]


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def is_missing(value):

    if value is None:
        return True

    if isinstance(value, str):

        cleaned = value.strip().lower()

        if cleaned in {
            "",
            "null",
            "none",
            "nan",
            "nat",
            "n/a",
            "na",
            "not applicable",
            "unknown",
        }:

            return True

    try:

        result = pd.isna(value)

        if isinstance(result, (bool, np.bool_)):
            return bool(result)

    except Exception:
        pass

    return False


def missing_count(series):

    return int(
        series.apply(is_missing).sum()
    )


def numeric_series(series):

    return pd.to_numeric(
        series,
        errors="coerce"
    )


def safe_numeric_columns(data):

    result = []

    for column in data.columns:

        converted = pd.to_numeric(
            data[column],
            errors="coerce"
        )

        if converted.notna().sum() >= 2:

            result.append(column)

    return result


def categorical_columns(data):

    result = []

    for column in data.columns:

        if (
            data[column].dtype == "object"
            or str(data[column].dtype).startswith("category")
        ):

            result.append(column)

    return result


def valid_date_column(series):

    converted = pd.to_datetime(
        series,
        errors="coerce",
        utc=True
    )

    return (
        int(converted.notna().sum()),
        converted
    )


def iqr_outlier_mask(series):

    numeric = pd.to_numeric(
        series,
        errors="coerce"
    )

    numeric = numeric.dropna()

    if numeric.empty:

        return pd.Series(
            False,
            index=series.index
        )

    q1 = numeric.quantile(0.25)

    q3 = numeric.quantile(0.75)

    iqr = q3 - q1

    if iqr == 0:

        return pd.Series(
            False,
            index=series.index
        )

    lower = q1 - (1.5 * iqr)

    upper = q3 + (1.5 * iqr)

    numeric_original = pd.to_numeric(
        series,
        errors="coerce"
    )

    mask = (
        (numeric_original < lower)
        |
        (numeric_original > upper)
    )

    return mask.fillna(False)


def plot_histogram(series, title):

    numeric = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if numeric.empty:

        st.info(
            "No numeric observations available."
        )

        return

    fig, ax = plt.subplots(
        figsize=(8, 4)
    )

    ax.hist(
        numeric,
        bins=min(
            20,
            max(
                5,
                len(numeric)
            )
        )
    )

    ax.set_title(title)

    ax.set_xlabel(
        str(series.name)
    )

    ax.set_ylabel(
        "Frequency"
    )

    ax.grid(
        axis="y",
        alpha=0.2
    )

    fig.tight_layout()

    st.pyplot(
        fig,
        clear_figure=True
    )

    plt.close(fig)


def plot_boxplot(series, title):

    numeric = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if numeric.empty:

        st.info(
            "No numeric observations available."
        )

        return

    fig, ax = plt.subplots(
        figsize=(8, 3)
    )

    ax.boxplot(
        numeric,
        vert=False
    )

    ax.set_title(title)

    ax.set_xlabel(
        str(series.name)
    )

    ax.grid(
        axis="x",
        alpha=0.2
    )

    fig.tight_layout()

    st.pyplot(
        fig,
        clear_figure=True
    )

    plt.close(fig)


# ==========================================================
# IDENTIFY DATA TYPES
# ==========================================================

numeric_candidates = safe_numeric_columns(df)

cat_cols = categorical_columns(df)


# ==========================================================
# DATASET OVERVIEW
# ==========================================================

st.divider()

st.header(
    "📌 Dataset Overview"
)

overview1, overview2, overview3, overview4 = st.columns(
    4
)

with overview1:

    st.metric(
        "Total Records",
        f"{df.shape[0]:,}"
    )

with overview2:

    st.metric(
        "Total Attributes",
        f"{df.shape[1]:,}"
    )

with overview3:

    if "user_uid" in df.columns:

        total_users = (
            df["user_uid"]
            .apply(
                lambda value:
                np.nan if is_missing(value)
                else str(value).strip()
            )
            .dropna()
            .nunique()
        )

    else:

        total_users = 0

    st.metric(
        "Unique Users",
        f"{total_users:,}"
    )

with overview4:

    if "source_file" in df.columns:

        total_sources = (
            df["source_file"]
            .apply(
                lambda value:
                np.nan if is_missing(value)
                else str(value).strip()
            )
            .dropna()
            .nunique()
        )

    else:

        total_sources = 0

    st.metric(
        "Data Sources",
        f"{total_sources:,}"
    )


# ==========================================================
# DATA SOURCE DISTRIBUTION
# ==========================================================

if "source_file" in df.columns:

    st.subheader(
        "📂 Records by Data Source"
    )

    source_counts = (
        df["source_file"]
        .apply(
            lambda value:
            "Unknown" if is_missing(value)
            else str(value).strip()
        )
        .value_counts()
        .rename_axis("Source")
        .reset_index(name="Records")
    )

    source_col1, source_col2 = st.columns(
        [1, 1]
    )

    with source_col1:

        st.dataframe(
            source_counts,
            use_container_width=True,
            hide_index=True
        )

    with source_col2:

        st.bar_chart(
            source_counts.set_index(
                "Source"
            )["Records"]
        )


# ==========================================================
# PART D
# DATA QUALITY ASSESSMENT
# ==========================================================

st.divider()

st.header(
    "🔎 Part D — Data Quality Assessment"
)

st.caption(
    "The following checks evaluate the quality of the current "
    "fused dataset without modifying the original data."
)


# ==========================================================
# D1 STRUCTURAL CHECKS
# ==========================================================

with st.expander(
    "1️⃣ Structural Checks",
    expanded=True
):

    st.markdown(
        """
        Structural checks examine the dimensions, data types,
        uniqueness and duplication characteristics of the
        fused dataset.
        """
    )

    structural_tab1, structural_tab2, structural_tab3 = st.tabs(
        [
            "📐 Dimensions",
            "🏷️ Data Types",
            "🔢 Unique Values"
        ]
    )

    with structural_tab1:

        dimension_df = pd.DataFrame(
            {
                "Measurement": [
                    "Rows",
                    "Columns"
                ],
                "Value": [
                    df.shape[0],
                    df.shape[1]
                ]
            }
        )

        st.dataframe(
            dimension_df,
            use_container_width=True,
            hide_index=True
        )

    with structural_tab2:

        dtype_df = pd.DataFrame(
            {
                "Attribute": df.columns,
                "Data Type": [
                    str(dtype)
                    for dtype in df.dtypes
                ],
                "Non-Missing": [
                    int(
                        df[column]
                        .apply(
                            lambda value:
                            not is_missing(value)
                        )
                        .sum()
                    )
                    for column in df.columns
                ]
            }
        )

        st.dataframe(
            dtype_df,
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with structural_tab3:

        unique_df = pd.DataFrame(
            {
                "Attribute": df.columns,
                "Unique Values": [
                    df[column]
                    .astype(str)
                    .nunique(
                        dropna=False
                    )
                    for column in df.columns
                ]
            }
        ).sort_values(
            "Unique Values"
        )

        st.dataframe(
            unique_df,
            use_container_width=True,
            hide_index=True,
            height=400
        )


# ==========================================================
# DUPLICATE RECORDS
# ==========================================================

with st.expander(
    "🔁 Duplicate Records & Identifiers",
    expanded=False
):

    duplicate_records = int(
        df.duplicated().sum()
    )

    dup1, dup2 = st.columns(2)

    with dup1:

        st.metric(
            "Complete Duplicate Rows",
            f"{duplicate_records:,}"
        )

    with dup2:

        if duplicate_records == 0:

            st.success(
                "No complete duplicate records detected."
            )

        else:

            st.warning(
                "Duplicate records were detected and should be reviewed."
            )


    identifier_columns = [
        column
        for column in [
            "record_id",
            "user_uid"
        ]
        if column in df.columns
    ]

    st.markdown(
        "### Duplicate Identifiers"
    )

    if identifier_columns:

        identifier_results = []

        for column in identifier_columns:

            non_empty = (
                df[column]
                .apply(
                    lambda value:
                    np.nan if is_missing(value)
                    else str(value).strip()
                )
                .dropna()
            )

            duplicate_count = int(
                non_empty.duplicated().sum()
            )

            identifier_results.append(
                {
                    "Identifier": column,
                    "Non-Missing Values": len(non_empty),
                    "Unique Values": non_empty.nunique(),
                    "Duplicate Occurrences": duplicate_count
                }
            )

        identifier_df = pd.DataFrame(
            identifier_results
        )

        st.dataframe(
            identifier_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "user_uid is expected to repeat because one user can "
            "generate multiple learning activities. record_id is "
            "the preferred record-level identifier when available."
        )

    else:

        st.info(
            "No standard identifier columns were found."
        )


# ==========================================================
# D2 MISSING DATA
# ==========================================================

with st.expander(
    "2️⃣ Missing Data Assessment",
    expanded=True
):

    missing_rows = []

    for column in df.columns:

        count = missing_count(
            df[column]
        )

        percentage = (
            count / len(df)
        ) * 100

        missing_rows.append(
            {
                "Attribute": column,
                "Missing Values": count,
                "Missing Percentage": round(
                    percentage,
                    2
                )
            }
        )

    missing_df = pd.DataFrame(
        missing_rows
    ).sort_values(
        "Missing Percentage",
        ascending=False
    )

    st.dataframe(
        missing_df,
        use_container_width=True,
        hide_index=True
    )

    max_missing = missing_df[
        missing_df["Missing Values"] > 0
    ]

    if not max_missing.empty:

        highest_missing = max_missing.iloc[0]

        st.warning(
            f"Highest missing-data attribute: "
            f"**{highest_missing['Attribute']}** "
            f"with **{highest_missing['Missing Percentage']:.2f}%** "
            f"missing values."
        )

        st.markdown(
            "### Attributes with Highest Missing Data"
        )

        st.dataframe(
            max_missing.head(10),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "✅ No missing values detected."
        )

    st.markdown(
        "### 🛠 Missing Value Treatment"
    )

    st.info(
        """
        **Treatment strategy used for analysis:**

        • Original fused records are never modified.

        • Numeric values are converted safely using numeric coercion
          where required.

        • Missing numeric observations are excluded from statistical
          calculations such as mean, median and IQR.

        • Missing categorical values are treated as unavailable
          during consistency analysis.

        • No artificial values are inserted into the original dataset.

        This approach prevents the EDA page from changing StudyNova's
        stored activity data.
        """
    )


# ==========================================================
# D3 CONSISTENCY
# ==========================================================

with st.expander(
    "3️⃣ Consistency Assessment",
    expanded=False
):

    st.markdown(
        "### 🏷️ Categorical Consistency"
    )

    categorical_report = []

    for column in cat_cols:

        values = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        values = values[
            values != ""
        ]

        if values.empty:
            continue

        unique_values = sorted(
            set(values)
        )

        lower_groups = {}

        for value in unique_values:

            key = value.lower()

            lower_groups.setdefault(
                key,
                []
            ).append(value)

        inconsistent_groups = [
            group
            for group in lower_groups.values()
            if len(group) > 1
        ]

        if inconsistent_groups:

            categorical_report.append(
                {
                    "Attribute": column,
                    "Potential Inconsistencies":
                        " | ".join(
                            [
                                ", ".join(group)
                                for group in inconsistent_groups
                            ]
                        )
                }
            )

    if categorical_report:

        st.warning(
            "Potential case/spelling inconsistencies detected."
        )

        st.dataframe(
            pd.DataFrame(
                categorical_report
            ),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "✅ No obvious case/spelling inconsistencies detected."
        )


    # ------------------------------------------------------
    # NUMERICAL VALIDITY
    # ------------------------------------------------------

    st.markdown(
        "### 🔢 Numerical Validity"
    )

    numerical_checks = []

    for column in numeric_candidates:

        values = numeric_series(
            df[column]
        ).dropna()

        if values.empty:
            continue

        invalid_count = 0

        rule = "General numeric review"

        lower_name = column.lower()

        if (
            "percentage" in lower_name
            or "percent" in lower_name
            or "score" in lower_name
        ):

            invalid_count = int(
                (
                    (values < 0)
                    |
                    (values > 100)
                ).sum()
            )

            rule = "Expected range: 0–100"

        elif (
            "hour" in lower_name
            or "hours" in lower_name
        ):

            invalid_count = int(
                (
                    (values < 0)
                    |
                    (values > 24)
                ).sum()
            )

            rule = "Expected range: 0–24"

        elif (
            "count" in lower_name
            or "length" in lower_name
            or "results" in lower_name
        ):

            invalid_count = int(
                (values < 0).sum()
            )

            rule = "Expected non-negative values"

        numerical_checks.append(
            {
                "Attribute": column,
                "Minimum": round(
                    values.min(),
                    2
                ),
                "Maximum": round(
                    values.max(),
                    2
                ),
                "Potential Invalid Values": invalid_count,
                "Validation Rule": rule
            }
        )

    if numerical_checks:

        numerical_df = pd.DataFrame(
            numerical_checks
        )

        st.dataframe(
            numerical_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No suitable numerical attributes detected."
        )


    # ------------------------------------------------------
    # DATE / TIME
    # ------------------------------------------------------

    st.markdown(
        "### 🕒 Date/Time Consistency"
    )

    possible_date_columns = []

    for column in df.columns:

        lower_column = column.lower()

        if (
            "date" in lower_column
            or "time" in lower_column
            or "created" in lower_column
            or "timestamp" in lower_column
        ):

            possible_date_columns.append(
                column
            )

    date_report = []

    for column in possible_date_columns:

        total_non_missing = int(
            df[column]
            .apply(
                lambda value:
                not is_missing(value)
            )
            .sum()
        )

        valid_count, converted = valid_date_column(
            df[column]
        )

        invalid_count = max(
            total_non_missing - valid_count,
            0
        )

        date_report.append(
            {
                "Attribute": column,
                "Non-Missing": total_non_missing,
                "Valid Date/Time": valid_count,
                "Invalid Date/Time": invalid_count
            }
        )

    if date_report:

        st.dataframe(
            pd.DataFrame(
                date_report
            ),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No date/time attributes were detected."
        )


    # ------------------------------------------------------
    # CROSS SOURCE
    # ------------------------------------------------------

    st.markdown(
        "### 🔗 Cross-Source Consistency"
    )

    st.info(
        """
        The fused dataset combines different StudyNova activity
        sources. Therefore, every field is not expected to be
        populated for every record.

        Cross-source consistency is checked using common
        identifiers and user attributes rather than assuming
        all activity types contain identical fields.
        """
    )

    if "user_uid" in df.columns:

        # User name conflicts

        if "user_name" in df.columns:

            name_check = df[
                [
                    "user_uid",
                    "user_name"
                ]
            ].copy()

            name_check = name_check[
                ~name_check["user_uid"].apply(
                    is_missing
                )
            ]

            name_check["clean_name"] = (
                name_check["user_name"]
                .astype(str)
                .str.strip()
            )

            name_counts = (
                name_check
                .groupby("user_uid")[
                    "clean_name"
                ]
                .nunique()
            )

            conflicting_names = name_counts[
                name_counts > 1
            ]

            if not conflicting_names.empty:

                st.warning(
                    f"{len(conflicting_names)} user UID(s) "
                    "have multiple recorded names."
                )

            else:

                st.success(
                    "✅ No conflicting user names detected."
                )

        # User email conflicts

        if "user_email" in df.columns:

            email_check = df[
                [
                    "user_uid",
                    "user_email"
                ]
            ].copy()

            email_check = email_check[
                ~email_check["user_uid"].apply(
                    is_missing
                )
            ]

            email_check["clean_email"] = (
                email_check["user_email"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            email_counts = (
                email_check
                .groupby("user_uid")[
                    "clean_email"
                ]
                .nunique()
            )

            conflicting_emails = email_counts[
                email_counts > 1
            ]

            if not conflicting_emails.empty:

                st.warning(
                    f"{len(conflicting_emails)} user UID(s) "
                    "have multiple recorded email values."
                )

            else:

                st.success(
                    "✅ No conflicting user emails detected."
                )


# ==========================================================
# D4 OUTLIER ANALYSIS
# ==========================================================

with st.expander(
    "4️⃣ Outlier Detection — IQR Method",
    expanded=False
):

    st.markdown(
        """
        The **Interquartile Range (IQR)** method is used.

        **IQR = Q3 − Q1**

        **Lower Bound = Q1 − 1.5 × IQR**

        **Upper Bound = Q3 + 1.5 × IQR**
        """
    )

    outlier_candidates = []

    for column in numeric_candidates:

        values = numeric_series(
            df[column]
        ).dropna()

        if len(values) < 4:
            continue

        mask = iqr_outlier_mask(
            df[column]
        )

        count = int(
            mask.sum()
        )

        q1 = values.quantile(
            0.25
        )

        q3 = values.quantile(
            0.75
        )

        iqr = q3 - q1

        lower = q1 - (1.5 * iqr)

        upper = q3 + (1.5 * iqr)

        outlier_candidates.append(
            {
                "Attribute": column,
                "Q1": round(q1, 2),
                "Median": round(
                    values.median(),
                    2
                ),
                "Q3": round(q3, 2),
                "IQR": round(iqr, 2),
                "Lower Bound": round(
                    lower,
                    2
                ),
                "Upper Bound": round(
                    upper,
                    2
                ),
                "Outlier Count": count,
                "Outlier %": round(
                    (count / len(values)) * 100,
                    2
                )
            }
        )

    if outlier_candidates:

        outlier_df = pd.DataFrame(
            outlier_candidates
        ).sort_values(
            "Outlier Count",
            ascending=False
        )

        st.dataframe(
            outlier_df,
            use_container_width=True,
            hide_index=True
        )

        selected_outlier_column = st.selectbox(
            "Select numerical attribute for boxplot",
            numeric_candidates,
            key="outlier_boxplot_column"
        )

        plot_boxplot(
            df[selected_outlier_column],
            f"IQR Boxplot — {selected_outlier_column}"
        )

    else:

        st.info(
            "Not enough numerical data for IQR analysis."
        )

    st.markdown(
        "### 🧠 Outlier Interpretation"
    )

    st.info(
        """
        An IQR outlier is **not automatically a data error**.

        In StudyNova, an extreme observation may represent
        legitimate student activity.

        Examples:

        • A long question may represent a complex academic query.

        • A long answer may represent a detailed AI explanation.

        • A high YouTube result count may represent a valid API response.

        • A high activity count may represent intensive study.

        Therefore, outliers should be considered **valid observations
        unless they violate a known validation rule**.

        Values outside logical ranges, such as percentages below 0
        or above 100, are stronger candidates for data errors.
        """
    )


# ==========================================================
# PART E
# EXPLORATORY DATA ANALYSIS
# ==========================================================

st.divider()

st.header(
    "📈 Part E — Exploratory Data Analysis"
)

st.caption(
    "EDA focuses on variables actually available in the current "
    "AcademicNotesAI fused dataset."
)


# ==========================================================
# E1 UNIVARIATE
# ==========================================================

with st.expander(
    "1️⃣ Univariate Analysis",
    expanded=True
):

    st.markdown(
        """
        Numerical attributes are analyzed using mean, median,
        standard deviation, minimum, maximum, quartiles and
        distribution visualizations.
        """
    )

    if numeric_candidates:

        selected_univariate = st.selectbox(
            "Select numerical attribute",
            numeric_candidates,
            key="univariate_column"
        )

        selected_values = numeric_series(
            df[selected_univariate]
        ).dropna()

        if not selected_values.empty:

            q1 = selected_values.quantile(
                0.25
            )

            q3 = selected_values.quantile(
                0.75
            )

            summary_df = pd.DataFrame(
                {
                    "Statistic": [
                        "Mean",
                        "Median",
                        "Standard Deviation",
                        "Minimum",
                        "Q1 (25%)",
                        "Q3 (75%)",
                        "Maximum"
                    ],
                    "Value": [
                        round(
                            selected_values.mean(),
                            2
                        ),
                        round(
                            selected_values.median(),
                            2
                        ),
                        round(
                            selected_values.std(),
                            2
                        ),
                        round(
                            selected_values.min(),
                            2
                        ),
                        round(
                            q1,
                            2
                        ),
                        round(
                            q3,
                            2
                        ),
                        round(
                            selected_values.max(),
                            2
                        )
                    ]
                }
            )

            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True
            )

            chart_col1, chart_col2 = st.columns(
                2
            )

            with chart_col1:

                plot_histogram(
                    df[selected_univariate],
                    f"Distribution of {selected_univariate}"
                )

            with chart_col2:

                plot_boxplot(
                    df[selected_univariate],
                    f"Boxplot of {selected_univariate}"
                )

        else:

            st.info(
                "No usable numeric observations."
            )

    else:

        st.info(
            "No numerical attributes are currently available."
        )


# ==========================================================
# E2 BIVARIATE
# ==========================================================

with st.expander(
    "2️⃣ Bivariate Analysis",
    expanded=True
):

    st.markdown(
        """
        Bivariate analysis investigates relationships between
        meaningful variables in the fused dataset.
        """
    )

    if len(numeric_candidates) >= 2:

        bivariate_col1, bivariate_col2 = st.columns(
            2
        )

        with bivariate_col1:

            x_column = st.selectbox(
                "X-axis variable",
                numeric_candidates,
                key="bivariate_x"
            )

        with bivariate_col2:

            y_options = [
                column
                for column in numeric_candidates
                if column != x_column
            ]

            if not y_options:

                y_options = numeric_candidates

            y_column = st.selectbox(
                "Y-axis variable",
                y_options,
                key="bivariate_y"
            )

        plot_data = pd.DataFrame(
            {
                "x": numeric_series(
                    df[x_column]
                ),
                "y": numeric_series(
                    df[y_column]
                )
            }
        ).dropna()

        if len(plot_data) >= 2:

            correlation = (
                plot_data["x"]
                .corr(
                    plot_data["y"]
                )
            )

            metric_col1, metric_col2 = st.columns(
                2
            )

            with metric_col1:

                st.metric(
                    "Pearson Correlation",
                    f"{correlation:.3f}"
                )

            with metric_col2:

                if abs(correlation) >= 0.7:

                    strength = "Strong"

                elif abs(correlation) >= 0.4:

                    strength = "Moderate"

                elif abs(correlation) >= 0.2:

                    strength = "Weak"

                else:

                    strength = "Very Weak"

                st.metric(
                    "Relationship Strength",
                    strength
                )

            fig, ax = plt.subplots(
                figsize=(9, 4.5)
            )

            ax.scatter(
                plot_data["x"],
                plot_data["y"],
                alpha=0.7
            )

            ax.set_xlabel(
                x_column
            )

            ax.set_ylabel(
                y_column
            )

            ax.set_title(
                f"{x_column} vs {y_column}"
            )

            ax.grid(
                alpha=0.2
            )

            fig.tight_layout()

            st.pyplot(
                fig,
                clear_figure=True
            )

            plt.close(fig)

            st.caption(
                """
                Pearson correlation ranges from -1 to +1.

                **+1** → strong positive relationship

                **-1** → strong negative relationship

                **0** → little/no linear relationship

                Correlation does not prove causation.
                """
            )

        else:

            st.info(
                "Not enough paired observations."
            )

    else:

        st.info(
            "At least two numerical attributes are required."
        )


# ==========================================================
# ACTIVITY TYPE VS NUMERICAL
# ==========================================================

if (
    "record_type" in df.columns
    and numeric_candidates
):

    st.markdown(
        "### 📚 Activity Type vs Numerical Variable"
    )

    group_numeric_column = st.selectbox(
        "Select numerical variable",
        numeric_candidates,
        key="activity_numeric_variable"
    )

    grouped_data = df.copy()

    grouped_data[
        group_numeric_column
    ] = numeric_series(
        grouped_data[
            group_numeric_column
        ]
    )

    grouped_data = grouped_data.dropna(
        subset=[
            group_numeric_column
        ]
    )

    if not grouped_data.empty:

        group_summary = (
            grouped_data
            .groupby(
                "record_type"
            )[
                group_numeric_column
            ]
            .agg(
                [
                    "count",
                    "mean",
                    "median",
                    "std"
                ]
            )
            .reset_index()
        )

        group_summary.columns = [
            "Activity Type",
            "Count",
            "Mean",
            "Median",
            "Std Dev"
        ]

        st.dataframe(
            group_summary.round(2),
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            group_summary.set_index(
                "Activity Type"
            )["Mean"]
        )


# ==========================================================
# API / ACTIVITY VARIABLES
# ==========================================================

st.markdown(
    "### 🔌 API / Activity Variables"
)

api_variable_descriptions = {

    "results_count":
        "Number of results returned by YouTube/API search",

    "message_count":
        "Number of chat messages",

    "activity_hour":
        "Hour at which learning activity occurred",

    "question_length":
        "Length of student's academic question",

    "answer_length":
        "Length of generated AI answer",

    "has_question":
        "Whether a question was recorded",

    "has_answer":
        "Whether an answer was recorded",

    "has_source":
        "Whether source information was available",

    "percentage":
        "Quiz percentage",

    "score":
        "Quiz score",

    "duration":
        "Activity duration",

    "views":
        "Number of views",

    "rating":
        "Rating associated with activity/resource",

    "reviews":
        "Number of reviews"
}

api_variables = [
    column
    for column in api_variable_descriptions
    if column in df.columns
]

if api_variables:

    api_df = pd.DataFrame(
        {
            "Activity/API Variable":
                api_variables,
            "Purpose": [
                api_variable_descriptions[
                    column
                ]
                for column in api_variables
            ]
        }
    )

    st.dataframe(
        api_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No recognized API/activity variables were found."
    )


# ==========================================================
# E3 MULTIVARIATE
# ==========================================================

with st.expander(
    "3️⃣ Multivariate Analysis",
    expanded=True
):

    st.markdown(
        """
        Multivariate analysis evaluates multiple numerical
        attributes together to identify broader patterns.
        """
    )

    if len(numeric_candidates) >= 2:

        correlation_data = df[
            numeric_candidates
        ].apply(
            pd.to_numeric,
            errors="coerce"
        )

        correlation_matrix = (
            correlation_data
            .corr()
        )

        st.markdown(
            "### 🔥 Correlation Heatmap"
        )

        figure_width = max(
            8,
            len(correlation_matrix.columns) * 0.7
        )

        figure_height = max(
            5,
            len(correlation_matrix.columns) * 0.55
        )

        fig, ax = plt.subplots(
            figsize=(
                figure_width,
                figure_height
            )
        )

        image = ax.imshow(
            correlation_matrix,
            aspect="auto",
            interpolation="nearest"
        )

        ax.set_xticks(
            range(
                len(
                    correlation_matrix.columns
                )
            )
        )

        ax.set_yticks(
            range(
                len(
                    correlation_matrix.columns
                )
            )
        )

        ax.set_xticklabels(
            correlation_matrix.columns,
            rotation=45,
            ha="right"
        )

        ax.set_yticklabels(
            correlation_matrix.columns
        )

        for i in range(
            len(
                correlation_matrix.index
            )
        ):

            for j in range(
                len(
                    correlation_matrix.columns
                )
            ):

                value = correlation_matrix.iloc[
                    i,
                    j
                ]

                if pd.notna(value):

                    ax.text(
                        j,
                        i,
                        f"{value:.2f}",
                        ha="center",
                        va="center"
                    )

        ax.set_title(
            "Correlation Heatmap"
        )

        fig.colorbar(
            image,
            ax=ax,
            fraction=0.046,
            pad=0.04
        )

        fig.tight_layout()

        st.pyplot(
            fig,
            clear_figure=True
        )

        plt.close(fig)

        st.markdown(
            """
            **Interpretation**

            Strong positive values indicate variables tend to
            increase together.

            Strong negative values indicate an inverse relationship.

            Values close to zero indicate weak linear association.

            Correlation should not be interpreted as causation.
            """
        )

    else:

        st.info(
            "At least two numerical variables are required."
        )


# ==========================================================
# GROUP-WISE MULTIVARIATE ANALYSIS
# ==========================================================

if (
    "record_type" in df.columns
    and len(numeric_candidates) >= 2
):

    st.markdown(
        "### 📚 Group-wise Activity Comparison"
    )

    default_variables = numeric_candidates[
        :min(
            3,
            len(numeric_candidates)
        )
    ]

    selected_group_variables = st.multiselect(
        "Select numerical variables",
        numeric_candidates,
        default=default_variables,
        key="groupwise_variables"
    )

    if selected_group_variables:

        groupwise = df.copy()

        for column in selected_group_variables:

            groupwise[column] = numeric_series(
                groupwise[column]
            )

        groupwise_summary = (
            groupwise
            .groupby(
                "record_type"
            )[
                selected_group_variables
            ]
            .mean()
            .round(2)
            .reset_index()
        )

        st.dataframe(
            groupwise_summary,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            groupwise_summary.set_index(
                "record_type"
            )
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