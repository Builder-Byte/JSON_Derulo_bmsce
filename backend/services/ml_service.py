#type: ignore
from typing_extensions import TypedDict
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver  

llm = init_chat_model(
    model="ollama:qwen3-next:80b-cloud",
    temperature=0
)

class State(TypedDict):
    messages: Annotated[list,add_messages]
    
def chatbot(state:State):
    #print("\n\nchatenode", state)
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}
    
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot", END)

#graph = graph_builder.compile()

def compile_graph_With_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

DB_URI = "mongodb://localhost:27017"

with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_With_checkpointer=compile_graph_With_checkpointer(checkpointer=checkpointer)
    config = {
            "configurable": {
                "thread_id": "divyansh"
            }
        }

    for chunk in graph_With_checkpointer.stream(
        State({"messages": ["guess my age"]}),
        config,
        stream_mode="values"
        ):
        chunk["messages"][-1].pretty_print()

    #print("\n\nUpdated state ", updated_state)