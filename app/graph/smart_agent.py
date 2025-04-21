from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, END
from sklearn.metrics.pairwise import cosine_similarity

# --- Import local services ---
from app.services.mememory_service import save_to_memory, check_contextual_and_respond, retriever, embedding_model
from app.services.classifier import classify_with_llm
from app.services import stock_data, news_search, google_search
from app.services.llm_response import get_answer_from_groq

# 🧠 Check if similar question was asked before
def was_question_asked_before(user_input: str, threshold: float = 0.85) -> bool:
    input_embedding = embedding_model.embed_query(user_input)
    similar_docs = retriever.get_relevant_documents(user_input)

    for doc in similar_docs:
        doc_embedding = embedding_model.embed_query(doc.page_content)
        similarity = cosine_similarity([input_embedding], [doc_embedding])[0][0]
        if similarity >= threshold:
            return True
    return False

# 🔁 LangGraph State
class State(TypedDict):
    input: str
    all_actions: Annotated[List[str], operator.add]
    response: str
    category: str

# ✅ Nodes

def save_input(state: State) -> State:
    save_to_memory(state["input"])
    return state

def check_previous(state: State) -> State:
    response = check_contextual_and_respond(state["input"])
    if response:
        state["response"] = response
    return state

def classify(state: State) -> State:
    print("🚀 classify() got input:", repr(state.get("input")))

    if not state.get("input"):
        print("❌ No input found in state!")
        state["category"] = ""
        return state

    category = classify_with_llm(state["input"])
    print("✅ classify_with_llm returned:", repr(category))
    state["category"] = category
    return state

def route_by_category(state: State) -> State:
    question = state["input"]
    category = state.get("category")

    print("📌 Routing category:", category)
    if was_question_asked_before(state["input"]):
        state["response"] = check_contextual_and_respond(question)
    elif category == "Trades":
        state["response"] = stock_data(question)
    elif category == "llm":
        state["response"] = get_answer_from_groq(question)
    elif category == "News":
        state["response"] = news_search(question)
    elif category == "FMP Data":
        state["response"] = stock_data(question)
    elif category == "Google stock_data":
        state["response"] = google_search(question)
    else:
        state["response"] = f"Could not classify the question (got '{category}')."
    return state

def return_response(state: State) -> State:
    return state

# 🧩 Build Graph
graph = StateGraph(State)

graph.add_node("save", save_input)
graph.add_node("check_previous", check_previous)
graph.add_node("classify", classify)
graph.add_node("route", route_by_category)
graph.add_node("return", return_response)

graph.set_entry_point("save")
graph.add_edge("save", "check_previous")
graph.add_conditional_edges(
    "check_previous",
    lambda state: "response" in state and isinstance(state["response"], str) and state["response"].strip() != "",
    {
        True: "return",
        False: "classify"
    }
)
graph.add_edge("classify", "route")
graph.add_edge("route", "return")
graph.set_finish_point("return")

# 📦 Export compiled graph
app = graph.compile()
