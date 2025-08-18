from langchain_community.document_loaders import YoutubeLoader
from langchain_yt_dlp.youtube_loader import YoutubeLoaderDL
from yt_dlp import YoutubeDL
import timeit


def transcribeVideo(video_url: str):
    """
    This function benchmarks transcript extraction using two loaders.
    """

    # Time YoutubeLoaderDL
    # def run_loader_dl():
    #     loader = YoutubeLoaderDL.from_youtube_url(
    #         youtube_url=video_url, add_video_info=True
    #     )
    #     _ = loader.load()

    # time1 = timeit.Timer(run_loader_dl).timeit(number=10)
    # print(f"YoutubeLoaderDL took: {time1 / 10:.2f} seconds")

    # Time YoutubeLoader + yt_dlp
    def run_loader_and_ydl():
        loader2 = YoutubeLoader.from_youtube_url(video_url)
        _ = loader2.load()

        print(_[0])

    time2 = timeit.Timer(run_loader_and_ydl).timeit(number=10)
    print(f"YoutubeLoader took: {time2 / 10:.2f} seconds")


# Example usage
transcribeVideo(video_url="https://www.youtube.com/watch?v=oX7OduG1YmI")

