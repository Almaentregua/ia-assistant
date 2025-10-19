from datetime import datetime
from typing import List, Dict

from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition

from src.repository_search import MavenRepositoryClient


class RepositoryAssistant:
    # System message
    sys_msg = SystemMessage(content="""
    Eres un asistente especializado en dependencias de Java. 
    Tu función es ayudar al usuario a encontrar la información más reciente sobre artefactos publicados en Maven Central, como la última versión disponible, la fecha de publicación y las ramas activas. 
    Responde siempre en español, de manera clara, técnica y estructurada.
    """)

    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.model_with_tools = self.model.bind_tools([self.get_versions])
        self.sys_msg = SystemMessage(content="""
    Eres un asistente especializado en dependencias de Java. 
    Tu función es ayudar al usuario a encontrar la información más reciente sobre artefactos publicados en Maven Central, como la última versión disponible, la fecha de publicación y las ramas activas. 
    Responde siempre en español, de manera clara, técnica y estructurada.
    """)

    def run(self, prompt: str):
        self.feedback()
        graph = StateGraph(MessagesState)
        graph.add_node("chat", self.chat_node)
        graph.add_node("tools", ToolNode([self.get_versions]))

        graph.add_edge(START, "chat")
        graph.add_conditional_edges(
            "chat",
            # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
            # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
            tools_condition,
        )
        graph.add_edge("tools", END)
        app = graph.compile()
        print(app.get_graph().draw_mermaid())
        return app.invoke({"messages": [HumanMessage(content=prompt)]})

    def feedback(self):
        # Get user feedback
        user_approval = input("Do you want to call the tool? (yes/no): ")

        # Check approval
        if user_approval.lower() == "yes":
            print("ok")
        else:
            exit()

    def chat_node(self, state):
        return {"messages": [self.model_with_tools.invoke([self.sys_msg] + state["messages"])]}

    def get_versions(self, group_id: str, artifact_id: str) -> List[Dict[str, datetime]]:
        """Fetch and parse all available versions for a given artifact."""
        maven_repository = MavenRepositoryClient()
        return maven_repository.get_versions(group_id, artifact_id)




if __name__ == "__main__":
    load_dotenv()
    bot = RepositoryAssistant()
    answer = bot.run("Quiero la ultima version de org.springframework.boot:spring-boot-starter")
    print(answer)
