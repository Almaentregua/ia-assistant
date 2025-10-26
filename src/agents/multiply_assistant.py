from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


class SimpleAssistant:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.model_with_tools = self.model.bind_tools([self.multiply])

    def run(self, prompt: str):
        graph = StateGraph(MessagesState)
        graph.add_node("chat", self.chat_node)
        graph.add_node("tools", ToolNode([self.multiply]))

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

    def chat_node(self, state):
        messages = state["messages"]
        response = self.model_with_tools.invoke(messages)
        return {"messages": messages + [response]}

    def multiply(self, a: int, b: int) -> int:
        """Multiply a and b.

        Args:
            a: first int
            b: second int
        """
        return a * b


if __name__ == "__main__":
    load_dotenv()
    bot = SimpleAssistant()
    answer = bot.run("cuanto es 2 x 2")
    print(answer["messages"][-1].content)
    print("--------------")
    print(answer)
