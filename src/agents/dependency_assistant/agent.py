from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agents.dependency_assistant.nodes.conversation.node import chat_node
from agents.dependency_assistant.nodes.conversation.tools import get_versions

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
agent = graph.compile()
#    print(app.get_graph().draw_mermaid())
