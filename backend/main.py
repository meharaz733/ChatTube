from fastapi import FastAPI
from dotenv import load_dotenv
from model_loader import load_model_
from data_model import (   #pydantic model to validate client and api reponse data.
    User_data,
    Response_data,
    ChatMessage,
    AIMessageData
)
load_dotenv()

model = load_model_()

app = FastAPI()


@app.get('/')
async def root():
    return {'message': "Server is running..."}


@app.post('/chat', response_model=Response_data)
async def chat(req_body: User_data):

    print(req_body.video_url)
    
    print(req_body.chat_history)
    model_response = await model.ainvoke(req_body.user_query)

    return Response_data(transcript = req_body.transcript, chat_history = [{'type':'ai', 'data':{'content':model_response.content}}])
