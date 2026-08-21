from dotenv import load_dotenv
import os
import google.generativeai as genai

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# -----------------------------
# Gemini Model
# -----------------------------
model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


def get_chat_response(question, context=""):
    """
    Generate a text response using
    previous conversation context.
    """

    prompt = f"""
You are an intelligent Multi-Modal AI Assistant.

Previous Context:
{context}

Current User Question:
{question}

Instructions:

1. Use previous conversation if relevant.
2. If the question is unrelated, answer normally.
3. Keep answers accurate.
4. If unsure, clearly mention the uncertainty.
5. Be concise but informative.
"""

    response = model.generate_content(prompt)

    return response.text