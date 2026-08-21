from langdetect import detect, LangDetectException

from langchain_helper import get_answer, llm


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "es": "Spanish"
}


# ============================================================
# COMMON MIXED-LANGUAGE WORDS
# ============================================================

HINDI_MIXED_WORDS = {
    "mera", "meri", "mere", "mujhe", "mujhko",
    "aap", "aapka", "aapki", "kaise", "kahan",
    "kya", "kyun", "kab", "hai", "hain",
    "nahi", "nahin", "chahiye", "karna",
    "kar", "sakta", "sakti", "ho", "yeh",
    "woh", "iska", "uska"
}


TELUGU_MIXED_WORDS = {
    "naa", "naku", "nakku", "mee", "mi",
    "meeru", "ela", "ekkada", "enduku",
    "emiti", "enti", "eppudu", "undi",
    "unnadi", "cheyali", "cheyyali",
    "kavali", "ledu", "chesanu", "cheyyacha"
}


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_language(text):
    """
    Detect English, Hindi, Telugu, Spanish,
    and common Roman-script mixed-language input.
    """

    text_lower = text.lower()

    # --------------------------------------------------------
    # Unicode script detection
    # --------------------------------------------------------

    telugu_count = sum(
        "\u0C00" <= char <= "\u0C7F"
        for char in text
    )

    hindi_count = sum(
        "\u0900" <= char <= "\u097F"
        for char in text
    )

    if telugu_count > 0:
        return "te"

    if hindi_count > 0:
        return "hi"

    # --------------------------------------------------------
    # Roman mixed-language detection
    # --------------------------------------------------------

    words = set(
        text_lower
        .replace(",", " ")
        .replace(".", " ")
        .replace("?", " ")
        .replace("!", " ")
        .split()
    )

    hindi_matches = len(
        words.intersection(HINDI_MIXED_WORDS)
    )

    telugu_matches = len(
        words.intersection(TELUGU_MIXED_WORDS)
    )

    if hindi_matches >= 2:
        return "hi"

    if telugu_matches >= 2:
        return "te"

    if hindi_matches == 1 and any(
        word in words
        for word in {
            "mera",
            "meri",
            "mujhe",
            "aapka",
            "kaise",
            "kahan"
        }
    ):
        return "hi"

    if telugu_matches == 1 and any(
        word in words
        for word in {
            "naku",
            "meeru",
            "ela",
            "ekkada",
            "enduku"
        }
    ):
        return "te"

    # --------------------------------------------------------
    # Standard language detection
    # --------------------------------------------------------

    try:

        detected = detect(text)

        if detected in SUPPORTED_LANGUAGES:
            return detected

        return "en"

    except LangDetectException:
        return "en"


# ============================================================
# TRANSLATE QUESTION TO ENGLISH
# ============================================================

def translate_to_english(text, source_language):

    if source_language == "en":
        return text

    language_name = SUPPORTED_LANGUAGES[source_language]

    prompt = f"""
You are a multilingual customer service assistant.

Translate the following customer question into English.

The main language is {language_name}.

The input may contain English words mixed with
{language_name}. Understand the complete meaning.

IMPORTANT:
- Preserve the customer's exact intent.
- Do not add information.
- Do not remove information.
- Do not answer the question.
- Return ONLY the English translation.

Customer question:
{text}

English translation:
"""

    response = llm.invoke(prompt)

    return response.content.strip()


# ============================================================
# CONTEXT RESOLUTION
# ============================================================

def create_contextual_question(
    english_question,
    conversation_history
):

    if not conversation_history:
        return english_question

    history_text = ""

    for message in conversation_history[-8:]:

        role = message["role"]
        content = message["content"]

        history_text += f"{role}: {content}\n"

    prompt = f"""
You are the context-resolution component of a
multilingual customer service chatbot.

Previous conversation:
{history_text}

Latest customer question:
{english_question}

Rewrite the latest question into a clear
standalone English question when necessary.

Resolve references such as:
- it
- that
- this
- there
- my order
- the product
- the payment
- the tracking link

IMPORTANT:
- Preserve the customer's original intent.
- Use previous conversation to resolve ambiguity.
- Do not invent facts.
- Do not answer the question.
- Return ONLY the standalone question.

Standalone question:
"""

    response = llm.invoke(prompt)

    return response.content.strip()


# ============================================================
# GENERATE RESPONSE IN USER LANGUAGE
# ============================================================

def translate_from_english(
    english_answer,
    target_language
):

    if target_language == "en":
        return english_answer

    language_name = SUPPORTED_LANGUAGES[target_language]

    prompt = f"""
You are a professional multilingual customer service assistant.

Convert the following English answer into natural
{language_name}.

IMPORTANT:
- Preserve the exact meaning.
- Do not add facts.
- Do not remove facts.
- Keep numbers and important terms unchanged.
- Use natural conversational {language_name}.
- Return ONLY the final answer.
- Do not mention translation.

English answer:
{english_answer}

Final answer in {language_name}:
"""

    response = llm.invoke(prompt)

    return response.content.strip()


# ============================================================
# MAIN MULTILINGUAL PIPELINE
# ============================================================

def multilingual_answer(
    user_text,
    conversation_history=None
):

    if conversation_history is None:
        conversation_history = []

    # Empty input protection
    if not user_text or not user_text.strip():
        return (
            "Please enter a question.",
            "en"
        )

    # --------------------------------------------------------
    # Step 1: Detect language
    # --------------------------------------------------------

    detected_language = detect_language(user_text)

    # --------------------------------------------------------
    # Step 2: Translate to English
    # --------------------------------------------------------

    english_question = translate_to_english(
        user_text,
        detected_language
    )

    # --------------------------------------------------------
    # Step 3: Resolve conversation context
    # --------------------------------------------------------

    contextual_question = create_contextual_question(
        english_question,
        conversation_history
    )

    # --------------------------------------------------------
    # Step 4: Retrieve information using RAG
    # --------------------------------------------------------

    english_answer = get_answer(
        contextual_question
    )

    # --------------------------------------------------------
    # Step 5: Generate answer in detected language
    # --------------------------------------------------------

    final_answer = translate_from_english(
        english_answer,
        detected_language
    )

    return final_answer, detected_language