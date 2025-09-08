from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, List
from web_operations import google_search_func, bing_search_func, get_reddit_posts, get_reddit_comments
from prompts import (
    get_reddit_url_analysis_messages,
    get_reddit_analysis_messages,
    get_google_analysis_messages,
    get_bing_analysis_messages,
    get_synthesis_messages
)


load_dotenv()


#llm = ChatOllama(model="llama3.2:1b", temperature=0)
llm = ChatGroq(model_name= "meta-llama/llama-4-scout-17b-16e-instruct")


# Defining State Object
class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_question: str | None
    google_results: str | None
    bing_results: str | None
    reddit_results: str | None
    selected_reddit_urls: list[str] | None
    reddit_post_data: str | None
    google_analysis: str | None
    bing_analysis: str | None
    reddit_analysis: str | None
    final_answer: str | None


class RedditURLAnalysis(BaseModel):
    selected_urls: List[str] = Field(description="List of Reddit URLs that contain valuable information for answering the user's question")


# Defining Nodes

def google_search(state: State):
    user_question = state.get("user_question", "")

    print(f"Searching google for: {user_question}\n")

    google_results = google_search_func(user_question)
    print(google_results)
    
    return {"google_results": google_results}


def bing_search(state: State):
    user_question = state.get("user_question", "")

    print(f"Searching Bing for: {user_question}\n")

    bing_results = bing_search_func(user_question)
    print(bing_results)

    return {"bing_results": bing_results}


def reddit_search(state: State):
    user_question = state.get("user_question")

    print(f"Searching Reddit for: {user_question}\n")

    reddit_results = get_reddit_posts(user_question)
    
    return {"reddit_results": reddit_results}


def analyze_reddit_posts(state: State):
    user_question = state.get("user_question", "")
    reddit_results = state.get("reddit_results", "")

    if not reddit_results:
        return {"selected_reddit_urls": []}
    
    structured_llm = llm.with_structured_output(RedditURLAnalysis)
    messages = get_reddit_url_analysis_messages(user_question, reddit_results)

    try:
        analysis = structured_llm.invoke(messages)
        selected_urls = analysis.selected_urls

        print("Selected URLs:")
        for i, url in enumerate(selected_urls, 1):
            print(f"   {i}. {url}")

    except Exception as e:
        print(e)
        selected_urls = []


    return {"selected_reddit_urls": selected_urls}


def retrieve_reddit_posts(state: State):

    print("Getting reddit post comments...")

    selected_urls = state.get("selected_reddit_urls", [])

    print(f"Processing {len(selected_urls)} Reddit URLs")
    reddit_post_data = get_reddit_comments(selected_urls)

    if reddit_post_data:
        print(f"Successfully got {len(reddit_post_data)} posts")
    else:
        print("Failed to get post data")
        reddit_post_data = []

    print(reddit_post_data)

    if not selected_urls:
        return {"reddit_post_data": []}
    
    return {"reddit_post_data": reddit_post_data}


def analyze_google_results(state: State):
    print("Analyzing google search results")

    user_question = state.get("user_question", "")
    google_results = state.get("google_results", "")

    messages = get_google_analysis_messages(user_question, google_results)
    reply = llm.invoke(messages)
    return {"google_analysis": reply.content}


def analyze_bing_results(state: State):
    print("Analyzing bing search results")

    user_question = state.get("user_question", "")
    bing_results = state.get("bing_results", "")

    messages = get_bing_analysis_messages(user_question, bing_results)
    reply = llm.invoke(messages)

    return {"bing_analysis": reply.content}


def analyze_reddit_results(state: State):
    print("Analyzing reddit search results")

    user_question = state.get("user_question", "")
    reddit_results = state.get("reddit_results", "")
    reddit_post_data = state.get("reddit_post_data", "")

    messages = get_reddit_analysis_messages(user_question, reddit_results, reddit_post_data)
    reply = llm.invoke(messages)

    return {"reddit_analysis": reply.content}

def synthesize_analyses(state: State):
    print("Combine all results together")

    user_question = state.get("user_question", "")
    google_analysis = state.get("google_analysis", "")
    bing_analysis = state.get("bing_analysis", "")
    reddit_analysis = state.get("reddit_analysis", "")

    messages = get_synthesis_messages(
        user_question, google_analysis, bing_analysis, reddit_analysis
    )

    reply = llm.invoke(messages)
    final_answer = reply.content

    return {"final_answer": final_answer, "messages": [{"role": "assistant", "content": final_answer}]}


# Building the Graph
graph_builder = StateGraph(State)


graph_builder.add_node("google_search", google_search)
graph_builder.add_node("bing_search", bing_search)
graph_builder.add_node("reddit_search", reddit_search)
graph_builder.add_node("analyze_reddit_posts", analyze_reddit_posts)
graph_builder.add_node("retrieve_reddit_posts", retrieve_reddit_posts)
graph_builder.add_node("analyze_google_results", analyze_google_results)
graph_builder.add_node("analyze_bing_results", analyze_bing_results)
graph_builder.add_node("analyze_reddit_results", analyze_reddit_results)
graph_builder.add_node("synthesize_analyses", synthesize_analyses)

graph_builder.add_edge(START, "google_search")
graph_builder.add_edge(START, "bing_search")
graph_builder.add_edge(START, "reddit_search")

graph_builder.add_edge("google_search", "analyze_reddit_posts")
graph_builder.add_edge("bing_search", "analyze_reddit_posts")
graph_builder.add_edge("reddit_search", "analyze_reddit_posts")
graph_builder.add_edge("analyze_reddit_posts", "retrieve_reddit_posts")

graph_builder.add_edge("retrieve_reddit_posts", "analyze_google_results")
graph_builder.add_edge("retrieve_reddit_posts", "analyze_bing_results")
graph_builder.add_edge("retrieve_reddit_posts", "analyze_reddit_results")

graph_builder.add_edge("analyze_google_results", "synthesize_analyses")
graph_builder.add_edge("analyze_bing_results", "synthesize_analyses")
graph_builder.add_edge("analyze_reddit_results", "synthesize_analyses")

graph_builder.add_edge("synthesize_analyses", END)

graph = graph_builder.compile()


# Execute Agent
def run_chatbot():
    print("Mutlitsource Search Agent")
    print("Type exit to quit\n")

    while True:
        user_input = input("Ask me anything: ")
        if user_input == "exit":
            print("Bye Bye!!")
            break

        state = {
            "messages" : [{"role":"user", "content": user_input}],
            "user_question" : user_input,
            "google_results": None,
            "bing_results": None,
            "reddit_results": None,
            "selected_redit_urls": None,
            "reddit_post_data": None,
            "google_analysis": None,
            "bing_analysis": None,
            "reddit_analysis": None,
            "final_answer": None,
        }

        print("Starting parallel research process...")
        print("Launching Google, Bing, Reddit Search\n")

        final_state = graph.invoke(state)
        
        if final_state.get("final_answer"):
            print(f"Final Answer: {final_state.get("final_answer")}\n")

        print("-" * 80)

if __name__ == "__main__":
    run_chatbot()
