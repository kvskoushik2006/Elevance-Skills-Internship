from paper_utils import PaperSearchEngine

engine = PaperSearchEngine()

engine.load_index()

results = engine.search("transformer neural networks", 5)

print("\nTop 5 relevant papers:\n")

for i, paper in enumerate(results, start=1):
    print(f"{i}. {paper['title']}")
    print(f"   Score: {paper['similarity_score']:.3f}")
    print()