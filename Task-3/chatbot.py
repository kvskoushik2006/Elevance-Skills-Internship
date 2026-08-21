import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("embeddings/faiss_index.index")

# Load processed documents
with open("embeddings/documents.pkl", "rb") as f:
    documents = pickle.load(f)


def search_medical_answer(user_question):
    """
    Searches the most relevant medical answer
    from the FAISS vector database.
    """

    query_embedding = model.encode(
        [user_question],
        convert_to_numpy=True
    ).astype(np.float32)

    distances, indices = index.search(query_embedding, 1)

    best_match = documents.iloc[indices[0][0]]

    return {
        "Focus": best_match["Focus"],
        "Question_Type": best_match["Question_Type"],
        "Question": best_match["Question"],
        "Answer": best_match["Answer"]
    }