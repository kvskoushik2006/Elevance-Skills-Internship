import streamlit as st

from multilingual_helper import (
    multilingual_answer,
    SUPPORTED_LANGUAGES
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multilingual Customer Service Chatbot",
    page_icon="🌍",
    layout="centered"
)


# ============================================================
# HEADER
# ============================================================

st.title("🌍 Multilingual Customer Service Chatbot")

st.write(
    "Ask questions in English, Hindi, Telugu, or Spanish. "
    "The chatbot automatically detects your language, "
    "understands context, and responds in the same language."
)


# ============================================================
# CONVERSATION MEMORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🌐 Supported Languages")

    for code, language in SUPPORTED_LANGUAGES.items():
        st.write(f"• {language}")

    st.divider()

    st.write(
        "You can switch languages at any point "
        "during the same conversation."
    )

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# DISPLAY PREVIOUS CONVERSATION
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if (
            message["role"] == "assistant"
            and "language" in message
        ):

            language_name = SUPPORTED_LANGUAGES.get(
                message["language"],
                "English"
            )

            st.caption(
                f"Detected language: {language_name}"
            )

        st.write(message["content"])


# ============================================================
# USER INPUT
# ============================================================

user_question = st.chat_input(
    "Type your question in any supported language..."
)


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if user_question:

    # Save previous conversation BEFORE adding
    # the current question.
    previous_conversation = (
        st.session_state.messages.copy()
    )

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):
        st.write(user_question)

    # --------------------------------------------------------
    # Generate multilingual answer
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🌍 Understanding your language and context..."
        ):

            answer, detected_language = multilingual_answer(
                user_question,
                previous_conversation
            )

        language_name = SUPPORTED_LANGUAGES.get(
            detected_language,
            "English"
        )

        st.caption(
            f"Detected language: {language_name}"
        )

        st.write(answer)

    # --------------------------------------------------------
    # Store conversation
    # --------------------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "language": detected_language
    })