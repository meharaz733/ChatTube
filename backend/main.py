from fastapi import FastAPI
from data_model import (   #pydantic model to validate client and api reponse data.
    UserData,
    ResponseData,
    SessionIDData
)
from makeItReadyForChat import (
    MakeItReadyForChat,
    isVideoExist
)
from modelAndTalk import _model
from chatHistory import ChatHistory
# from retrieve import RetrieveContentFromVectorStore
from prompt import promptForChat
import uuid
from database import Database
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
from embed_fn import embedding
import langchain

langchain.debug = True
load_dotenv()

db = Database()
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
    video_id = MakeItReadyForChat(video_url, sessionID, db.get_db_path())
    
    return SessionIDData(sessionID = sessionID, videoID = video_id)



@app.post('/chat', response_model=ResponseData)
async def chat(req_body: UserData):
    """
    Chat endpoint: retrieves context, builds prompt, gets LLM answer, saves chat history.
    """

    db_path = db.get_db_path()

    chat = ChatHistory(req_body.sessionID, dbPath=db_path)

    #load previous chat...
    userChatHistory = chat.__loadMessage__(50) #last 50 messages

    session_id = req_body.sessionID

    existSessionID = isVideoExist(req_body.videoID, dbPath=db_path)
    
    if existSessionID: #If session ID is exist that's mean the video transcript is already stored in the vector store, 
        session_id = existSessionID #use old session id to find existing collection for user query ##collection name set as session ID..

    try:
        vectorStore = Chroma(
            collection_name=session_id,
            embedding_function=embedding,
            chroma_cloud_api_key=os.getenv("CHROMA_API_KEY"),
            tenant=os.getenv("CHROMA_TENANT"),
            database=os.getenv("CHROMA_DATABASE")
        )
    except Exception as e:
        return ResponseData(
            sessionID = req_body.sessionID,
            aiAnswer = "ERROR: Connenction error",
            videoID = req_body.videoID
        )
    chatPrompt = promptForChat(userChatHistory)
    
    questionAndAnswerChain = create_stuff_documents_chain(
        llm=_model,
        prompt=chatPrompt
    )
    chain = create_retrieval_chain(
        vectorStore.as_retriever(),
        questionAndAnswerChain
    )

    #send to llm(chatmodel)...
    try:
        model_response = chain.invoke({'input': req_body.user_query})["answer"]
    except Exception as e:
        print(f"ERROR: {e}")
        model_response = "Sorry, I couldn't generate a respones at the moment."

    # store the chat...
    chat.__saveMessage__([("human", req_body.user_query),("ai", model_response)])
    
    return ResponseData(sessionID = req_body.sessionID, aiAnswer = model_response, videoID = req_body.videoID)
