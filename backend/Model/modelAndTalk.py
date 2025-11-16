"""Chat model and Chat function."""
from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint
)
from langchain_chroma import Chroma
from Model.embed_fn import embedding
import os
from Utils.prompt import promptForChat
from Utils.makeItReadyForChat import isVideoExist
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


llm_model = HuggingFaceEndpoint(
    repo_id = "meta-llama/Llama-3.1-8B-Instruct",
    task = "text_generation"
)

model = ChatHuggingFace(llm = llm_model)


def talkWithChatModel(userQuery, sessionID, userChatHistory, videoID, dbPath):

    session_id = sessionID
    
    #existing session ID for existing collection..
    existSessionID = isVideoExist(videoID=videoID, dbPath=dbPath)
    if existSessionID:
        session_id = existSessionID

    try:
        vectorStore = Chroma(
            collection_name=session_id,
            embedding_function=embedding,
            chroma_cloud_api_key=os.getenv("CHROMA_API_KEY"),
            tenant=os.getenv("CHROMA_TENANT"),
            database=os.getenv("CHROMA_DATABASE")
        )
    except Exception as e:
        return f"ERROR: Database connenction error\n{e}"
    
    chatPrompt = promptForChat(userChatHistory)
    
    questionAndAnswerChain = create_stuff_documents_chain(
        llm=model,
        prompt=chatPrompt
    )
    chain = create_retrieval_chain(
        vectorStore.as_retriever(),
        questionAndAnswerChain
    )

    try:
        model_response = chain.invoke({'input': userQuery})["answer"]
    except Exception as e:
        print(f"ERROR: {e}")
        model_response = "Sorry, I couldn't generate a respones at the moment."

    return model_response
