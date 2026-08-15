import os
import streamlit as st

from firebase_manager import (
    login_user,
    set_current_user,
    send_password_reset
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Login | Academic Notes AI",
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

st.markdown("## 📚 Academic Notes AI")

st.caption(
    "Your Personal AI Study Assistant"
)

st.divider()


# ==========================================================
# LOGIN CARD
# ==========================================================

with st.container(border=True):

    st.subheader(
        "🔐 Welcome Back"
    )

    st.write(
        "Login to continue to your personalized study workspace."
    )

    # ------------------------------------------------------
    # EMAIL
    # ------------------------------------------------------

    email = st.text_input(
        "📧 Email Address",
        placeholder="Enter your email address",
        key="login_email"
    )

    # ------------------------------------------------------
    # PASSWORD
    # ------------------------------------------------------

    password = st.text_input(
        "🔑 Password",
        type="password",
        placeholder="Enter your password",
        key="login_password"
    )

    st.write("")

    # ------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------

    if st.button(
        "🔐 Login",
        type="primary",
        use_container_width=True,
        key="login_button"
    ):

        email_value = (
            email.strip().lower()
        )

        if not email_value:

            st.warning(
                "⚠️ Please enter your email address."
            )

        elif not password:

            st.warning(
                "⚠️ Please enter your password."
            )

        else:

            with st.spinner(
                "🔐 Signing you in..."
            ):

                result = login_user(
                    email_value,
                    password
                )


            if result["success"]:

                set_current_user(
                    result
                )

                st.success(
                    "✅ Login successful!"
                )

                st.switch_page(
                    "app.py"
                )

            else:

                st.error(
                    f"❌ {result['error']}"
                )


# ==========================================================
# FORGOT PASSWORD
# ==========================================================

st.divider()

st.subheader(
    "🔑 Forgot Password?"
)

st.caption(
    "Enter your registered email and we'll send a reset link."
)

reset_email = st.text_input(
    "Reset Email",
    placeholder="your@email.com",
    key="reset_email",
    label_visibility="collapsed"
)

if st.button(
    "📧 Send Reset Email",
    use_container_width=True,
    key="send_reset_email"
):

    reset_email_value = (
        reset_email.strip().lower()
    )

    if not reset_email_value:

        st.warning(
            "⚠️ Please enter your email address."
        )

    else:

        with st.spinner(
            "📧 Sending password reset email..."
        ):

            reset_result = send_password_reset(
                reset_email_value
            )

        if reset_result["success"]:

            st.success(
                "✅ Password reset email sent. "
                "Please check your inbox."
            )

        else:

            st.error(
                f"❌ {reset_result['error']}"
            )


# ==========================================================
# SIGNUP
# ==========================================================

st.divider()

st.caption(
    "Don't have an account?"
)

if st.button(
    "📝 Create New Account",
    use_container_width=True,
    key="go_signup"
):

    st.switch_page(
        "pages/Signup.py"
    )


# ==========================================================
# FOOTER
# ==========================================================

st.write("")

st.caption(
    "🔒 Secure authentication powered by Firebase"
)