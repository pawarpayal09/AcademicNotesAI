import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
import streamlit as st
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

STORAGE_DIR = PROJECT_ROOT / "storage"

USERS_JSON_FILE = (
    STORAGE_DIR / "users.json"
)


# Your Firebase service-account JSON is outside
# the AcademicNotesAI project folder.
LOCAL_SERVICE_ACCOUNT_PATH = (
    PROJECT_ROOT.parent
    / "firebase_credentials"
    / "firebase_service_account.json"
)


# Optional fallback if the JSON is inside the project.
PROJECT_SERVICE_ACCOUNT_PATH = (
    PROJECT_ROOT
    / "firebase_credentials"
    / "firebase_service_account.json"
)


# ==========================================================
# FIREBASE AUTH REST URL
# ==========================================================

FIREBASE_AUTH_BASE_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts"
)


# ==========================================================
# DEFAULT USER STATS
# ==========================================================

DEFAULT_USER_STATS = {
    "total_questions": 0,
    "total_quizzes": 0,
    "quiz_score_sum": 0,
    "average_quiz_score": 0,
    "total_images": 0,
    "total_saved_notes": 0,
    "total_youtube_searches": 0,
}


# ==========================================================
# CREATE STORAGE DIRECTORY
# ==========================================================

def ensure_storage_directory():

    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


ensure_storage_directory()


# ==========================================================
# FIREBASE WEB API KEY
# ==========================================================

def get_firebase_api_key():
    """
    Priority:
    1. Streamlit Secrets
    2. Local .env
    """

    api_key = None

    # ------------------------------------------------------
    # Streamlit Cloud
    # ------------------------------------------------------

    try:

        api_key = st.secrets.get(
            "FIREBASE_API_KEY"
        )

    except Exception:

        api_key = None

    # ------------------------------------------------------
    # Local .env
    # ------------------------------------------------------

    if not api_key:

        api_key = os.getenv(
            "FIREBASE_API_KEY"
        )

    if api_key:

        api_key = str(
            api_key
        ).strip()

    return api_key


# ==========================================================
# SERVICE ACCOUNT INFORMATION
# ==========================================================

