import streamlit as st
from pathlib import Path
from favourites_manager import load_favourites, remove_favourite

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Saved Notes",
    page_icon="📌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD CUSTOM CSS
# =====================================================

css_file = Path("css/style.css")

if css_file.exists():

    with open(css_file, "r", encoding="utf-8") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
# 📚 Academic Notes AI

### Learn Smarter with AI
""")

    st.divider()

    st.info("""
### 🤖 About

An AI-powered academic assistant that helps students:

- 📚 Search academic notes
- 📄 Chat with uploaded PDFs
- 🧠 Learn difficult concepts
- ⚡ Get instant answers
""")

    st.divider()

    st.markdown("### 🚀 Technologies")

    st.success("🤖 Google Gemini")
    st.success("🦜 LangChain")
    st.success("📚 FAISS")
    st.success("🧠 RAG")
    st.success("⚡ Streamlit")

    st.divider()

    st.markdown("### 👩‍💻 Developer")

    st.info("""
**Payal Pawar**

🎓 MCA Student

Academic Notes AI

Version 1.0
""")

# ==========================================
# Load Favorites
# ==========================================

favorites = load_favourites()

# Latest first
favorites = list(reversed(favorites))

# ==========================================
# Empty State
# ==========================================

if len(favorites) == 0:

    st.info("⭐ No favorite notes saved yet.")

    st.stop()

# ==========================================
# Header
# ==========================================

st.markdown("""
<div style="
padding:30px;
border-radius:20px;
background:linear-gradient(135deg,#2563EB,#4F46E5);
color:white;
box-shadow:0px 12px 28px rgba(0,0,0,.18);
text-align:center;
">

<h1>⭐ Saved Notes Library</h1>

<p style="font-size:18px;">

Quickly access every important AI answer you've saved.

</p>

</div>
""", unsafe_allow_html=True)

st.write("")

col1,col2,col3=st.columns(3)

with col1:
    st.metric(
        "📚 Saved Notes",
        len(favorites)
    )

with col2:

    latest = favorites[0]["date"] if favorites else "-"

    st.metric(
        "🕒 Latest Save",
        latest
    )

with col3:

    st.metric(
        "🤖 AI Model",
        "Gemini"
    )

st.divider()

search = st.text_input(
    "",
    placeholder="🔍 Search by question...",
    help="Search saved notes instantly"
)

st.divider()

# ==========================================
# Filter Saved Notes
# ==========================================

filtered = []

for fav in favorites:

    # Show everything when search box is empty
    if search.strip() == "":
        filtered.append(fav)

    # Otherwise filter by question
    elif search.lower() in fav["question"].lower():
        filtered.append(fav)

# ==========================================
# Initialize selected note
# ==========================================

if "selected_favorite" not in st.session_state:
    st.session_state.selected_favorite = None

# ==========================================
# Layout
# ==========================================

left, right = st.columns([1, 2])

# ==========================================
# LEFT PANEL
# ==========================================

with left:

    st.markdown("## 📚 Saved Notes")

    st.caption(f"Total Saved : {len(filtered)}")

    st.write("")

    if len(filtered) == 0:

        st.warning("No matching notes found.")

    for fav in filtered:

        with st.container(border=True):

            st.markdown(
                f"""
### 📘 {fav['question']}

📅 **{fav['date']}**
"""
            )

            col1, col2 = st.columns([3, 1])

            with col1:

                if st.button(
                    "📖 Open",
                    key=f"open_{fav['id']}",
                    use_container_width=True
                ):

                    st.session_state.selected_favorite = fav

            with col2:

                if st.button(
                    "🗑",
                    key=f"delete_{fav['id']}",
                    use_container_width=True
                ):

                    remove_favourite(fav["id"])

                    if (
                        st.session_state.selected_favorite
                        and
                        st.session_state.selected_favorite["id"] == fav["id"]
                    ):

                        st.session_state.selected_favorite = None

                    st.success("Removed successfully.")

                    st.rerun()

            st.write("")

# ==========================================
# RIGHT PANEL
# ==========================================

with right:

    if st.session_state.selected_favorite:

        fav = st.session_state.selected_favorite

        # ===================================
        # Hero Card
        # ===================================

        st.markdown("""
<div style="
padding:20px;
border-radius:18px;
background:linear-gradient(135deg,#2563EB,#4F46E5);
color:white;
box-shadow:0px 8px 20px rgba(0,0,0,.15);
">

<h2>🤖 AI Saved Answer</h2>

<p>
This answer has been saved for quick future reference.
</p>

</div>
""", unsafe_allow_html=True)

        st.write("")

        # ===================================
        # Question
        # ===================================

        st.markdown("## 📘 Question")

        st.info(fav["question"])

        st.write("")

        # ===================================
        # Answer
        # ===================================

        st.markdown("### 📚 AI Answer")

        st.markdown(
            f"""
        <div style="
        background:white;
        padding:22px;
        border-radius:18px;
        box-shadow:0px 8px 18px rgba(0,0,0,.08);
        line-height:1.8;
        font-size:16px;
        ">

        {fav["answer"]}

  
        """,
        unsafe_allow_html=True
        )

        st.write("")

        # ===================================
        # Sources
        # ===================================

        st.markdown("## 📄 Source Documents")

        if fav["sources"]:
            for src in fav["sources"]:

                st.markdown(
                    f"""
            <div style="
            padding:12px;
            margin-bottom:8px;
            border-radius:12px;
            background:#F8FAFC;
            border-left:5px solid #2563EB;
            ">

            📄 {src}

            </div>
            """,
            unsafe_allow_html=True
            )

        else:

            st.warning("No source documents available.")

        st.write("")

        # ===================================
        # Information Cards
        # ===================================

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "📅 Saved On",
                fav["date"]
            )

        with c2:

            st.metric(
                "🤖 Generated By",
                "Gemini AI"
            )

        st.write("")

        # ===================================
        # Remove Button
        # ===================================

        st.write("")

        if st.button(
            "🗑 Remove From Saved Notes",
            use_container_width=True,
            type="primary"
        ):

            remove_favourite(fav["id"])

            st.session_state.selected_favorite = None

            st.success("✅ Removed Successfully")

            st.rerun()

    else:

        st.markdown("""
<div style="
padding:60px;
text-align:center;
border:2px dashed #CBD5E1;
border-radius:18px;
background:#F8FAFC;
">

<h2>📚 No Note Selected</h2>

<p>
Choose any saved note from the left panel.

The complete AI answer will appear here.

</p>

</div>
""", unsafe_allow_html=True)

st.write("")

st.divider()

st.markdown(
    """
<div style="text-align:center;color:gray;padding:10px;">

Made with ❤️ using
<b>Gemini • LangChain • FAISS • Streamlit</b>

</div>
""",
unsafe_allow_html=True
)