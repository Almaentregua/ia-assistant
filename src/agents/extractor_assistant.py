from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class Person(BaseModel):
    """ Personal information """
    name: str= Field(description="The name of the person")
    age: str= Field(description="The age of the person")




def chat_node(state: MessagesState):
    sys_msg = SystemMessage(content="Eres un asistente especializado para extraer los datos de una persona de una conversacion")
    ia_message = model_with_tools.invoke([sys_msg] + [state["messages"][-1]])
    print(ia_message)
    return {"messages": [ia_message]}



model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
model_with_tools = model.with_structured_output(schema=Person)

graph = StateGraph(MessagesState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

app = graph.compile()