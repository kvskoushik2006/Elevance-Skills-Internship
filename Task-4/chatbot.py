import ollama


class ResearchChatbot:
    def __init__(self, search_engine, model="llama3.2:3b"):
        self.search_engine = search_engine
        self.model = model
        self.conversation_history = []

    def search_papers(self, query, top_k=5):
        """
        Search the FAISS index for relevant research papers.
        """
        try:
            results = self.search_engine.search(query, top_k)

            if not results:
                return []

            return results

        except Exception as e:
            print("Search error:", e)
            return []

    def build_context(self, papers):
        """
        Convert retrieved papers into context for the LLM.
        """
        context = ""

        for i, paper in enumerate(papers, start=1):
            title = paper.get("title", "Unknown title")
            abstract = paper.get("abstract", "No abstract available")
            categories = paper.get("categories", "")

            context += f"""
Paper {i}
Title: {title}
Categories: {categories}
Abstract: {abstract}

"""

        return context

    def generate_response(self, question, papers):
        """
        Generate an answer using the local Ollama LLM.
        """

        context = self.build_context(papers)

        prompt = f"""
You are an expert research assistant specializing in Computer Science.

Use the research papers provided below to answer the user's question.

IMPORTANT RULES:
1. Give accurate and understandable explanations.
2. Use the retrieved papers as the main source of information.
3. If the papers do not contain enough information, clearly say so.
4. Do not invent paper titles, authors, results, or facts.
5. Explain complex concepts in simple language when appropriate.
6. For technical questions, provide structured explanations.
7. For follow-up questions, use the previous conversation context.

RESEARCH PAPERS:
{context}

USER QUESTION:
{question}

Provide a clear and useful answer.
"""

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful Computer Science research assistant "
                    "that explains scientific papers and technical concepts."
                ),
            }
        ]

        # Add previous conversation
        messages.extend(self.conversation_history[-6:])

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
            )

            answer = response["message"]["content"]

            # Store conversation
            self.conversation_history.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            self.conversation_history.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            return answer

        except Exception as e:
            return f"LLM Error: {str(e)}"

    def ask(self, question, top_k=5):
        """
        Complete pipeline:
        Question → FAISS search → Context → Ollama → Answer
        """

        papers = self.search_papers(question, top_k)

        if not papers:
            return {
                "answer": "I could not find relevant research papers for this question.",
                "papers": [],
            }

        answer = self.generate_response(question, papers)

        return {
            "answer": answer,
            "papers": papers,
        }

    def clear_history(self):
        """
        Clear conversation memory.
        """
        self.conversation_history = []