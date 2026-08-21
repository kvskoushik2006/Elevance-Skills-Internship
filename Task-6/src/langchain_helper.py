import os
import pandas as pd
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# -----------------------------
# Load Customer Service Dataset
# -----------------------------

DATASET_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "dataset.csv"
)

df = pd.read_csv(DATASET_PATH)


# Convert dataset into text documents
documents = []

for _, row in df.iterrows():
    text = f"""
Question: {row['question']}
Answer: {row['answer']}
"""
    documents.append(text)


# -----------------------------
# Create Embeddings
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------
# Create FAISS Vector Database
# -----------------------------

vector_db = FAISS.from_texts(
    documents,
    embedding=embeddings
)


# -----------------------------
# Create Gemini LLM
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)


# -----------------------------
# Prompt Template
# -----------------------------

prompt = PromptTemplate(
    template="""
You are a helpful customer service assistant.

Use the following context to answer the customer's question.

CONTEXT:
{context}

QUESTION:
{question}

Instructions:
- Answer clearly and naturally.
- Use only the information available in the context.
- Do not invent information.
- If the information is not available, say that you do not have enough information.
- Keep the answer concise.

ANSWER:
""",
    input_variables=["context", "question"]
)


# -----------------------------
# Answer Function
# -----------------------------

def get_answer(question):

    # Retrieve relevant documents
    retriever = vector_db.as_retriever(
        search_kwargs={"k": 3}
    )

    relevant_documents = retriever.invoke(question)

    # Combine retrieved context
    context = "\n\n".join(
        document.page_content
        for document in relevant_documents
    )

    # Create final prompt
    final_prompt = prompt.format(
        context=context,
        question=question
    )

    # Generate response
    response = llm.invoke(final_prompt)

    return response.content