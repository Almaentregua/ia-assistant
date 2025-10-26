from datetime import datetime
from typing import List, Dict

from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition

from src.repository_search import MavenRepositoryClient


def feedback():
    # Get user feedback
    user_approval = input("Do you want to continue? (yes/no): ")

    # Check approval
    if not user_approval.lower() == "yes":
        exit()


def chat_node(state: MessagesState):
    sys_msg = SystemMessage(
        content="Eres un asistente especializado en dependencias de Java."
        + "Tu función es ayudar al usuario a encontrar la información más reciente sobre artefactos publicados en Maven Central, como la última versión disponible, la fecha de publicación y las ramas activas."
        + "Responde siempre en español, de manera clara, técnica y estructurada."
    )
    print(f"estado actual: {state}")
    return {"messages": [model_with_tools.invoke([sys_msg] + state["messages"])]}


def get_versions(group_id: str, artifact_id: str) -> List[Dict[str, datetime]]:
    """Fetch and parse all available versions for a given artifact."""
    maven_repository = MavenRepositoryClient()
    return maven_repository.get_versions(group_id, artifact_id)


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
model_with_tools = model.bind_tools([get_versions])


graph = StateGraph(MessagesState)
graph.add_node("chat", chat_node)
graph.add_node("tools", ToolNode([get_versions]))
graph.add_edge(START, "chat")
graph.add_conditional_edges(
    "chat",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
graph.add_edge("tools", "chat")
app = graph.compile()
#    print(app.get_graph().draw_mermaid())
