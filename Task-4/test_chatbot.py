from paper_utils import PaperSearchEngine
from chatbot import ResearchChatbot


print("Loading paper search engine...")

engine = PaperSearchEngine()
engine.load_index()

print("Starting research chatbot...")

bot = ResearchChatbot(engine)

question = "What are transformer neural networks?"

result = bot.ask(question, top_k=5)

print("\n==============================")
print("ANSWER")
print("==============================")

print(result["answer"])

print("\n==============================")
print("RELEVANT PAPERS")
print("==============================")

for i, paper in enumerate(result["papers"], start=1):
    print(f"\n{i}. {paper.get('title', 'Unknown title')}")
    print(f"Score: {paper.get('similarity_score', 0):.3f}")