def get_service_account_info():
    """
    Get Firebase service-account information.

    Streamlit Cloud supports:

    FIREBASE_SERVICE_ACCOUNT_JSON = "..."

    OR:

    [FIREBASE_SERVICE_ACCOUNT]
    type = "service_account"
    ...

    Local development supports:

    FIREBASE_SERVICE_ACCOUNT_PATH
    external firebase_credentials folder
    project firebase_credentials folder
    """

    # ======================================================
    # OPTION 1 — JSON STRING IN STREAMLIT SECRETS
    # ======================================================

    try:

        secret_json = st.secrets.get(
            "FIREBASE_SERVICE_ACCOUNT_JSON"
        )

    except Exception:

        secret_json = None


    if secret_json:

        if isinstance(
            secret_json,
            str
        ):

            try:

                return json.loads(
                    secret_json
                )

            except json.JSONDecodeError as e:

                raise RuntimeError(
                    "FIREBASE_SERVICE_ACCOUNT_JSON "
                    "contains invalid JSON."
                ) from e


        if isinstance(
            secret_json,
            dict
        ):

            return dict(
                secret_json
            )


    # ======================================================
    # OPTION 2 — TOML SECTION IN STREAMLIT SECRETS
    # ======================================================

    try:

        secret_section = st.secrets.get(
            "FIREBASE_SERVICE_ACCOUNT"
        )

    except Exception:

        secret_section = None


    if secret_section:

        try:

            return dict(
                secret_section
            )

        except Exception as e:

            raise RuntimeError(
                "FIREBASE_SERVICE_ACCOUNT secret "
                "could not be read."
            ) from e


    # ======================================================
    # OPTION 3 — ENVIRONMENT PATH
    # ======================================================

    env_path = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_PATH"
    )


    if env_path:

        service_account_path = Path(
            env_path
        )

    # ======================================================
    # OPTION 4 — EXTERNAL LOCAL FILE
    # ======================================================

    elif LOCAL_SERVICE_ACCOUNT_PATH.exists():

        service_account_path = (
            LOCAL_SERVICE_ACCOUNT_PATH
        )

    # ======================================================
    # OPTION 5 — PROJECT LOCAL FILE
    # ======================================================

    else:

        service_account_path = (
            PROJECT_SERVICE_ACCOUNT_PATH
        )


    # ======================================================
    # CHECK FILE
    # ======================================================

    if not service_account_path.exists():

        raise FileNotFoundError(
            "Firebase service-account credentials "
            "were not found.\n\n"
            "Checked:\n"
            f"{LOCAL_SERVICE_ACCOUNT_PATH}\n"
            f"{PROJECT_SERVICE_ACCOUNT_PATH}\n"
            "and Streamlit Secrets."
        )


    # ======================================================
    # READ JSON FILE
    # ======================================================

    with open(
        service_account_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(
            file
        )


# ==========================================================
# INITIALIZE FIREBASE ADMIN SDK
# ==========================================================

@st.cache_resource(
    show_spinner=False
)
def initialize_firebase_admin():

    # Already initialized?
    if firebase_admin._apps:

        return firebase_admin.get_app()


    service_account_info = (
        get_service_account_info()
    )


    cred = credentials.Certificate(
        service_account_info
    )


    return firebase_admin.initialize_app(
        cred
    )


# ==========================================================
# FIRESTORE CLIENT
# ==========================================================

@st.cache_resource(
    show_spinner=False
)
def get_firestore_client():

    initialize_firebase_admin()

    return firestore.client()


# ==========================================================
# FIREBASE ERROR FORMATTER
# ==========================================================

def format_firebase_error(
    error_message
):

    error_message = str(
        error_message
    )


    error_map = {

        "EMAIL_EXISTS":
            "This email is already registered. "
            "Please login instead.",

        "EMAIL_NOT_FOUND":
            "No account was found with this email.",

        "INVALID_PASSWORD":
            "Incorrect password.",

        "INVALID_LOGIN_CREDENTIALS":
            "Incorrect email or password.",

        "INVALID_CREDENTIAL":
            "Incorrect email or password.",

        "USER_DISABLED":
            "This account has been disabled.",

        "WEAK_PASSWORD":
            "Password must contain at least 6 characters.",

        "OPERATION_NOT_ALLOWED":
            "Email/password authentication is not enabled "
            "in Firebase.",

        "TOO_MANY_ATTEMPTS_TRY_LATER":
            "Too many attempts. Please try again later.",

        "INVALID_EMAIL":
            "Please enter a valid email address.",

        "API_KEY_INVALID":
            "Firebase API key is invalid.",

        "PROJECT_NOT_FOUND":
            "Firebase project could not be found.",

        "USER_NOT_FOUND":
            "User account was not found.",

        "INVALID_ID_TOKEN":
            "Firebase login session is invalid. "
            "Please login again.",

        "TOKEN_EXPIRED":
            "Your login session has expired. "
            "Please login again.",
    }


    if error_message in error_map:

        return error_map[
            error_message
        ]


    for code, message in error_map.items():

        if code in error_message:

            return message


    return (
        "Firebase authentication failed. "
        "Please try again."
    )


# ==========================================================
# FIREBASE REST REQUEST
# ==========================================================

def firebase_auth_request(
    endpoint,
    payload
):

    api_key = get_firebase_api_key()


    if not api_key:

        return {
            "success": False,
            "error": (
                "FIREBASE_API_KEY is not configured."
            )
        }


    url = (
        f"{FIREBASE_AUTH_BASE_URL}"
        f":{endpoint}"
        f"?key={api_key}"
    )


    try:

        response = requests.post(
            url,
            json=payload,
            timeout=20
        )


    except requests.Timeout:

        return {
            "success": False,
            "error": (
                "Firebase request timed out. "
                "Please try again."
            )
        }


    except requests.RequestException as e:

        return {
            "success": False,
            "error": (
                "Unable to connect to Firebase. "
                f"{e}"
            )
        }


    # ------------------------------------------------------
    # Parse JSON
    # ------------------------------------------------------

    try:

        data = response.json()

    except ValueError:

        return {
            "success": False,
            "error": (
                "Firebase returned an invalid response."
            )
        }


    # ------------------------------------------------------
    # Firebase error
    # ------------------------------------------------------

    if response.status_code != 200:

        error_message = (
            data
            .get("error", {})
            .get(
                "message",
                "Firebase request failed."
            )
        )


        return {
            "success": False,
            "error": format_firebase_error(
                error_message
            ),
            "firebase_error": error_message
        }


    return {
        "success": True,
        "data": data
    }


# ==========================================================
# USERS JSON HELPERS
# ==========================================================

def load_users_json():
    """
    Load storage/users.json.

    If the file doesn't exist, it is created automatically.
    """

    ensure_storage_directory()


    # ------------------------------------------------------
    # Create file if missing
    # ------------------------------------------------------

    if not USERS_JSON_FILE.exists():

        with open(
            USERS_JSON_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4,
                ensure_ascii=False
            )


        return []


    # ------------------------------------------------------
    # Repair empty file
    # ------------------------------------------------------

    if USERS_JSON_FILE.stat().st_size == 0:

        with open(
            USERS_JSON_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4,
                ensure_ascii=False
            )


        return []


    # ------------------------------------------------------
    # Read file
    # ------------------------------------------------------

    try:

        with open(
            USERS_JSON_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )


        if isinstance(
            data,
            list
        ):

            return data


        return []


    except (
        json.JSONDecodeError,
        OSError
    ):

        # Repair invalid file

        with open(
            USERS_JSON_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4,
                ensure_ascii=False
            )


        return []


# ==========================================================
# CREATE USERS.JSON AUTOMATICALLY
# ==========================================================

# IMPORTANT:
# This call is intentionally AFTER load_users_json()
# has been defined.

load_users_json()


# ==========================================================
# SAVE USERS JSON
# ==========================================================

def save_users_json(
    users
):

    ensure_storage_directory()


    temporary_file = (
        STORAGE_DIR / "users.tmp"
    )


    with open(
        temporary_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            indent=4,
            ensure_ascii=False
        )


    os.replace(
        temporary_file,
        USERS_JSON_FILE
    )


# ==========================================================
# SAVE / UPDATE SINGLE USER
# ==========================================================

def save_user_to_json(
    uid,
    name,
    email,
    email_verified=False,
    disabled=False,
    created_at=None,
    last_login_at=None
):
    """
    Save user information to storage/users.json.

    Passwords are NEVER stored.
    """

    users = load_users_json()


    existing_user = None


    for user in users:

        if user.get(
            "uid"
        ) == uid:

            existing_user = user

            break


    user_data = {
        "uid": uid,
        "name": name,
        "email": email,
        "email_verified": bool(
            email_verified
        ),
        "disabled": bool(
            disabled
        ),
        "created_at": created_at,
        "last_login_at": last_login_at,
    }


    # Remove None values

    user_data = {
        key: value
        for key, value in user_data.items()
        if value is not None
    }


    # Update existing user

    if existing_user:

        existing_user.update(
            user_data
        )


    # Add new user

    else:

        users.append(
            user_data
        )


    save_users_json(
        users
    )


# ==========================================================
# TIMESTAMP HELPER
# ==========================================================

def datetime_from_timestamp(
    timestamp
):

    try:

        milliseconds = int(
            timestamp
        )


        seconds = (
            milliseconds / 1000
        )


        return datetime.fromtimestamp(
            seconds,
            timezone.utc
        ).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )


    except Exception:

        return str(
            timestamp
        )


