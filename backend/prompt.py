"""
Prompt template for chat model. It consists of a transcript, user query and chat history and returns a template ready to pass to the model.

"""

from langchain_core.prompts import PromptTemplate
from data_model import User_data

def Prompt_template(data: User_data):
    """
    Takes user input as a User_data model (Pydantic) and returns a PromptTemplate.
    
    """
    prompt = PromptTemplate(
        template= """
            
        """,
        input_variables = ["query"]
        
    )
    
    return prompt
