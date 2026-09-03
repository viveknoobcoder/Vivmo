from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()



client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

class chatRequest(BaseModel):
    message : str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


def get_bot_response(user_message):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="openai/gpt-oss-20b",
            stream=False,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print("GROQ ERROR:", e)
        return f"Groq error: {e}"

@app.get("/")
def home():
    return {"message": "Chatbot API is running"}


@app.post("/chat")
async def chat(request:chatRequest):
    reply=get_bot_response(request.message)
    return {"reply":reply}
    