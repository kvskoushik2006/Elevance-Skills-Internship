
import streamlit as st
from PIL import Image

from chat import get_chat_response
from vision import analyze_image, generate_image_summary
from memory import ConversationMemory
from reasoning import ReasoningEngine
from validator import ResponseValidator

st.set_page_config(
    page_title="🤖 Multi-Modal AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Multi-Modal AI Assistant")
st.caption("AI-powered assistant with Text, Vision, Memory, Reasoning and Validation.")
st.divider()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "reasoner" not in st.session_state:
    st.session_state.reasoner = ReasoningEngine()

if "validator" not in st.session_state:
    st.session_state.validator = ResponseValidator()

st.sidebar.title("🤖 AI Assistant")
st.sidebar.subheader("📷 Upload Image")

uploaded_file = st.sidebar.file_uploader(
    "Choose an image",
    type=["jpg","jpeg","png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.session_state.uploaded_image = image
    try:
        summary = generate_image_summary(image)
        st.session_state.memory.set_image_summary(summary)
        st.sidebar.success("✅ Image uploaded successfully")
    except Exception as e:
        st.sidebar.warning(f"Image summary unavailable: {e}")

if st.sidebar.button("🗑 Clear Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.session_state.memory.clear()
    st.session_state.uploaded_image = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("✨ Features")
for item in [
    "💬 Text Chat",
    "🖼 Image Analysis",
    "🧠 Conversation Memory",
    "🤖 Intelligent Reasoning",
    "✅ Response Validation"
]:
    st.sidebar.success(item)

st.sidebar.markdown("---")
st.sidebar.info("🟢 AI Ready")

m1,m2,m3 = st.columns(3)
m1.metric("💬 Messages", len(st.session_state.chat_history))
m2.metric("🖼 Image","Yes" if st.session_state.uploaded_image else "No")
m3.metric("🧠 Memory","ON")
st.divider()

left,right = st.columns([2,1])

with left:
    st.subheader("💬 Chat with AI")
    prompt = st.text_input("💬 Ask anything...")
    submit = st.button("🚀 Ask AI", use_container_width=True)

with right:
    st.subheader("🖼 Uploaded Image")
    if st.session_state.uploaded_image:
        st.image(st.session_state.uploaded_image, use_container_width=True)
    else:
        st.info("No image uploaded.")

if submit and prompt:
    with st.spinner("🤖 Thinking..."):
        try:
            decision = st.session_state.reasoner.decide(
                prompt,
                st.session_state.uploaded_image is not None,
                st.session_state.memory
            )

            if decision["route"] == "vision":
                answer = analyze_image(prompt, st.session_state.uploaded_image)

            elif decision["route"] == "clarify":
                answer = "Could you clarify your question? I'm not sure what you're referring to."

            else:
                context = st.session_state.memory.get_context()
                answer = get_chat_response(prompt, context)

            answer = st.session_state.validator.validate(
                prompt,
                answer,
                st.session_state.uploaded_image is not None,
                decision["route"]
            )

        except Exception as e:
            answer = f"⚠️ Error: {e}"

        st.session_state.chat_history.append(("You", prompt))
        st.session_state.memory.add_message("User", prompt)

        st.session_state.chat_history.append(("Assistant", answer))
        st.session_state.memory.add_message("Assistant", answer)

st.divider()
st.subheader("📝 Conversation History")

for role,message in st.session_state.chat_history:
    with st.chat_message("user" if role=="You" else "assistant"):
        st.write(message)

st.divider()
st.caption("🤖 Multi-Modal AI Assistant | Powered by Google Gemini | Built with Streamlit")
