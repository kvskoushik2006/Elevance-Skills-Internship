import json
import csv
import random

INPUT_FILE = "data/arxiv-metadata-oai-snapshot.json"
OUTPUT_FILE = "data/arxiv_cs.csv"

MAX_PAPERS = 50000
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

papers = []
total_cs = 0

print("Starting Computer Science paper extraction...")
print("This may take some time because the source file is about 5 GB.")

with open(INPUT_FILE, "r", encoding="utf-8") as file:

    for line_number, line in enumerate(file, start=1):

        try:
            paper = json.loads(line)

            categories = paper.get("categories", "")

            # Keep Computer Science papers
            if any(category.startswith("cs.") for category in categories.split()):

                total_cs += 1

                selected_paper = {
                    "id": paper.get("id", ""),
                    "title": paper.get("title", "").replace("\n", " ").strip(),
                    "abstract": paper.get("abstract", "").replace("\n", " ").strip(),
                    "authors": paper.get("authors", ""),
                    "categories": categories,
                    "update_date": paper.get("update_date", "")
                }

                # Reservoir sampling
                if len(papers) < MAX_PAPERS:
                    papers.append(selected_paper)
                else:
                    position = random.randint(0, total_cs - 1)

                    if position < MAX_PAPERS:
                        papers[position] = selected_paper

            if line_number % 100000 == 0:
                print(
                    f"Processed {line_number:,} papers | "
                    f"CS papers found: {total_cs:,}"
                )

        except json.JSONDecodeError:
            continue

print()
print(f"Total Computer Science papers found: {total_cs:,}")
print(f"Selected papers: {len(papers):,}")

with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "id",
            "title",
            "abstract",
            "authors",
            "categories",
            "update_date"
        ]
    )

    writer.writeheader()
    writer.writerows(papers)

print()
print("SUCCESS!")
print(f"Computer Science dataset saved to: {OUTPUT_FILE}")