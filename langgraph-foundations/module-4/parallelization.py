import os
import operator
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.tools import TavilySearchResults
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, START, END

# ── Environment setup ──────────────────────────────────────────────────────────
load_dotenv(
    "/Users/L107127/Library/CloudStorage/OneDrive-EliLillyandCompany/Desktop/langchain-academy/.env",
    override=True,
)

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# ── LLM ────────────────────────────────────────────────────────────────────────
llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)

# ── State ──────────────────────────────────────────────────────────────────────
class State(TypedDict):
    question: str
    answer: str
    context: Annotated[list, operator.add]

# ── Nodes ──────────────────────────────────────────────────────────────────────
def search_web(state):
    """Retrieve docs from web search"""
    print("Searching the web...")
    tavily_search = TavilySearchResults(max_results=3)
    search_docs = tavily_search.invoke(state["question"])

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}">\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"context": [formatted_search_docs]}

def search_wikipedia(state):
    """Retrieve docs from wikipedia"""
    print("Searching Wikipedia...")
    search_docs = WikipediaLoader(
        query=state["question"], load_max_docs=2
    ).load()

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}">\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"context": [formatted_search_docs]}

def generate_answer(state):
    """Node to answer a question"""
    context = state["context"]
    question = state["question"]

    answer_template = "Answer the question {question} using this context: {context}"
    answer_instructions = answer_template.format(question=question, context=context)

    answer = llm.invoke(
        [SystemMessage(content=answer_instructions)]
        + [HumanMessage(content="Answer the question.")]
    )
    return {"answer": answer}

# ── Graph ──────────────────────────────────────────────────────────────────────
builder = StateGraph(State)

builder.add_node("search_web", search_web)
builder.add_node("search_wikipedia", search_wikipedia)
builder.add_node("generate_answer", generate_answer)

builder.add_edge(START, "search_wikipedia")
builder.add_edge(START, "search_web")
builder.add_edge("search_wikipedia", "generate_answer")
builder.add_edge("search_web", "generate_answer")
builder.add_edge("generate_answer", END)

graph = builder.compile()

# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    questions = [
        "How were Nvidia's Q2 2024 earnings",
        "What is the latest breakthrough in quantum computing",
        "What caused the 2008 financial crisis",
        "How does mRNA vaccine technology work",
        "What are the biggest risks of artificial general intelligence",
    ]

    for q in questions:
        print(f"\n{'='*80}")
        print(f"Question: {q}")
        print("=" * 80)
        result = graph.invoke({"question": q})
        print(result["answer"].content)
