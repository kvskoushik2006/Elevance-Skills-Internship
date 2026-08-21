class ReasoningEngine:
    """
    Intelligent Decision-Making Engine

    Decides whether the assistant should:
    1. Analyze an uploaded image
    2. Use conversation memory
    3. Answer as a normal chatbot
    4. Ask the user for clarification
    """

    def __init__(self):

        # Keywords indicating image-related questions
        self.image_keywords = [
            "image",
            "photo",
            "picture",
            "upload",
            "show",
            "see",
            "look",
            "describe",
            "identify",
            "detect",
            "recognize",
            "car",
            "vehicle",
            "person",
            "man",
            "woman",
            "child",
            "dog",
            "cat",
            "animal",
            "tree",
            "building",
            "road",
            "background",
            "sky",
            "object",
            "color"
        ]

        # Ambiguous words
        self.ambiguous_words = [
            "it",
            "this",
            "that",
            "they",
            "them",
            "he",
            "she"
        ]

    def decide(self, question, image_available, memory):

        question = question.lower().strip()

        # ----------------------------
        # Rule 1 : Ambiguous Question
        # ----------------------------

        if question in self.ambiguous_words:

            return {
                "route": "clarify",
                "reason": "Ambiguous question."
            }

        # ----------------------------
        # Rule 2 : Image Question
        # ----------------------------

        if image_available:

            for keyword in self.image_keywords:

                if keyword in question:

                    return {
                        "route": "vision",
                        "reason": "Image analysis required."
                    }

        # ----------------------------
        # Rule 3 : Use Conversation Memory
        # ----------------------------

        if len(memory.get_conversation()) > 0:

            return {
                "route": "chat_memory",
                "reason": "Using previous conversation context."
            }

        # ----------------------------
        # Rule 4 : General Chat
        # ----------------------------

        return {
            "route": "chat",
            "reason": "General text conversation."
        }