from langchain_community.document_loaders import YoutubeAudioLoader

loader = YoutubeAudioLoader(urls=["https://youtu.be/jEG8wuUE1pY?si=ZLDeGrD2XjdIpPhT"], save_dir='test.mp3')
#docs = loader.load()
#print(docs[0].page_content)
