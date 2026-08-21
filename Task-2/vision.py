from dotenv import load_dotenv
import os
import google.generativeai as genai

# -------------------------------
# Load Environment Variables
# -------------------------------

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# -------------------------------
# Gemini Vision Model
# -------------------------------

vision_model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


# -------------------------------
# Analyze Uploaded Image
# -------------------------------

def analyze_image(question, image):
    """
    Analyze the uploaded image based on the user's question.
    """

    prompt = f"""
You are an intelligent Multi-Modal AI Vision Assistant.

Carefully analyze the uploaded image.

Instructions:
- Answer ONLY using visual evidence from the image.
- Do not assume facts that are not visible.
- If the answer cannot be determined, clearly say so.
- Keep the answer accurate and concise.

User Question:
{question}
"""

    try:

        response = vision_model.generate_content(
            [prompt, image]
        )

        if response.text:
            return response.text

        return "I couldn't analyze the image."

    except Exception as e:

        return f"Vision Error: {str(e)}"


# -------------------------------
# Generate Image Summary
# -------------------------------

def generate_image_summary(image):
    """
    Generate a concise summary of the uploaded image.
    The summary is stored in conversation memory.
    """

    prompt = """
Analyze this image and provide a short summary.

Include:
- Main objects
- Scene/environment
- Important colors
- People or animals (if any)
- Activities (if any)

Keep the summary under 80 words.
"""

    try:

        response = vision_model.generate_content(
            [prompt, image]
        )

        if response.text:
            return response.text

        return "No image summary available."

    except Exception:

        return "Unable to generate image summary."