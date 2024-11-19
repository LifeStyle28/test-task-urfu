from fastapi import FastAPI
import logging
from pydantic import BaseModel


app = FastAPI()


class Message(BaseModel):
    message: str


@app.post("/send-message/{user_id}")
async def send_message(user_id: int, message: Message):
    logging.getLogger('uvicorn').info(f"user_id: {user_id}, message: {message.message}")
    return {"message": "delivered", "user_id": user_id}
