from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId



class ChatMessage(BaseModel):
    message: str
    sentTime: str
    sender: str
    direction: str
    position: str
    type: str




# 用于验证和转换ObjectId的自定义字段类
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type='string')

# 定义接收到的聊天信息的模型
class ChatMessageModel(BaseModel):
    conversation_id: Optional[PyObjectId] = None
    messages: List[dict]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
