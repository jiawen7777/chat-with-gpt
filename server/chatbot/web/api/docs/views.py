from fastapi import APIRouter
import motor.motor_asyncio
from typing import List
from chatbot.web.api.docs.schema import ChatMessage, ChatMessageList, ChatMessageAddModel
from fastapi import Body 
import datetime


router = APIRouter()
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017/?readPreference=primary&ssl=false&directConnection=true")
db = client.chatbot
message_collection = db.get_collection("messages")


router = APIRouter() 
 
 
async def add_chat_messages(chat_messages: dict):
    result = await message_collection.insert_one(chat_messages)
    inserted_id = result.inserted_id
    return inserted_id

@router.post("/conversation", response_description="Add new chat messages") 
async def create_chat_messages(): 
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 格式化时间字符串
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
    chat_messages = {"message_list": [], "created_time": time_string, "edited_time": time_string}
    inserted_id = await add_chat_messages(chat_messages) 
    return {"inserted_id": str(inserted_id)}

@router.post("/messages/", 
             response_description="Add new chat messages") 
async def create_chat_messages(chat_messages: ChatMessageList): 
        # 获取当前时间
    current_time = datetime.datetime.now()
    # 格式化时间字符串
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
    chat_messages = ChatMessageAddModel(message_list=chat_messages.message_list,
                        created_time=time_string,
                        edited_time=time_string)
    inserted_id = await add_chat_messages(chat_messages) 
    return {"inserted_id": inserted_id}



@router.get("/documents")
async def get_document_ids():
    # 查询所有文档的_id字段
    documents = await message_collection.find({}, {"_id": 1}).to_list(None)
    document_ids = [str(doc["_id"]) for doc in documents]
    
    return {"document_ids": document_ids}