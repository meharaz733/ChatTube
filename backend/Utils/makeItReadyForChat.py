"""MakeItReadyForChat, omplete the nessesary step to make chat more reliable."""

# from prompt import PrompForStructDoc
from .transcribeHelper import transcribeVideo
# from modelAndTalk import talkWithChatModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from Model.embed_fn import embedding
import sqlite3
import os


def getVideoID(url:str):
    """ONLY work for STANDARD VIDEO URL"""
    
    return url.split('=')[1]


def isVideoExist(videoID:str, dbPath:str):
    try:
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT sessionID FROM videoInfo where videoID = ?
            """,
            (videoID,)
        )
        existSessionID = cursor.fetchone()
        conn.close()
        return existSessionID[0] if existSessionID else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def saveTheVideo(videoID:str, dbPath:str, sessionID:str):
    try:
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO videoInfo (videoID, sessionID) VALUES (?, ?)
            """,
            (videoID, sessionID)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"WARNING: unable to save the video info\nERROR: {e}")


def MakeItReadyForChat(video_url: str, sessionID: str, dbPath:str):

    videoID = getVideoID(video_url)
    existSessionID = isVideoExist(videoID, dbPath)
    
    if existSessionID:
        print("The video already exist in database...")
        return videoID
    
    transcript = transcribeVideo(video_url=video_url)

    # prompt = PrompForStructDoc(transcript)
    # doc = talkWithChatModel(prompt)
    
    textSplitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100
    )
    texts = textSplitter.split_text(transcript)

    vectorStore = Chroma(
        collection_name=sessionID,
        embedding_function=embedding,
        chroma_cloud_api_key=os.getenv("CHROMA_API_KEY"),
        tenant=os.getenv("CHROMA_TENANT"),
        database=os.getenv("CHROMA_DATABASE")
    )
  
    ids = [f"{sessionID}_{_}" for _ in range(len(texts))]
    vectorStore.add_texts(texts=texts, ids=ids)

    saveTheVideo(videoID, dbPath, sessionID)
    
    return videoID

    
