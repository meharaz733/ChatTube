"""transcribeHelper help to extract text from YouTube video using youtube-transcript-api."""

from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat


def transcribeVideo(video_url: str):
    """
    This is a method to extract text from youtube video.

    """
    
    loader = YoutubeLoader.from_youtube_url(
        youtube_url=video_url,
        # add_video_info=True,
        language=["en", "en-US", "bn", "hi"],
        transcript_format=TranscriptFormat.CHUNKS,
        # chunk_size_seconds=30,
    )
    docs = loader.load()

    transcript = "\n\n".join(f"Start_time: {doc.metadata["start_timestamp"]} {doc.page_content}" for doc in docs)
 
    return transcript


#test
# url=input()
# docs = transcribeVideo(video_url=url)

# print(docs)
# print(type(docs))
    


