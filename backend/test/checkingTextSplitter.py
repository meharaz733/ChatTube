from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """Hi, I'm Meharaz.
what's your name?

oh, My name is kichu na.
"""

textSplitter = RecursiveCharacterTextSplitter(
    chunk_size=20, chunk_overlap=0,
)

texts = textSplitter.split_text(text)

print(texts)
print(type(texts))
