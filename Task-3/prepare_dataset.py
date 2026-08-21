import os
import pickle
import faiss
import pandas as pd
import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# -----------------------------
# Paths
# -----------------------------
DATASET_PATH = "data/MedQuAD"
CSV_PATH = "data/processed_medquad.csv"

EMBEDDING_FOLDER = "embeddings"
INDEX_PATH = os.path.join(EMBEDDING_FOLDER, "faiss_index.index")
DOCUMENT_PATH = os.path.join(EMBEDDING_FOLDER, "documents.pkl")

os.makedirs(EMBEDDING_FOLDER, exist_ok=True)

# -----------------------------
# Read XML Dataset
# -----------------------------
records = []

print("\nReading MedQuAD Dataset...\n")

for root, dirs, files in os.walk(DATASET_PATH):

    for file in tqdm(files):

        if not file.endswith(".xml"):
            continue

        filepath = os.path.join(root, file)

        try:

            tree = ET.parse(filepath)
            root_element = tree.getroot()

            focus = root_element.findtext("Focus", default="Unknown")

            qa_pairs = root_element.find("QAPairs")

            if qa_pairs is None:
                continue

            for qa in qa_pairs.findall("QAPair"):

                question = qa.find("Question")
                answer = qa.find("Answer")

                if question is None or answer is None:
                    continue

                question_text = "".join(question.itertext()).strip()
                answer_text = "".join(answer.itertext()).strip()

                if question_text == "" or answer_text == "":
                    continue

                question_type = question.attrib.get("qtype", "General")

                records.append({
                    "Focus": focus,
                    "Question_Type": question_type,
                    "Question": question_text,
                    "Answer": answer_text
                })

        except Exception:
            continue

# -----------------------------
# Create DataFrame
# -----------------------------
df = pd.DataFrame(records)

df = df.fillna("")

df.drop_duplicates(inplace=True)

df.reset_index(drop=True, inplace=True)

os.makedirs("data", exist_ok=True)

df.to_csv(CSV_PATH, index=False)

print("\nDataset Saved Successfully.")
print("Total Questions :", len(df))

# -----------------------------
# Create Embeddings
# -----------------------------
print("\nLoading Sentence Transformer...")

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = (
    df["Focus"].astype(str)
    + " "
    + df["Question_Type"].astype(str)
    + " "
    + df["Question"].astype(str)
).tolist()

print("Creating Embeddings...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True
).astype("float32")

# -----------------------------
# Build FAISS Index
# -----------------------------
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, INDEX_PATH)

# -----------------------------
# Save Documents
# -----------------------------
with open(DOCUMENT_PATH, "wb") as f:
    pickle.dump(df, f)

print("\n======================================")
print("Medical QA Dataset Prepared Successfully")
print("======================================")
print(f"CSV Saved        : {CSV_PATH}")
print(f"FAISS Index      : {INDEX_PATH}")
print(f"Documents Saved  : {DOCUMENT_PATH}")
print(f"Total Records    : {len(df)}")
print("======================================")