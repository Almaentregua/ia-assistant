from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
from agents.dependency_assistant.agent import agent
from langchain_core.messages import HumanMessage

app = FastAPI()


class Message(BaseModel):
    message: str

@app.post("/chat/{chat_id}")
async def hello_name(chat_id: str, message: Message):
    # TODO: add chat_id to the messages and use it to store the messages in the database
    messages = [HumanMessage(content=message.message)]
    response = agent.invoke({"messages": messages})
    last_message = response["messages"][-1]
    return {"message": last_message.content}
