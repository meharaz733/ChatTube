"""
Prompt template for chat model. It consists of a transcript, user query and chat history and returns a template ready to pass to the model.

"""

from langchain_core.prompts import PromptTemplate
from data_model import UserData


def Prompt_template(data: UserData):
    """
    Takes user input as a User_data model (Pydantic) and returns a PromptTemplate.

    """
    prompt = PromptTemplate(
        template="""
            
        """,
        input_variables=["query"],
    )

    return prompt


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

3. Conciseness: Keep paragraphs under 1000 words. Split long topics into (Part 1), (Part 2), etc with same title.

4. Avoid Redundancy: Merge repeated points into one paragraph.

5. Direct Start: Begin immediately with the first topic (no "Here’s the trimmed version...").

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
