import streamlit as st
from speech import speech_to_text


st.set_page_config(
    page_title="Speech to Text Test",
    page_icon="🎤"
)
# =====================================================
# LARGE MICROPHONE BUTTON
# =====================================================

st.markdown("""
<style>

div[data-testid="stAudioInput"] button {
    width: 100px !important;
    height: 100px !important;
    border-radius: 50% !important;
    font-size: 35px !important;
}

div[data-testid="stAudioInput"] {
    display: flex;
    justify-content: center;
    margin: 25px 0;
}

</style>
""", unsafe_allow_html=True)

st.title("🎤 Speech-to-Text Test")

st.write(
    "Click the microphone button and speak your question."
)

audio = st.audio_input(
    "🎤 Start Speaking"
)

if audio:

    st.success("🎧 Voice recording received!")

    st.audio(audio)

    with st.spinner("🔄 Converting your voice into text..."):

        text = speech_to_text(audio)

    if text:

        st.success("✅ Speech converted successfully!")

        st.subheader("📝 Recognized Question")

        st.info(text)

    else:

        st.error(
            "❌ Could not understand the voice. "
            "Please try again."
        )