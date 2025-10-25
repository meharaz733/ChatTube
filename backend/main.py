from fastapi import FastAPI
from Schema.data_model import (   #pydantic model to validate client and api reponse data.
    UserData,
    ResponseData,
    SessionIDData,
    startdata
)
from Utils.makeItReadyForChat import (
    MakeItReadyForChat
)
from Utils.chatHistory import ChatHistory
import uuid
from Database.database import Database
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import langchain
from Model.modelAndTalk import talkWithChatModel

langchain.debug = True
load_dotenv()

db = Database()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["chrome-extension://jgkalpoemkbkooalhmiinabmcieekkcj"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/')
async def root():
    return {'message': "Server is running..."}


@app.get('/health')
async def health_check():
    return {
        'status': 'Ok',
    }


@app.post('/start', response_model=SessionIDData)
async def getSessionID(data: startdata):
    """
    Generate a secure random session ID and perform preprocces for chat.
    """
    sessionID = str(uuid.uuid4())
    video_id = MakeItReadyForChat(data.video_url, sessionID, db.get_db_path())
    
    return SessionIDData(
        sessionID = sessionID,
        videoID = video_id
    )



@app.post('/chat', response_model=ResponseData)
async def chat(req_body: UserData):
    """
    Chat endpoint: retrieves context, builds prompt, gets LLM answer, saves chat history.
    """

    chat = ChatHistory(req_body.sessionID, dbPath=db.get_db_path())
    userChatHistory = chat.__loadMessage__(50) #last 50 messages

    model_response = talkWithChatModel(
                        req_body.user_query,
                        req_body.sessionID,
                        userChatHistory,
                        req_body.videoID,
                        db.get_db_path()
                    )
    
    # store the chat...
    chat.__saveMessage__([("human", req_body.user_query),("ai", model_response)])
    
    return ResponseData(sessionID = req_body.sessionID, aiAnswer = model_response, videoID = req_body.videoID)
