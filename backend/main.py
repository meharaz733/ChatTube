from fastapi import FastAPI
from data_model import (   #pydantic model to validate client and api reponse data.
    UserData,
    ResponseData,
    SessionIDData
)
from makeItReadyForChat import MakeItReadyForChat
from modelAndTalk import talkWithChatModel
from chatHistory import ChatHistory
from retrieve import RetrieveContentFromVectorStore
from prompt import promptForChat
import uuid


app = FastAPI()


@app.get('/')
async def root():
    return {'message': "Server is running..."}



@app.post('/start', response_model=SessionIDData)
async def getSessionID(video_url: str):

    """
    Generate a secure random session ID and perform preprocces for chat.
    
    Args:
        video url(str): user input.
    
    Returns:
        str: A secure session ID string.
    """
    sessionID = str(uuid.uuid4())
    MakeItReadyForChat(video_url, sessionID)
    return SessionIDData(sessionID = sessionID)



@app.post('/chat', response_model=ResponseData)
async def chat(req_body: UserData):
    
    """This is Chat endpoint."""

    chat = ChatHistory(req_body.sessionID)

    #load previous chat...
    userChatHistory = chat.__loadMessage__(50) #last 50 messages

    #retrieve related content of user query...
    retrieval = RetrieveContentFromVectorStore(req_body.sessionID)
    content = retrieval.get_content(req_body.user_query)
    
    #making prompt using user query, content and chat history...
    prompt = promptForChat(userChatHistory, req_body.user_query, content)

    #send to llm(chatmodel)...
    model_response = talkWithChatModel(prompt)

    #store the chat...
    chat.__saveMessage__([("human", req_body.user_query),("ai", model_response)])
    
    return ResponseData(sessionID = req_body.sessionID, aiAnswer = model_response)
