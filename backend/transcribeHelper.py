"""transcribeHelper help to extract text from YouTube video using youtube-transcript-api."""

from langchain_community.document_loaders import YoutubeLoader


def transcribeVideo(video_url: str):
    """
    This is a method to extract text from youtube video.

    """
    
    loader = YoutubeLoader.from_youtube_url(youtube_url=video_url)
    docs = loader.load()

    return docs[0].page_content
