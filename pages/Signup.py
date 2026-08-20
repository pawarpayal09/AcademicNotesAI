import os
import streamlit as st

from firebase_manager import (
    sign_up_user,
    set_current_user
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Signup | Academic Notes AI",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# LOAD SHARED CSS
# ==========================================================

def load_css():

    css_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "css",
        "style.css"
    )

    if os.path.exists(css_path):

        with open(
            css_path,
            "r",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


load_css()


# ==========================================================
# PAGE HEADER
# ==========================================================

st.markdown("## 🧑‍🎓 StudyNova")

st.caption(
    "Create your personal study account"
)

st.divider()


# ==========================================================
# SIGNUP CARD
# ==========================================================

with st.container(border=True):

    st.subheader(
        "📝 Create Your Account"
    )

    st.write(
        "Create an account to save your personal learning progress."
    )

    # ------------------------------------------------------
    # NAME
    # ------------------------------------------------------

    name = st.text_input(
        "👤 Full Name",
        placeholder="Enter your full name",
        key="signup_name"
    )

    # ------------------------------------------------------
    # EMAIL
    # ------------------------------------------------------

    email = st.text_input(
        "📧 Email Address",
        placeholder="Enter your email address",
        key="signup_email"
    )

    # ------------------------------------------------------
    # PASSWORD
    # ------------------------------------------------------

    password = st.text_input(
        "🔑 Password",
        type="password",
        placeholder="Minimum 6 characters",
        key="signup_password"
    )

    # ------------------------------------------------------
    # CONFIRM PASSWORD
    # ------------------------------------------------------

    confirm_password = st.text_input(
        "🔐 Confirm Password",
        type="password",
        placeholder="Re-enter your password",
        key="signup_confirm_password"
    )

    st.write("")

    # ------------------------------------------------------
    # CREATE ACCOUNT
    # ------------------------------------------------------

    if st.button(
        "🚀 Create Account",
        type="primary",
        use_container_width=True,
        key="signup_button"
    ):

        name_value = (
            name.strip()
        )

        email_value = (
            email.strip().lower()
        )


        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        if not name_value:

            st.warning(
                "⚠️ Please enter your full name."
            )

        elif not email_value:

            st.warning(
                "⚠️ Please enter your email address."
            )

        elif not password:

            st.warning(
                "⚠️ Please create a password."
            )

        elif len(password) < 6:

            st.warning(
                "⚠️ Password must contain at least 6 characters."
            )

        elif password != confirm_password:

            st.error(
                "❌ Passwords do not match."
            )

        else:

            with st.spinner(
                "📝 Creating your account..."
            ):

                result = sign_up_user(
                    name=name_value,
                    email=email_value,
                    password=password
                )


            if result["success"]:

                set_current_user(
                    result
                )

                st.success(
                    "✅ Account created successfully!"
                )

                st.switch_page(
                    "app.py"
                )

            else:

                st.error(
                    f"❌ {result['error']}"
                )


# ==========================================================
# LOGIN
# ==========================================================

st.divider()

st.caption(
    "Already have an account?"
)

if st.button(
    "🔐 Back to Login",
    use_container_width=True,
    key="go_login"
):

    st.switch_page(
        "pages/Login.py"
    )


# ==========================================================
# FOOTER
# ==========================================================

st.write("")

st.caption(
    "🔒 Secure authentication powered by Firebase"
)