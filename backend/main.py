from fastapi import FastAPI
from dotenv import load_dotenv
from model_loader import load_model_
from data_model import (   #pydantic model to validate client and api reponse data.
    UserData,
    ResponseData
)
from transcribeHelper import transcribeVideo


load_dotenv()

model = load_model_()

app = FastAPI()


@app.get('/')
async def root():
    return {'message': "Server is running..."}


@app.post('/chat', response_model=ResponseData)
async def chat(req_body: UserData):
    
    """This is Chat endpoint."""
    
    transcribe = transcribeVideo(video_url=req_body.video_url)
    
    model_response = await model.ainvoke(req_body.user_query)

    return ResponseData(video_url = req_body.video_url, chat_history = [{'type':'ai', 'data':{'content':model_response.content}}])
