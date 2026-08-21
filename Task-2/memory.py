class ConversationMemory:
    def __init__(self):
        # Stores conversation history
        self.history = []

        # Stores information about the uploaded image
        self.image_summary = None

    def add_message(self, role, message):
        """
        Store a conversation message.
        """
        self.history.append({
            "role": role,
            "message": message
        })

    def get_conversation(self, limit=10):
        """
        Return the latest conversation messages.
        """
        return self.history[-limit:]

    def set_image_summary(self, summary):
        """
        Save image description once.
        """
        self.image_summary = summary

    def get_image_summary(self):
        """
        Return stored image summary.
        """
        return self.image_summary

    def get_context(self):

        context = ""

        if self.image_summary:
            context += f"""
Image Context:
{self.image_summary}

"""

        if self.history:

            context += "Conversation History:\n"

            for item in self.history[-10:]:

                context += f"{item['role']}: {item['message']}\n"

        return context

    def clear(self):
        """
        Clear all stored memory.
        """
        self.history = []
        self.image_summary = None