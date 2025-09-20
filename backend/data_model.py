"""This is pydantic data model. This model validate user data and api response data."""

from pydantic import (
    BaseModel,
    Field
)
from typing import (
    Annotated
)


class SessionIDData(BaseModel):

    """This model validate session ID."""

    sessionID: Annotated[str, Field(..., description="Session ID.")]

class UserData(BaseModel):
    
    """This model validate user data."""

    sessionID: Annotated[str, Field(..., description="This variable hold video transcript.")]
    user_query: Annotated[str, Field(..., description="This variable hold user query.")]


class ResponseData(BaseModel):
    
    """This model validate api response data."""

    sessionID: Annotated[str, Field(..., description="User Video transcrit")]
    aiAnswer: Annotated[str, Field(..., description="the ai response of the last query...")]
