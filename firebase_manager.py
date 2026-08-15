import json
import os
from pathlib import Path

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
# CONSTANTS
# ==========================================================

FIREBASE_AUTH_BASE_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts"
)

# Your service-account JSON is OUTSIDE AcademicNotesAI
LOCAL_SERVICE_ACCOUNT_PATH = (
    Path(__file__).resolve().parent.parent
    / "firebase_credentials"
    / "firebase_service_account.json"
)


# ==========================================================
# FIREBASE API KEY
# ==========================================================

def get_firebase_api_key():
    """
    Get the Firebase Web API key.

    Priority:
    1. Streamlit secrets
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

        api_key = str(api_key).strip()


    return api_key


# ==========================================================
# SERVICE ACCOUNT INFORMATION
# ==========================================================

def get_service_account_info():
    """
    Get the Firebase service-account JSON data.

    Local:
        D:\\MCA Sem 3\\LLM\\firebase_credentials\\
        firebase_service_account.json

    Streamlit Cloud:
        FIREBASE_SERVICE_ACCOUNT_JSON secret
    """

    # ------------------------------------------------------
    # Option 1: Streamlit secret as JSON string
    # ------------------------------------------------------

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

            except json.JSONDecodeError:

                raise RuntimeError(
                    "FIREBASE_SERVICE_ACCOUNT_JSON "
                    "contains invalid JSON."
                )

        if isinstance(
            secret_json,
            dict
        ):

            return dict(
                secret_json
            )


    # ------------------------------------------------------
    # Option 2: Explicit local environment path
    # ------------------------------------------------------

    env_path = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_PATH"
    )


    if env_path:

        service_account_path = Path(
            env_path
        )

    else:

        service_account_path = (
            LOCAL_SERVICE_ACCOUNT_PATH
        )


    # ------------------------------------------------------
    # Check local file
    # ------------------------------------------------------

    if not service_account_path.exists():

        raise FileNotFoundError(
            "Firebase service-account JSON was not found.\n\n"
            f"Expected path:\n"
            f"{service_account_path}"
        )


    # ------------------------------------------------------
    # Read JSON
    # ------------------------------------------------------

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

@st.cache_resource(show_spinner=False)
def initialize_firebase_admin():
    """
    Initialize Firebase Admin SDK once.

    Returns:
        Firebase Admin app
    """

    # Already initialized?
    if firebase_admin._apps:

        return firebase_admin.get_app()


    service_account_info = (
        get_service_account_info()
    )


    cred = credentials.Certificate(
        service_account_info
    )


    app = firebase_admin.initialize_app(
        cred
    )


    return app


# ==========================================================
# FIRESTORE CLIENT
# ==========================================================

@st.cache_resource(show_spinner=False)
def get_firestore_client():
    """
    Return the Firestore client.
    """

    initialize_firebase_admin()

    return firestore.client()


# ==========================================================
# FIREBASE ERROR MESSAGE
# ==========================================================

def format_firebase_error(error_message):
    """
    Convert Firebase API error codes into
    user-friendly messages.
    """

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
            "User account was not found."
    }


    # Exact match first

    if error_message in error_map:

        return error_map[
            error_message
        ]


    # Search inside longer Firebase errors

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
    """
    Send a request to Firebase Authentication REST API.
    """

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
            timeout=15
        )


    except requests.Timeout:

        return {
            "success": False,
            "error": (
                "Firebase request timed out. "
                "Please try again."
            )
        }


    except requests.RequestException:

        return {
            "success": False,
            "error": (
                "Unable to connect to Firebase. "
                "Please check your internet connection."
            )
        }


    # ------------------------------------------------------
    # Parse JSON response
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
# SIGN UP
# ==========================================================

def sign_up_user(
    name,
    email,
    password
):
    """
    Create a Firebase email/password account.

    Returns:
        success, uid, email, id_token
    """

    name = str(name).strip()
    email = str(email).strip().lower()
    password = str(password)


    # ------------------------------------------------------
    # Local validation
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


    if len(password) < 6:

        return {
            "success": False,
            "error": (
                "Password must contain at least "
                "6 characters."
            )
        }


    # ------------------------------------------------------
    # Firebase signup
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


    # ------------------------------------------------------
    # Save display name in Firebase Auth
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

        data = update_result["data"]

        id_token = data.get(
            "idToken",
            id_token
        )


    # ------------------------------------------------------
    # Create Firestore profile
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

                "stats": {
                    "total_questions": 0,
                    "total_quizzes": 0,
                    "average_quiz_score": 0,
                    "total_images": 0,
                    "total_saved_notes": 0,
                    "total_youtube_searches": 0
                }
            },
            merge=True
        )


    except Exception as e:

        print(
            "Firestore profile error:",
            type(e).__name__,
            str(e)
        )

        # Do not destroy a successful Firebase account
        # just because profile creation failed.

        st.warning(
            "Account created, but your profile "
            "could not be saved yet."
        )


    return {
        "success": True,
        "uid": uid,
        "name": name,
        "email": email,
        "id_token": id_token
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

    email = str(email).strip().lower()
    password = str(password)


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
    # Firebase login
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


    # ------------------------------------------------------
    # Verify Firebase ID token server-side
    # ------------------------------------------------------

    try:

        initialize_firebase_admin()

        decoded_token = (
            auth.verify_id_token(
                id_token
            )
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
    # Get user information
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


    except Exception:

        display_name = (
            email.split("@")[0]
        )


    # ------------------------------------------------------
    # Ensure user profile exists
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

                    "stats": {
                        "total_questions": 0,
                        "total_quizzes": 0,
                        "average_quiz_score": 0,
                        "total_images": 0,
                        "total_saved_notes": 0,
                        "total_youtube_searches": 0
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


    return {
        "success": True,
        "uid": uid,
        "name": display_name,
        "email": email,
        "id_token": id_token
    }


# ==========================================================
# SESSION LOGIN
# ==========================================================

def set_current_user(
    user
):
    """
    Store the authenticated user in Streamlit session state.
    """

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


# ==========================================================
# AUTHENTICATION CHECK
# ==========================================================

def is_authenticated():
    """
    Check whether this Streamlit session has
    an authenticated user.
    """

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
    """
    Return current authenticated user's session data.
    """

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
    """
    Clear authentication information from
    the current Streamlit session.
    """

    keys_to_remove = [
        "authenticated",
        "user_uid",
        "user_name",
        "user_email",
        "firebase_id_token"
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
    """
    Use this only inside protected pages.

    If the user is not logged in, redirect to Login.
    """

    if not is_authenticated():

        st.warning(
            "🔐 Please login to access this feature."
        )

        st.switch_page(
            login_page
        )

        st.stop()


# ==========================================================
# FIRESTORE USER DOCUMENT
# ==========================================================

def get_user_document():
    """
    Return the Firestore document reference
    belonging to the currently logged-in user.
    """

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
    """
    Get the current user's Firestore profile.
    """

    user_ref = get_user_document()


    if user_ref is None:

        return None


    document = (
        user_ref.get()
    )


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
    """
    Get current user's dashboard statistics.
    """

    user_ref = get_user_document()


    if user_ref is None:

        return {
            "total_questions": 0,
            "total_quizzes": 0,
            "average_quiz_score": 0,
            "total_images": 0,
            "total_saved_notes": 0,
            "total_youtube_searches": 0
        }


    document = (
        user_ref.get()
    )


    if not document.exists:

        return {
            "total_questions": 0,
            "total_quizzes": 0,
            "average_quiz_score": 0,
            "total_images": 0,
            "total_saved_notes": 0,
            "total_youtube_searches": 0
        }


    data = document.to_dict()


    return data.get(
        "stats",
        {
            "total_questions": 0,
            "total_quizzes": 0,
            "average_quiz_score": 0,
            "total_images": 0,
            "total_saved_notes": 0,
            "total_youtube_searches": 0
        }
    )

# ==========================================================
# SEND EMAIL VERIFICATION
# ==========================================================

def send_email_verification(id_token):
    """
    Send Firebase verification email.
    """

    api_key = get_firebase_api_key()

    if not api_key:
        return {
            "success": False,
            "error": "FIREBASE_API_KEY is not configured."
        }

    url = (
        f"https://identitytoolkit.googleapis.com/v1/"
        f"accounts:sendOobCode?key={api_key}"
    )

    try:

        response = requests.post(
            url,
            json={
                "requestType": "VERIFY_EMAIL",
                "idToken": id_token
            },
            timeout=15
        )

        data = response.json()

        if response.status_code != 200:

            error_message = (
                data
                .get("error", {})
                .get(
                    "message",
                    "Unable to send verification email."
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

    except Exception as e:

        return {
            "success": False,
            "error": f"Verification email error: {e}"
        }


# ==========================================================
# CHECK EMAIL VERIFICATION
# ==========================================================

def get_email_verification_status(id_token):
    """
    Check whether the current Firebase user
    has verified their email.
    """

    api_key = get_firebase_api_key()

    if not api_key:
        return False

    url = (
        f"https://identitytoolkit.googleapis.com/v1/"
        f"accounts:lookup?key={api_key}"
    )

    try:

        response = requests.post(
            url,
            json={
                "idToken": id_token
            },
            timeout=15
        )

        data = response.json()

        users = data.get("users", [])

        if not users:
            return False

        return bool(
            users[0].get(
                "emailVerified",
                False
            )
        )

    except Exception:
        return False


# ==========================================================
# SEND PASSWORD RESET EMAIL
# ==========================================================

def send_password_reset(email):
    """
    Send Firebase password reset email.
    """

    api_key = get_firebase_api_key()

    if not api_key:
        return {
            "success": False,
            "error": "FIREBASE_API_KEY is not configured."
        }

    url = (
        f"https://identitytoolkit.googleapis.com/v1/"
        f"accounts:sendOobCode?key={api_key}"
    )

    try:

        response = requests.post(
            url,
            json={
                "requestType": "PASSWORD_RESET",
                "email": email.strip().lower()
            },
            timeout=15
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

    except Exception as e:

        return {
            "success": False,
            "error": f"Password reset error: {e}"
        }

# ==========================================================
# SEND EMAIL VERIFICATION
# ==========================================================

def send_email_verification(id_token):

    api_key = get_firebase_api_key()

    if not api_key:

        return {
            "success": False,
            "error": "FIREBASE_API_KEY is not configured."
        }

    url = (
        "https://identitytoolkit.googleapis.com/v1/"
        f"accounts:sendOobCode?key={api_key}"
    )

    try:

        response = requests.post(
            url,
            json={
                "requestType": "VERIFY_EMAIL",
                "idToken": id_token
            },
            timeout=15
        )

        data = response.json()

        if response.status_code != 200:

            error_message = (
                data
                .get("error", {})
                .get(
                    "message",
                    "Unable to send verification email."
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
                f"Unable to send verification email: {e}"
            )
        }


# ==========================================================
# CHECK EMAIL VERIFICATION STATUS
# ==========================================================

def get_email_verification_status(id_token):

    api_key = get_firebase_api_key()

    if not api_key:
        return False

    url = (
        "https://identitytoolkit.googleapis.com/v1/"
        f"accounts:lookup?key={api_key}"
    )

    try:

        response = requests.post(
            url,
            json={
                "idToken": id_token
            },
            timeout=15
        )

        if response.status_code != 200:
            return False

        data = response.json()

        users = data.get(
            "users",
            []
        )

        if not users:
            return False

        return bool(
            users[0].get(
                "emailVerified",
                False
            )
        )

    except Exception:

        return False


# ==========================================================
# SEND PASSWORD RESET EMAIL
# ==========================================================

def send_password_reset(email):

    api_key = get_firebase_api_key()

    if not api_key:

        return {
            "success": False,
            "error": "FIREBASE_API_KEY is not configured."
        }

    url = (
        "https://identitytoolkit.googleapis.com/v1/"
        f"accounts:sendOobCode?key={api_key}"
    )

    try:

        response = requests.post(
            url,
            json={
                "requestType": "PASSWORD_RESET",
                "email": email.strip().lower()
            },
            timeout=15
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
                f"Unable to send password reset email: {e}"
            )
        }
