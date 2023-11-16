import typing

from pydantic import BaseModel 
from typing import Optional, List, Any
from datetime import datetime 


    
    
class ChatMessage(BaseModel): 
    message: str 
    sentTime: str
    sender: str 
    direction: str 
    position: str 
    type: str 
    
    
class ChatMessageList(BaseModel): 
    message_list: List[ChatMessage]
    
class ChatMessageAddModel(BaseModel): 
    message_list: List[ChatMessage]
    created_time: str
    edited_time: str