# ==========================================================
# SYNC ALL FIREBASE USERS TO JSON
# ==========================================================

def sync_all_users_to_json():
    """
    Mirror Firebase Authentication users
    into storage/users.json.

    Passwords are never stored.
    """

    initialize_firebase_admin()


    users = []


    try:

        page = auth.list_users()


        while page:

            for user_record in page.users:

                user_metadata = (
                    user_record.user_metadata
                )


                created_at = None

                last_login_at = None


                if user_metadata:

                    creation_timestamp = getattr(
                        user_metadata,
                        "creation_timestamp",
                        None
                    )


                    last_sign_in_timestamp = getattr(
                        user_metadata,
                        "last_sign_in_timestamp",
                        None
                    )


                    if creation_timestamp:

                        created_at = (
                            datetime_from_timestamp(
                                creation_timestamp
                            )
                        )


                    if last_sign_in_timestamp:

                        last_login_at = (
                            datetime_from_timestamp(
                                last_sign_in_timestamp
                            )
                        )


                # Safe display name

                if user_record.display_name:

                    display_name = (
                        user_record.display_name
                    )

                elif user_record.email:

                    display_name = (
                        user_record.email.split("@")[0]
                    )

                else:

                    display_name = "Student"


                users.append(
                    {
                        "uid": user_record.uid,
                        "name": display_name,
                        "email": (
                            user_record.email
                            or ""
                        ),
                        "email_verified": bool(
                            user_record.email_verified
                        ),
                        "disabled": bool(
                            user_record.disabled
                        ),
                        "created_at": created_at,
                        "last_login_at": last_login_at,
                    }
                )


            page = page.get_next_page()


        save_users_json(
            users
        )


        return users


    except Exception as e:

        print(
            "Firebase users sync error:",
            type(e).__name__,
            str(e)
        )


        return []


