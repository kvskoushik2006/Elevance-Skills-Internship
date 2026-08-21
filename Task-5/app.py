import streamlit as st
from sentiment_analysis import analyze_sentiment


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Sentiment Analysis Chatbot",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">🤖 Sentiment Analysis Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'A chatbot that understands customer emotions '
    'and responds appropriately.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("🧠 Sentiment Analysis")

    st.write(
        "This chatbot detects the sentiment "
        "of every user message."
    )

    st.write("😊 Positive")
    st.write("😐 Neutral")
    st.write("😟 Negative")

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# DISPLAY PREVIOUS MESSAGES
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_message = st.chat_input(
    "Type your message..."
)


# --------------------------------------------------
# PROCESS USER MESSAGE
# --------------------------------------------------

if user_message:

    # Detect sentiment
    sentiment, scores = analyze_sentiment(user_message)


    # ----------------------------------------------
    # SELECT APPROPRIATE RESPONSE
    # ----------------------------------------------

    if sentiment == "Positive":

        emoji = "😊"

        response = (
            "That's wonderful to hear! 😊 "
            "I'm glad you're having a positive experience. "
            "How can I help you today?"
        )

    elif sentiment == "Negative":

        emoji = "😟"

        response = (
            "I'm sorry to hear that you're having a "
            "difficult experience. 😟 "
            "I understand your concern, and I'm here "
            "to help you. Please tell me more about "
            "the problem."
        )

    else:

        emoji = "😐"

        response = (
            "Thanks for your message. "
            "I'm here to help. How can I assist you?"
        )


    # ----------------------------------------------
    # DISPLAY USER MESSAGE
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):

        st.markdown(user_message)


    # ----------------------------------------------
    # DISPLAY BOT RESPONSE
    # ----------------------------------------------

    with st.chat_message("assistant"):

        st.markdown(
            f"**Detected Sentiment:** "
            f"{emoji} {sentiment}"
        )

        st.markdown(response)


    # ----------------------------------------------
    # SAVE BOT RESPONSE
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": (
                f"**Detected Sentiment:** "
                f"{emoji} {sentiment}\n\n"
                f"{response}"
            )
        }
    )


# --------------------------------------------------
# SENTIMENT INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("📊 How it works")

st.write(
    "The chatbot analyzes each message using VADER "
    "sentiment analysis and classifies it as "
    "Positive, Negative, or Neutral. "
    "The response is then adapted according to "
    "the detected emotion."
)