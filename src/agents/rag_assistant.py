

from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI


def chat_node(state: MessagesState) -> dict:
    sys_msg = SystemMessage(content="Eres un asistente especializado en estadisticas de futbol")
    print(f"estado actual: {state}")
    ia_message = model_with_tools.invoke([sys_msg] + [state["messages"][-1]])
    print(ia_message.text)
    return {"messages": [ia_message]}


VECTOR_STORE_IDS = ["vs_68fcf3fc0ee4819187471dd2e1e1ca75"]
TOOLS = [{"type": "file_search", "vector_store_ids": VECTOR_STORE_IDS}]

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
model_with_tools = model.bind_tools(TOOLS)

graph = StateGraph(MessagesState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")

app = graph.compile()