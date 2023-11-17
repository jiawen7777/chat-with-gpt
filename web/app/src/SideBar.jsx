/* eslint-disable react/jsx-key */
/* eslint-disable react/prop-types */

import {
  ConversationList,
  Conversation,
  Button,
} from "@chatscope/chat-ui-kit-react";

import axios from "axios";
import LayersClearIcon from "@mui/icons-material/LayersClear";
// eslint-disable-next-line react/prop-types
function SideBar({
  selectedConversationId,
  setSelectedConversationId,
  conversations,
  onSelectConversation,
  setConversations,
  initMessage,
  setMessages,
}) {
  const serverBaseURL = "http://localhost:8001/api";
  const createConversation = async () => {
    try {
      const response = await axios.post(serverBaseURL + "/docs/new");
      if (response.data && response.data.status === "created") {
        // 更新 selectedConversationId 为新创建的会话的 ID
        const insertedId = response.data.inserted_id;
        setSelectedConversationId(insertedId);
        // 如果需要，这里也可以添加新会话的 ID 到会话列表的状态中去
        setConversations([
          ...conversations,
          {
            id: insertedId,
            last_message: "New Message",
          },
        ]);
        setMessages([initMessage]);
      }
    } catch (error) {
      console.error("Error creating a new conversation:", error);
      // TODO: 根据你的应用逻辑，你可能想在这里设置一个错误状态并在 UI 中显示错误消息
    }
  };

  const handleDelete = async (conversationId) => {
    try {
      // 调用 API 删除对话
      const response = await axios.delete(
        serverBaseURL + `/docs/conversations/${conversationId}`
      );

      // 从状态中移除被删除的对话
      setConversations((conversations) =>
        conversations.filter((c) => c.id !== response.data.deleted_id)
      );
    } catch (error) {
      console.error("Error deleting conversation:", error);
      // TODO: 在 UI 中展示错误信息
    }
  };

  return (
    <div>
      <ConversationList>
        <Button
          variant="contained"
          color="primary"
          onClick={createConversation}
          style={{
            marginLeft: 10,
            marginRight: 10,
            paddingTop: 20,
            paddingBottom: 20,
            backgroundColor: "#c6e5fa",
            color: "black",
            width: "80%",
          }}
        >
          New Conversation
        </Button>
        {
          // eslint-disable-next-line react/prop-types
          conversations.map((conversation) => (
            <div>
              <Conversation
                onClick={() => onSelectConversation(conversation.id)}
                name={`Conversation`}
                info={
                  conversation.last_message
                    ? `${conversation.last_message.slice(0, 30)}${
                        conversation.last_message.length > 30 ? "..." : ""
                      }`
                    : ""
                }
                style={{
                  innerWidth: "50%",
                }}
                active={conversation.id === selectedConversationId}
              >
                <Conversation.Operations visible>
                  <LayersClearIcon
                    onClick={() => handleDelete(conversation.id)}
                  ></LayersClearIcon>
                </Conversation.Operations>
              </Conversation>
            </div>
          ))
        }
      </ConversationList>
    </div>
  );
}

export default SideBar;
