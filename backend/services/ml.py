#type:ignore

from config import EVAL_OLLAMA_MODEL, OLLAMA_MODEL
from ollama import chat
from ollama import ChatResponse

from typing_extensions import Annotated, TypedDict
from typing import Literal, Optional
from langgraph.graph import StateGraph, END, START
from langchain.chat_models import init_chat_model
import os
os.system("clear")
class State(TypedDict):
    user_query:str
    llm_output: Optional[str]
    is_good: Optional[bool]
    
# llm = init_chat_model(
#     model="ollama:qwen3-next:80b-cloud",
# )


def chatbot(state: State):
    # llm.invoke(state.get("user_query"))
    print("\n\nChatBot Node", state)
    response: ChatResponse = chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "user", "content": state.get("user_query")}
            ],
        )    
    state["llm_output"] = response.message.content
    return state

def eval_chatbot(state: State) :
    # llm.invoke(state.get("user_query"))
    print("\n\nEvalBot Node", state)
    
    response: ChatResponse = chat(
            model=EVAL_OLLAMA_MODEL,
            messages=[
                {"role": "user", "content": state.get("user_query")}
            ],
        )    
    state["llm_output"] = response.message.content
    return state


def endnode(state:State):
    print("\n\nEnd Node", state)
    return state

def evaluate_response(state: State) -> Literal["eval_chatbot" , "endnode"]:
    print("\n\nEvalResponse Node", state)
    
    if False:
        return "endnode"
    
    return "eval_chatbot"

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("eval_chatbot", eval_chatbot)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)
graph_builder.add_edge("eval_chatbot", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

print(graph.invoke(State(user_query="What is 2 +2 ")))