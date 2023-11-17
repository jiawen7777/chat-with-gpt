import ChatPage from "./ChatPage"; // 引入你的chatscope.io聊天界面组件
import SideBar from "./SideBar";
import axios from "axios";
import { useEffect, useState } from "react";
import './App.css';  // 假设你的样式表文件叫做 App.css
// 省略其它import和代码

function App() {
  // 状态
  const [conversations, setConversations] = useState([]); // 对话列表的状态
  const [selectedConversationId, setSelectedConversationId] = useState(null); // 选中对话ID
  const initMessage = {
      message:
        "Hello jiawen, I'm a professional Software Engineer, Ask me anything!",
      sentTime: "just now",
      sender: "ChatGPT",
      direction: "incoming",
      position: "last",
      type: "html",
    }
  const [messages, setMessages] = useState([initMessage]);
  const serverBaseURL = "http://localhost:8001/api";

  // 获取对话列表
  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const response = await axios.get(serverBaseURL + "/docs/conversations");
        setConversations(response.data.conversation_ids); // 假设API返回的直接是对话列表数组
      } catch (error) {
        console.error("Error fetching conversations:", error);
        // TODO:设置一个错误状态，并在UI中显示错误消息
      }
    };

    fetchConversations();
  }, []); // 空数组作为依赖项，意味着effect仅在组件挂载时执行一次

  // 选中对话并获取消息
  const onSelectConversation = async (conversationId) => {
    setSelectedConversationId(conversationId);
    try {
      const response = await axios.get(
        serverBaseURL + `/docs/conversations/${conversationId}/messages`
      );
      setMessages(response.data.messages); // 假设API返回的消息格式符合 ChatPage 组件的要求
    } catch (error) {
      console.error(
        "Error fetching messages for conversation:",
        conversationId,
        error
      );
      // TODO:设置一个错误状态，并在UI中显示错误消息
    }
  };

  return (
    <div style={{ display: "flex", height: "100%", padding: 0 }}>
      <div style={{ flex: 2, padding: 0 }}>
        <SideBar
          selectedConversationId={selectedConversationId}
          setSelectedConversationId={setSelectedConversationId}
          conversations={conversations}
          onSelectConversation={onSelectConversation}
          setConversations={setConversations}
          initMessage={initMessage}
          setMessages={setMessages}
        />
      </div>
      <div style={{ flex: 6, padding: 0 }}>
        <ChatPage
          selectedConversationId={selectedConversationId}
          setSelectedConversationId={setSelectedConversationId}
          messages={messages}
          setMessages={setMessages}
          conversations={conversations}
          setConversations={setConversations}
        />
      </div>
    </div>
  );



}

export default App;
