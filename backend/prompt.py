"""
Make prompt to send the Chat model...
"""

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate
)


def promptForChat(userChatHistory, query, relatedContent):
    """
    Takes user query, chat history, and query related content then returns a PromptTemplate.
    """

    systemMsg = [("system", "Let's you are a video comprehension assistant. Here're a chathistory(if available), query and user query related content that are collected from the video. Kindly response accurately as user want to know. If you haven't enough information in this prompt then simply ans, 'Insufficient context, please provide more details So I can ans your question'.")]
    finalMsg = systemMsg + userChatHistory #systemMsg and userChatHistory are list of tuple, so finalMsg will be a list of tuple..
    chatPrompt = ChatPromptTemplate(finalMsg + [("human", "Query: {query}\n\nContent:{content}")])
    prompt = chatPrompt.invoke({
                                   "query":query,
                                   "content": relatedContent
                               })    
    return prompt


#####################################################
# ##################################################
# ################################################


def PrompForStructDoc(transcript: str):
    """
    This method take a script and make a prompt template, then return it.

    """

    prompt = PromptTemplate(
        template="""
Hi, your role is a script writer. Trim this YouTube video transcript into clear, topic-based sections.


Transcript:
{transcript}


Instructions:
1. Split by Topic: Divide the transcript into paragraphs, each covering one key topic. Start each with a 3–6-word title.
   Example:  
   "Early Life and Education Struggles
   When I was young, my family lived overseas in Indonesia for a few years..."

2. Preserve Original Meaning: Never alter the speaker’s intent or add external content.

3. Conciseness: Keep paragraphs under 100 words. Split long topics into (Part 1), (Part 2), etc with same title.

4. Avoid Redundancy: Merge repeated points into one paragraph.

5. Direct Start: Don't start with "Here’s the trimmed version", "Here is the trimmed version.", etc, start directly with title of paragraph...

6. Search-Friendly Titles: Make titles descriptive and SEO-friendly that symantic search can be apply. (e.g., Career Challenges in Tech:).

7. Speaker Handling (if applicable): If multiple speakers discuss the same topic, group their contributions under one title.

8. Tone: Retain the speaker’s style but fix minor grammar issues if needed.

9. Don't summarize: Don't summarize the script. Make it a well struct text accoriding above instruction.
""",
        input_variables=["transcript"],
    )

    promptTemplate = prompt.invoke({"transcript": transcript})

    return promptTemplate


# x = input("transcript: ")

# ans = PrompForStructDoc(x)

# print(ans)
