import os
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


DATA_FILE = "data/arxiv_cs.csv"
VECTOR_STORE = "vector_store"
INDEX_FILE = os.path.join(VECTOR_STORE, "papers.index")
DATA_STORE = os.path.join(VECTOR_STORE, "papers.csv")

MODEL_NAME = "all-MiniLM-L6-v2"


class PaperSearchEngine:

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = None
        self.papers = None

    def load_data(self):
        """Load the Computer Science research papers."""

        self.papers = pd.read_csv(DATA_FILE)

        self.papers = self.papers.fillna("")

        print(f"Loaded {len(self.papers)} research papers.")

    def create_embeddings(self):
        """Create embeddings from paper title and abstract."""

        texts = (
            self.papers["title"].astype(str)
            + ". "
            + self.papers["abstract"].astype(str)
        ).tolist()

        print("Creating paper embeddings...")
        print("This may take several minutes.")

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        return np.asarray(embeddings, dtype="float32")

    def build_index(self):
        """Create and save the FAISS vector index."""

        os.makedirs(VECTOR_STORE, exist_ok=True)

        self.load_data()

        embeddings = self.create_embeddings()

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

        faiss.write_index(self.index, INDEX_FILE)

        self.papers.to_csv(DATA_STORE, index=False)

        print()
        print("FAISS index created successfully!")
        print(f"Number of vectors: {self.index.ntotal}")
        print(f"Index saved to: {INDEX_FILE}")
        print(f"Paper data saved to: {DATA_STORE}")

    def load_index(self):
        """Load an existing FAISS index."""

        if not os.path.exists(INDEX_FILE):
            raise FileNotFoundError(
                "FAISS index not found. Build the index first."
            )

        self.index = faiss.read_index(INDEX_FILE)

        self.papers = pd.read_csv(DATA_STORE).fillna("")

        print(f"Loaded FAISS index with {self.index.ntotal} papers.")

    def search(self, query, top_k=5):
        """Search for papers similar to the user's query."""

        if self.index is None or self.papers is None:
            self.load_index()

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            paper = self.papers.iloc[index].to_dict()

            paper["similarity_score"] = float(score)

            results.append(paper)

        return results