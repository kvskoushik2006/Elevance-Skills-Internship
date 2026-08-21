import streamlit as st
import pandas as pd
import plotly.express as px

from paper_utils import PaperSearchEngine
from chatbot import ResearchChatbot


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CS Research Assistant",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-bottom: 25px;
    }

    .paper-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }

    .score {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# LOAD SEARCH ENGINE
# --------------------------------------------------

@st.cache_resource
def load_search_engine():

    engine = PaperSearchEngine()

    engine.load_index()

    return engine


@st.cache_resource
def load_chatbot():

    engine = load_search_engine()

    bot = ResearchChatbot(engine)

    return bot


# --------------------------------------------------
# INITIALIZE
# --------------------------------------------------

try:

    engine = load_search_engine()
    chatbot = load_chatbot()

except Exception as e:

    st.error("Unable to load the research system.")

    st.exception(e)

    st.stop()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


if "last_papers" not in st.session_state:

    st.session_state.last_papers = []


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎓 Computer Science Research Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered research assistant for searching and understanding '
    'Computer Science papers from the arXiv dataset.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    top_k = st.slider(
        "Number of papers to retrieve",
        min_value=3,
        max_value=10,
        value=5
    )

    st.divider()

    st.subheader("📚 System")

    st.write("Dataset: arXiv")
    st.write("Domain: Computer Science")
    st.write("Papers indexed: 50,000")
    st.write("Search: FAISS")
    st.write("LLM: Llama 3.2 3B")
    st.write("Runtime: Ollama")

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        chatbot.clear_history()

        st.session_state.last_papers = []

        st.rerun()


# --------------------------------------------------
# DISPLAY PREVIOUS CHAT
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask a Computer Science research question..."
)


# --------------------------------------------------
# PROCESS QUESTION
# --------------------------------------------------

if question:

    # Display user question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Searching research papers and generating answer..."
        ):

            result = chatbot.ask(
                question,
                top_k=top_k
            )

        answer = result["answer"]

        papers = result["papers"]

        st.markdown(answer)

    # Save answer
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Save retrieved papers
    st.session_state.last_papers = papers


# --------------------------------------------------
# RESEARCH PAPERS SECTION
# --------------------------------------------------

if st.session_state.last_papers:

    st.divider()

    st.header("📚 Retrieved Research Papers")

    papers = st.session_state.last_papers


    # ----------------------------------------------
    # PAPER INFORMATION
    # ----------------------------------------------

    for i, paper in enumerate(papers, start=1):

        title = paper.get(
            "title",
            "Unknown title"
        )

        abstract = paper.get(
            "abstract",
            "No abstract available."
        )

        categories = paper.get(
            "categories",
            "Not available"
        )

        score = paper.get(
            "similarity_score",
            0
        )

        with st.expander(
            f"{i}. {title}"
        ):

            st.markdown(
                f"**Similarity Score:** `{score:.3f}`"
            )

            st.markdown(
                f"**Categories:** {categories}"
            )

            st.markdown("### Abstract")

            st.write(abstract)


    # --------------------------------------------------
    # VISUALIZATION
    # --------------------------------------------------

    st.divider()

    st.header("📊 Research Visualization")


    # Similarity score chart

    chart_data = []

    for i, paper in enumerate(papers, start=1):

        chart_data.append(
            {
                "Paper": f"Paper {i}",
                "Title": paper.get(
                    "title",
                    "Unknown"
                )[:60],
                "Similarity Score": paper.get(
                    "similarity_score",
                    0
                )
            }
        )


    chart_df = pd.DataFrame(chart_data)


    fig = px.bar(
        chart_df,
        x="Paper",
        y="Similarity Score",
        hover_data=["Title"],
        title="Retrieved Papers by Similarity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------
    # CATEGORY VISUALIZATION
    # --------------------------------------------------

    category_list = []

    for paper in papers:

        categories = paper.get(
            "categories",
            ""
        )

        if isinstance(categories, str):

            category_list.extend(
                categories.split()
            )


    if category_list:

        category_counts = (
            pd.Series(category_list)
            .value_counts()
            .reset_index()
        )

        category_counts.columns = [
            "Category",
            "Count"
        ]

        fig2 = px.pie(
            category_counts,
            names="Category",
            values="Count",
            title="Research Categories in Retrieved Papers"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "🎓 Computer Science Research Assistant | "
    "arXiv Dataset + FAISS + Sentence Transformers + Ollama"
)