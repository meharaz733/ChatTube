"""toBeReadyForChat, complete the nessesary step to make chat more reliable."""

from prompt import PrompForStructDoc
from transcribeHelper import transcribeVideo
from modelAndTalk import talkWithChatModel

def MakeItReadyForChat(video_url: str):
    #get transcript
    transcript = transcribeVideo(video_url=video_url)
    #make a promptTemplate
    prompt = PrompForStructDoc(transcript)
    #make the transcript structured doc with NLP model...
    doc = talkWithChatModel(prompt)
    #embedding the doc based on paragraph...
    

    #Store the embedding result to vetore database...
