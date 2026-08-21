class ResponseValidator:
    """
    Validates AI responses before they are shown to the user.
    """

    def validate(
        self,
        question,
        answer,
        image_available,
        decision
    ):

        question = question.lower()

        # ---------------------------------
        # 1. Image Required
        # ---------------------------------

        image_words = [
            "image",
            "photo",
            "picture",
            "car",
            "vehicle",
            "person",
            "dog",
            "cat",
            "tree",
            "building",
            "background",
            "color",
            "describe",
            "see"
        ]

        if not image_available:

            for word in image_words:

                if word in question:

                    return (
                        "⚠️ Please upload an image first "
                        "before asking image-related questions."
                    )

        # ---------------------------------
        # 2. Empty Response
        # ---------------------------------

        if answer is None:

            return (
                "I couldn't generate a response."
            )

        if len(answer.strip()) == 0:

            return (
                "The response was empty."
            )

        # ---------------------------------
        # 3. Very Short Response
        # ---------------------------------

        if len(answer.split()) < 3:

            answer += (
                "\n\n⚠️ The response is very short. "
                "Consider asking a more detailed question."
            )

        # ---------------------------------
        # 4. Ambiguous Question
        # ---------------------------------

        if decision == "clarify":

            return (
                "Could you please clarify your question? "
                "I'm not sure what 'it' refers to."
            )

        # ---------------------------------
        # 5. Normal Response
        # ---------------------------------

        return answer