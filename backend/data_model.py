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
    videoID: Annotated[str, Field(..., description="The video ID")]

class startdata(BaseModel):
    video_url: Annotated[str, Field(..., description="Youtube video url")]

class UserData(BaseModel):
    
    """This model validate user data."""

    videoID: Annotated[str, Field(..., description="The video ID..")]
    sessionID: Annotated[str, Field(..., description="User session ID..")]
    user_query: Annotated[str, Field(..., description="This variable hold user query.")]


class ResponseData(BaseModel):
    
    """This model validate api response data."""

    sessionID: Annotated[str, Field(..., description="User session ID..")]
    aiAnswer: Annotated[str, Field(..., description="the ai response of the last query...")]
    videoID: Annotated[str, Field(..., description="The video ID..")]
