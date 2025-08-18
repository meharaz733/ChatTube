from fastapi import FastAPI
from dotenv import load_dotenv
from model_loader import load_model_
from data_model import (   #pydantic model to validate client and api reponse data.
    UserData,
    ResponseData,
    SessionIDData
)
from transcribeHelper import transcribeVideo  #extract a transcript from given video url.
from makeItReadyForChat import MakeItReadyForChat

load_dotenv()

model = load_model_()

app = FastAPI()


@app.get('/')
async def root():
    return {'message': "Server is running..."}



@app.post('/start', response_model=SessionIDData)
async def getSessionID(video_url):
    
    transcript = transcribeVideo(video_url=video_url)
#   print(transcript)
    PromptWithTranscript = MakeItReadyForChat(transcript)
    doc = await model.ainvoke(PromptWithTranscript)

    

    print(PromptWithTranscript)
    print("\n\n", doc.content)

    return SessionIDData(sessionID = "jsdh")    

@app.post('/chat', response_model=ResponseData)
async def chat(req_body: UserData):
    
    """This is Chat endpoint."""
    
    model_response = await model.ainvoke(req_body.user_query)
    return ResponseData(video_url = req_body.video_url, chat_history = [{'type':'ai', 'data':{'content':model_response.content}}])
