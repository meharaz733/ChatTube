"""This is pydantic data model. This model validate user data and api response data."""

from pydantic import (
    BaseModel,
    Field
)
from typing import (
    Annotated,
    Optional,
    List,
    Dict,
    Literal,
    Union
)


class SystemMessageData(BaseModel):
    
    """This model check System Message Data."""
    
    content: Annotated[Optional[str], Field(default=None, description="It will take system message.")]
    additional_kwargs: Annotated[Optional[Dict], Field(default=None, description="This is for additional kwargs for system message.")]
    response_metadata: Annotated[Optional[Dict], Field(default=None, description="this is for response metadata of system message.")]
    type: Annotated[Optional[Literal["system"]], Field(default=None, description="Type of message, it should be system message.")]
    name: Optional[str] = None
    id: Optional[str] = None


class HumanMessageData(SystemMessageData):

    """This model check Human Message Data."""

    type: Annotated[Optional[Literal["human"]], Field(default=None, description="Type of message, it should be human message.")]
    example: Optional[bool] = None


class AIMessageData(HumanMessageData):

    """This model check AI Message Data."""

    type: Annotated[Optional[Literal["ai"]], Field(default=None, description="Type of message, it should be AI message.")]
    tool_calls: Annotated[Optional[List], Field(default=None, description="Name of tools that AI may call.")]
    invalid_tool_calls: Annotated[Optional[List], Field(default=None, description="name of invalid tools.")]
    usage_metadata: Annotated[Optional[Dict], Field(default=None, description="Dict of usage metadata.")]
    



class ChatMessage(BaseModel):

    """Custom model to check user data."""
    
    type: Literal["system", "human", "ai"]
    data: Optional[Union[SystemMessageData, HumanMessageData, AIMessageData]] = None

class UserData(BaseModel):
    
    """This model validate user data."""

    video_url: Annotated[str, Field(..., description="Video url for chatting.")]
    transcript: Annotated[Optional[str], Field(default=None, description="This variable hold video transcript.")]
    user_query: Annotated[str, Field(..., description="This variable hold user query.")]
    chat_history: Annotated[Optional[List[ChatMessage]], Field(default=None, description="Chat history between user and AI model")]


class ResponseData(BaseModel):
    
    """This model validate api response data."""

    video_url: Annotated[str, Field(..., description="the video url that provided by user.")]
    transcript: Annotated[Optional[str], Field(default=None, description="User Video transcrit")]
    chat_history: Annotated[List[ChatMessage], Field(..., description="Chat history between user and AI model")]
