from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState

from agents.dependency_assistant.nodes.conversation.tools import get_versions

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
model_with_tools = model.bind_tools([get_versions])


def chat_node(state: MessagesState):
    sys_msg = SystemMessage(
        content="Eres un asistente especializado en dependencias de Java."
        + "Tu función es ayudar al usuario a encontrar la información más reciente sobre artefactos publicados en Maven Central, como la última versión disponible, la fecha de publicación y las ramas activas."
        + "Responde siempre en español, de manera clara, técnica y estructurada."
    )
    print(f"estado actual: {state}")
    return {"messages": [model_with_tools.invoke([sys_msg] + state["messages"])]}
