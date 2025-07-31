"""
Prompt template for chat model. It's consist user query as string and return a template rady to pass to model.
"""
from langchain_core.prompts import PromptTemplate


class Prompt_template():
    """This class take user input as User_data model(pydantic)."""
    promt = PromptTemplate(
        template= """
            
        """,
        input_variables = ["query"]
        
    )
