from http.client import HTTPException

from fastapi import APIRouter, Path
import motor.motor_asyncio
from typing import List, Any
from chatbot.web.api.docs.schema import ChatMessageModel
from fastapi import Body
from bson import ObjectId
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


@router.post("/new", response_description="Add new conversation")
async def create_new_conversation():
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 格式化时间字符串
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
    chat_messages = {"message_list": [{
      "message":
        "Hello jiawen, I'm a professional Software Engineer, Ask me anything!",
      "sentTime": "just now",
      "sender": "ChatGPT",
      "direction": "incoming",
      "position": "last",
      "type": "html",
    }], "created_time": time_string,
                     "edited_time": time_string}
    inserted_id = await add_chat_messages(chat_messages)
    return {"status": "created", "inserted_id": str(inserted_id)}


@router.post("/messages", response_description="Update or create chat messages")
async def create_or_update_chat_messages(chat_messages: ChatMessageModel):
    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")

    if chat_messages.conversation_id:
        # 这里我们尝试更新现有对话
        result = await message_collection.update_one(
            {"_id": chat_messages.conversation_id},
            {"$set": {"message_list": chat_messages.messages,
                      "edited_time": time_string}},
            upsert=True  # 如果找不到id则插入新纪录
        )
        if result.matched_count:
            return {"status": "updated",
                    "conversation_id": str(chat_messages.conversation_id)}
        elif result.upserted_id:
            return {"status": "created", "inserted_id": str(result.upserted_id)}
        else:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # 这里我们创建新的对话
        chat_document = {
            "message_list": chat_messages.messages,
            "created_time": time_string,
            "edited_time": time_string
        }
        result = await message_collection.insert_one(chat_document)
        return {"status": "created", "inserted_id": str(result.inserted_id)}


@router.get("/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: str):
    try:
        # 尝试把字符串conversation_id转换为ObjectId
        object_id = ObjectId(conversation_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid conversation ID") from e

    # 使用ObjectId来查询对应的文档
    result = await message_collection.find_one({"_id": object_id})
    if result:
        # 返回messages字段
        return {"messages": result.get("message_list", [])}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str = Path(...,
                                                          description="The ID of the conversation to delete")) -> Any:
    # 尝试将 ID 转换为 ObjectId
    try:
        obj_id = ObjectId(conversation_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid conversation ID format")

    # 在数据库中执行删除操作
    delete_result = await message_collection.delete_one({"_id": obj_id})

    # 检查是否有文档被删除（matched_count > 0）
    if delete_result.deleted_count:
        return {"status": "deleted", "deleted_id": str(obj_id)}
    else:
        raise HTTPException(status_code=404,
                            detail=f"Conversation with ID {conversation_id} not found")


@router.get("/conversations")
async def get_conversation_ids():
    # 查询所有文档的_id字段
    documents = await message_collection.find({},
                                              {"_id": 1, "message_list": 1}).to_list(
        None)
    document_ids = [{"id": str(doc["_id"]),
                     "last_message": doc["message_list"][-1]['message']} for doc in
                    documents]
    return {"conversation_ids": document_ids}
