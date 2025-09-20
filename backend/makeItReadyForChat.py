"""MakeItReadyForChat, complete the nessesary step to make chat more reliable."""

from prompt import PrompForStructDoc
from transcribeHelper import transcribeVideo
from modelAndTalk import talkWithChatModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from embed_fn import embedding
import os


def MakeItReadyForChat(video_url: str, sessionID: str):

    #check is the video script already exist in vector db...

    
    #get transcript
    transcript = transcribeVideo(video_url=video_url)
    
    #make a promptTemplate
    prompt = PrompForStructDoc(transcript)
    
    #make the transcript structured doc with NLP model...
    doc = talkWithChatModel(prompt)
    
    #Splitting the doc...
    textSplitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=50
    )
    texts = textSplitter.split_text(doc)

    # print(len(texts))
    
    #store the texts into vector database...
    vectorStore = Chroma(
        collection_name=sessionID,
        embedding_function=embedding,
        chroma_cloud_api_key=os.getenv("CHROMA_API_KEY"),
        tenant=os.getenv("CHROMA_TENANT"),
        database=os.getenv("CHROMA_DATABASE")
    )
    
    ids = [f"{sessionID}_{_}" for _ in range(len(texts))]
    
    vectorStore.add_texts(texts=texts, ids=ids)

    
