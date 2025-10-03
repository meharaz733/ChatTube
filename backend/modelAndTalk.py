"""This method will return a ChatModel."""
from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint
)


model_ = HuggingFaceEndpoint(
    repo_id = "meta-llama/Llama-3.1-8B-Instruct",
    task = "text_generation"
)

_model = ChatHuggingFace(llm = model_)


def talkWithChatModel(prompt):
    model_response = _model.invoke(prompt)
    return model_response.content
