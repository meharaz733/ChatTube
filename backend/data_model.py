"""This is pydantic data model. This model validate user data and api response data."""

from pydantic import (
    BaseModel,
    Field
)
from typing import (
    Annotated,
    Optional,
    List
)

class User_data(BaseModel):
    """This model validate user data."""
    transcript: Annotated[str, Field(..., description="This variable hold video transcript.")]
    user_query: Annotated[str, Field(..., description="This variable hold user query.")]
    chat_history: Annotated[Optional[List[str]], Field(default=None, description="Chat history between user and AI model")]


class Response_data(BaseModel):
    """This model validate api response data."""
    transcript: Annotated[str, Field(..., description="User Video transcrit")]
    chat_history: Annotated[List[str], Field(..., description="Chat history between user and AI model")]
