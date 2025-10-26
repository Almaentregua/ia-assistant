from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState

from agents.dependency_assistant.nodes.conversation.prompt import prompt_template
from agents.dependency_assistant.nodes.conversation.tools import get_versions

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
model_with_tools = model.bind_tools([get_versions])


def chat_node(state: MessagesState):
    sys_msg = SystemMessage(content=prompt_template)
    print(f"estado actual: {state}")
    return {"messages": [model_with_tools.invoke([sys_msg] + state["messages"])]}
