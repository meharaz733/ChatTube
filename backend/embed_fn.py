from langchain_huggingface import HuggingFaceEmbeddings


embedding = HuggingFaceEmbeddings(
    model_name= "sentence-transformers/all-mpnet-base-v2"
)