# ==========================================================
# SIGN UP
# ==========================================================

def sign_up_user(
    name,
    email,
    password
):
    """
    Create Firebase email/password account.

    Also:
    - creates Firestore profile
    - creates/updates storage/users.json
    """

    name = str(
        name
    ).strip()


    email = str(
        email
    ).strip().lower()


    password = str(
        password
    )


    # ------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------

    if not name:

        return {
            "success": False,
            "error": "Please enter your full name."
        }


    if not email:

        return {
            "success": False,
            "error": "Please enter your email address."
        }


    if len(
        password
    ) < 6:

        return {
            "success": False,
            "error": (
                "Password must contain at least "
                "6 characters."
            )
        }


    # ------------------------------------------------------
    # FIREBASE SIGNUP
    # ------------------------------------------------------

    result = firebase_auth_request(
        "signUp",
        {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
    )


    if not result["success"]:

        return result


    data = result["data"]


    uid = data["localId"]

    id_token = data["idToken"]

    refresh_token = data.get(
        "refreshToken"
    )


    # ------------------------------------------------------
    # SAVE DISPLAY NAME IN FIREBASE AUTH
    # ------------------------------------------------------

    update_result = firebase_auth_request(
        "update",
        {
            "idToken": id_token,
            "displayName": name,
            "returnSecureToken": True
        }
    )


    if update_result["success"]:

        update_data = (
            update_result["data"]
        )


        id_token = update_data.get(
            "idToken",
            id_token
        )


        refresh_token = update_data.get(
            "refreshToken",
            refresh_token
        )


    # ------------------------------------------------------
    # CREATE FIRESTORE PROFILE
    # ------------------------------------------------------

    try:

        db = get_firestore_client()


        db.collection(
            "users"
        ).document(
            uid
        ).set(
            {
                "profile": {
                    "uid": uid,
                    "name": name,
                    "email": email
                },

                "stats": DEFAULT_USER_STATS
            },
            merge=True
        )


    except Exception as e:

        print(
            "Firestore profile error:",
            type(e).__name__,
            str(e)
        )


        st.warning(
            "Account created, but the Firestore "
            "profile could not be saved."
        )


    # ------------------------------------------------------
    # SAVE USER TO JSON
    # ------------------------------------------------------

    try:

        save_user_to_json(
            uid=uid,
            name=name,
            email=email,
            email_verified=False,
            disabled=False
        )


        # Sync all Firebase users

        sync_all_users_to_json()


    except Exception as e:

        print(
            "Local users.json error:",
            type(e).__name__,
            str(e)
        )


    return {
        "success": True,
        "uid": uid,
        "name": name,
        "email": email,
        "id_token": id_token,
        "refresh_token": refresh_token
    }


# ==========================================================
# LOGIN
# ==========================================================

def login_user(
    email,
    password
):
    """
    Login with Firebase email/password.
    """

    email = str(
        email
    ).strip().lower()


    password = str(
        password
    )


    # ------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------

    if not email:

        return {
            "success": False,
            "error": "Please enter your email."
        }


    if not password:

        return {
            "success": False,
            "error": "Please enter your password."
        }


    # ------------------------------------------------------
    # FIREBASE LOGIN
    # ------------------------------------------------------

    result = firebase_auth_request(
        "signInWithPassword",
        {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
    )


    if not result["success"]:

        return result


    data = result["data"]


    uid = data["localId"]

    id_token = data["idToken"]

    refresh_token = data.get(
        "refreshToken"
    )


    # ------------------------------------------------------
    # VERIFY FIREBASE ID TOKEN
    # ------------------------------------------------------

    try:

        initialize_firebase_admin()


        decoded_token = auth.verify_id_token(
            id_token
        )


        verified_uid = (
            decoded_token["uid"]
        )


        if verified_uid != uid:

            return {
                "success": False,
                "error": (
                    "Firebase user verification failed."
                )
            }


    except Exception as e:

        print(
            "Firebase token verification error:",
            type(e).__name__,
            str(e)
        )


        return {
            "success": False,
            "error": (
                "Unable to verify the Firebase "
                "login token."
            )
        }


    # ------------------------------------------------------
    # GET FIREBASE USER
    # ------------------------------------------------------

    try:

        firebase_user = auth.get_user(
            uid
        )


        display_name = (
            firebase_user.display_name
            or
            email.split("@")[0]
        )


        email_verified = bool(
            firebase_user.email_verified
        )


        disabled = bool(
            firebase_user.disabled
        )


        user_metadata = (
            firebase_user.user_metadata
        )


        created_at = None

        last_login_at = None


        if user_metadata:

            created_timestamp = getattr(
                user_metadata,
                "creation_timestamp",
                None
            )


            last_sign_in_timestamp = getattr(
                user_metadata,
                "last_sign_in_timestamp",
                None
            )


            if created_timestamp:

                created_at = (
                    datetime_from_timestamp(
                        created_timestamp
                    )
                )


            if last_sign_in_timestamp:

                last_login_at = (
                    datetime_from_timestamp(
                        last_sign_in_timestamp
                    )
                )


    except Exception as e:

        print(
            "Firebase user lookup error:",
            type(e).__name__,
            str(e)
        )


        display_name = (
            email.split("@")[0]
        )


        email_verified = False

        disabled = False

        created_at = None

        last_login_at = None


    # ------------------------------------------------------
    # ENSURE FIRESTORE PROFILE
    # ------------------------------------------------------

    try:

        db = get_firestore_client()


        user_ref = (
            db.collection(
                "users"
            ).document(
                uid
            )
        )


        user_document = (
            user_ref.get()
        )


        if not user_document.exists:

            user_ref.set(
                {
                    "profile": {
                        "uid": uid,
                        "name": display_name,
                        "email": email
                    },

                    "stats": DEFAULT_USER_STATS
                },
                merge=True
            )


        else:

            user_ref.set(
                {
                    "profile": {
                        "uid": uid,
                        "name": display_name,
                        "email": email
                    }
                },
                merge=True
            )


    except Exception as e:

        print(
            "Firestore login profile error:",
            type(e).__name__,
            str(e)
        )


    # ------------------------------------------------------
    # UPDATE USERS.JSON
    # ------------------------------------------------------

    try:

        save_user_to_json(
            uid=uid,
            name=display_name,
            email=email,
            email_verified=email_verified,
            disabled=disabled,
            created_at=created_at,
            last_login_at=last_login_at
        )


        sync_all_users_to_json()


    except Exception as e:

        print(
            "Local users.json update error:",
            type(e).__name__,
            str(e)
        )


    return {
        "success": True,
        "uid": uid,
        "name": display_name,
        "email": email,
        "id_token": id_token,
        "refresh_token": refresh_token
    }


# ==========================================================
# SESSION LOGIN
# ==========================================================

def set_current_user(
    user
):

    st.session_state.authenticated = True


    st.session_state.user_uid = (
        user["uid"]
    )


    st.session_state.user_name = (
        user["name"]
    )


    st.session_state.user_email = (
        user["email"]
    )


    st.session_state.firebase_id_token = (
        user["id_token"]
    )


    if user.get(
        "refresh_token"
    ):

        st.session_state.firebase_refresh_token = (
            user["refresh_token"]
        )


# ==========================================================
# AUTHENTICATION CHECK
# ==========================================================

def is_authenticated():

    return bool(
        st.session_state.get(
            "authenticated",
            False
        )
    )


# ==========================================================
# CURRENT USER
# ==========================================================

def get_current_user():

    if not is_authenticated():

        return None


    return {
        "uid": st.session_state.get(
            "user_uid"
        ),

        "name": st.session_state.get(
            "user_name"
        ),

        "email": st.session_state.get(
            "user_email"
        )
    }


# ==========================================================
# LOGOUT
# ==========================================================

def logout_user():

    keys_to_remove = [
        "authenticated",
        "user_uid",
        "user_name",
        "user_email",
        "firebase_id_token",
        "firebase_refresh_token"
    ]


    for key in keys_to_remove:

        st.session_state.pop(
            key,
            None
        )


# ==========================================================
# PROTECTED PAGE HELPER
# ==========================================================

def require_login(
    login_page="pages/Login.py"
):

    if not is_authenticated():

        st.warning(
            "🔐 Please login to access this feature."
        )


        st.switch_page(
            login_page
        )


        st.stop()


# ==========================================================
# GET USER DOCUMENT
# ==========================================================

def get_user_document():

    if not is_authenticated():

        return None


    uid = st.session_state.get(
        "user_uid"
    )


    if not uid:

        return None


    db = get_firestore_client()


    return (
        db.collection(
            "users"
        ).document(
            uid
        )
    )


# ==========================================================
# GET USER PROFILE
# ==========================================================

def get_user_profile():

    user_ref = get_user_document()


    if user_ref is None:

        return None


    document = user_ref.get()


    if not document.exists:

        return None


    data = document.to_dict()


    return data.get(
        "profile",
        {}
    )


# ==========================================================
# GET USER STATS
# ==========================================================

def get_user_stats():

    user_ref = get_user_document()


    if user_ref is None:

        return DEFAULT_USER_STATS.copy()


    document = user_ref.get()


    if not document.exists:

        return DEFAULT_USER_STATS.copy()


    data = document.to_dict()


    stats = data.get(
        "stats",
        {}
    )


    result = (
        DEFAULT_USER_STATS.copy()
    )


    result.update(
        stats
    )


    return result


# ==========================================================
# PASSWORD RESET
# ==========================================================

def send_password_reset(
    email
):

    api_key = get_firebase_api_key()


    if not api_key:

        return {
            "success": False,
            "error": (
                "FIREBASE_API_KEY is not configured."
            )
        }


    url = (
        f"{FIREBASE_AUTH_BASE_URL}"
        f":sendOobCode"
        f"?key={api_key}"
    )


    try:

        response = requests.post(
            url,
            json={
                "requestType": "PASSWORD_RESET",
                "email": (
                    str(email)
                    .strip()
                    .lower()
                )
            },
            timeout=20
        )


        data = response.json()


        if response.status_code != 200:

            error_message = (
                data
                .get("error", {})
                .get(
                    "message",
                    "Unable to send password reset email."
                )
            )


            return {
                "success": False,
                "error": format_firebase_error(
                    error_message
                )
            }


        return {
            "success": True,
            "error": None
        }


    except requests.RequestException as e:

        return {
            "success": False,
            "error": (
                f"Password reset error: {e}"
            )
        }