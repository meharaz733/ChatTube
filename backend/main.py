from fastapi import FastAPI
from data_model import (   #pydantic model to validate client and api reponse data.
    UserData,
    ResponseData,
    SessionIDData
)
from makeItReadyForChat import MakeItReadyForChat
from modelAndTalk import talkWithChatModel


app = FastAPI()


@app.get('/')
async def root():
    return {'message': "Server is running..."}



@app.post('/start', response_model=SessionIDData)
async def getSessionID(video_url):
    MakeItReadyForChat(video_url)
    return SessionIDData(sessionID = "jsdh")    



@app.post('/chat', response_model=ResponseData)
async def chat(req_body: UserData):
    
    """This is Chat endpoint."""
    
    model_response = talkWithChatModel(req_body.user_query)
    
    return ResponseData(video_url = req_body.video_url, chat_history = [{'type':'ai', 'data':{'content':model_response}}])
