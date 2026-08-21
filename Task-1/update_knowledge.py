import os
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from docx import Document

# -----------------------------
# Folders
# -----------------------------

KNOWLEDGE_FOLDER = "knowledge"
VECTOR_DB_FOLDER = "vector_db"

# -----------------------------
# Load Embedding Model
# -----------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model Loaded Successfully!")

# -----------------------------
# Read TXT Files
# -----------------------------

def read_txt(filepath):

    with open(filepath, "r", encoding="utf-8") as file:

        return file.read()


# -----------------------------
# Read PDF Files
# -----------------------------

def read_pdf(filepath):

    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:

        if page.extract_text():

            text += page.extract_text() + "\n"

    return text


# -----------------------------
# Read DOCX Files
# -----------------------------

def read_docx(filepath):

    document = Document(filepath)

    text = ""

    for para in document.paragraphs:

        text += para.text + "\n"

    return text


# -----------------------------
# Load Knowledge Files
# -----------------------------

documents = []
filenames = []

print("Reading Knowledge Folder...")

for file in os.listdir(KNOWLEDGE_FOLDER):

    filepath = os.path.join(KNOWLEDGE_FOLDER, file)

    if file.endswith(".txt"):
        text = read_txt(filepath)

    elif file.endswith(".pdf"):
        text = read_pdf(filepath)

    elif file.endswith(".docx"):
        text = read_docx(filepath)

    else:
        continue

    # Split document into individual lines
    chunks = text.split("\n")

    for chunk in chunks:

        chunk = chunk.strip()

        if len(chunk) > 10:

            documents.append(chunk)

            filenames.append(file)

print(f"Loaded {len(documents)} knowledge chunks.")
# -----------------------------
# Create Embeddings
# -----------------------------

print("Creating Embeddings...")

embeddings = model.encode(documents)

embeddings = np.array(embeddings).astype("float32")

# -----------------------------
# Create FAISS Index
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# -----------------------------
# Save Vector Database
# -----------------------------

faiss.write_index(
    index,
    os.path.join(VECTOR_DB_FOLDER, "knowledge.index")
)

with open(
    os.path.join(VECTOR_DB_FOLDER, "documents.pkl"),
    "wb"
) as file:

    pickle.dump(documents, file)

with open(
    os.path.join(VECTOR_DB_FOLDER, "filenames.pkl"),
    "wb"
) as file:

    pickle.dump(filenames, file)

print("\nKnowledge Base Updated Successfully!")

print(f"Documents Indexed : {len(documents)}")