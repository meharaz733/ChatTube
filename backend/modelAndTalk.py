from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint
)
from dotenv import load_dotenv

load_dotenv()

def load_model_():
    """This method will return a ChatModel."""
    model_ = HuggingFaceEndpoint(
        repo_id = "meta-llama/Llama-3.1-8B-Instruct",
        task = "text_generation"
    )

    return ChatHuggingFace(llm = model_)

model = load_model_()

def talkWithChatModel(prompt):
    model_response = model.invoke(prompt)
    return model_response.content
