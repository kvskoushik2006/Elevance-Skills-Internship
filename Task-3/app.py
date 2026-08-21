import streamlit as st
from chatbot import search_medical_answer
from entity_recognition import extract_medical_entities

st.set_page_config(
    page_title="Medical QA Chatbot",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Medical Question Answering Chatbot")
st.write("Ask any medical question from the MedQuAD dataset.")

question = st.text_input(
    "Enter your medical question",
    placeholder="Example: What are the symptoms of Chronic Myelogenous Leukemia?"
)

if st.button("Get Answer"):

    if question.strip() == "":
        st.warning("Please enter a medical question.")

    else:

        entity = extract_medical_entities(question)

        result = search_medical_answer(question)

        st.divider()

        st.subheader("Detected Information")

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"**Disease:** {entity['Disease']}")

        with col2:
            st.info(f"**Question Type:** {entity['Question_Type']}")

        st.subheader("Matched Question")

        st.write(result["Question"])

        st.subheader("Answer")

        st.write(result["Answer"])

st.divider()

st.caption(
    "This chatbot is for educational purposes only. "
    "Please consult a qualified healthcare professional for medical advice."
)