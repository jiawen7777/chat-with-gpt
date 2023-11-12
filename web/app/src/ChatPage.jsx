import { useState } from "react";
import "./App.css";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import {
  ConversationHeader,
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
  Avatar,
} from "@chatscope/chat-ui-kit-react";
import ReactMarkdown from "react-markdown";
import GPTLogo from "./assets/gpt_logo.png";
import UserLogo from "./assets/user_logo.png";
import {
  Container,
  Select,
  MenuItem,
  Grid,
  InputLabel,
  Input,
} from "@mui/material";

// "Explain things like you would to a 10 year old learning how to code."
const systemMessage = {
  //  Explain things like you're talking to a software professional with 5 years of experience.
  role: "system",
  content:
    "Explain things like you're talking to a software professional with 2 years of experience.",
};

function ChatPage() {
  const [messages, setMessages] = useState([
    {
      message:
        "Hello jiawen, I'm a professional Software Engineer, Ask me anything!",
      sentTime: "just now",
      sender: "ChatGPT",
      direction: "incoming",
      position: "last",
      type: "html",
    },
  ]);

  const [model, setModel] = useState("");
  const [tmp, setTmp] = useState(0.0);

  const handleChange = (event) => {
    setModel(event.target.value);
  };

  const handleTemChange = (event) => {
    setTmp(event.target.value);
  };

  const [isTyping, setIsTyping] = useState(false);
  let botMessageContent = "";
  const handleSend = async (message) => {
    const newMessage = {
      message,
      direction: "outgoing",
      sender: "user",
      position: "last",
      type: "html",
      sentTime: new Date().toDateString(),
    };

    const newMessages = [...messages, newMessage];

    setMessages(newMessages);

    // Initial system message to determine ChatGPT functionality
    // How it responds, how it talks, etc.
    setIsTyping(true);
    botMessageContent = "";
    await processMessageToChatGPT(newMessages);
  };

  async function processMessageToChatGPT(chatMessages) {
    // messages is an array of messages
    // Format messages for chatGPT API
    // API is expecting objects in format of { role: "user" or "assistant", "content": "message here"}
    // So we need to reformat
    let apiMessages = chatMessages.map((messageObject) => {
      let role = "";
      if (messageObject.sender === "ChatGPT") {
        role = "assistant";
      } else {
        role = "user";
      }
      return { role: role, content: messageObject.message };
    });

    // Get the request body set up with the model we plan to use
    // and the messages which we formatted above. We add a system message in the front to'
    // determine how we want chatGPT to act.
    const apiRequestBody = {
      model: model,
      messages: [
        systemMessage, // The system message DEFINES the logic of our chatGPT
        ...apiMessages, // The messages from our chat with ChatGPT
      ],
      temperature: tmp,
    };
    const serverBaseURL = "http://localhost:8001";

    const fetchData = async () => {
      await fetchEventSource(`${serverBaseURL}/api/chat/stream`, {
        method: "POST",
        body: JSON.stringify(apiRequestBody),
        headers: {
          Accept: "text/event-stream",
          "Content-Type": "application/json",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        },
        onopen(res) {
          if (res.ok && res.status === 200) {
            console.log("Connection made ", res);
          } else if (
            res.status >= 400 &&
            res.status < 500 &&
            res.status !== 429
          ) {
            console.log("Client side error ", res);
          }
        },
        onmessage(event) {
          let parsedData = event.data;
          console.log(event);
          if (parsedData === "") {
            parsedData = " \n ";
          }
          botMessageContent += parsedData;
          setMessages([
            ...chatMessages,
            {
              message: botMessageContent,
              sender: "ChatGPT",
              direction: "incoming",
              position: "last",
              type: "html",
              sentTime: new Date().toDateString(),
            },
          ]);
        },
        onclose() {
          setIsTyping(false);
          console.log("Connection closed by the server");
        },
        onerror(err) {
          console.log("There was an error from server", err);
        },
      });
    };

    fetchData();
  }

  return (
    <Container style={{ height: "800px", textAlign: "left" }}>
      <MainContainer>
        <ChatContainer>
          <ConversationHeader>
            <ConversationHeader.Content>
              <Grid container spacing={1}>
                <Grid item xs={2}>
                  <h4>Chat GPT</h4>
                </Grid>
                <Grid item xs={2}>
                  <InputLabel>Model</InputLabel>
                  <Select
                    value={model}
                    label="Model"
                    onChange={handleChange}
                    defaultValue="gpt-3.5-turbo"
                  >
                    <MenuItem value={"gpt-4-1106-preview"}>GPT 4</MenuItem>
                    <MenuItem value={"gpt-3.5-turbo"}>GPT 3.5</MenuItem>
                  </Select>
                </Grid>
                <Grid item xs={2}>
                  <InputLabel>Temperature</InputLabel>
                  <Input
                    type="number"
                    step="0.1"
                    value={tmp}
                    onChange={handleTemChange}
                  ></Input>
                </Grid>
              </Grid>
            </ConversationHeader.Content>
          </ConversationHeader>
          <MessageList
            scrollBehavior="smooth"
            typingIndicator={
              isTyping ? <TypingIndicator content="ChatGPT is typing" /> : null
            }
          >
            {messages.map((message, i) => {
              return (
                <Message key={i} model={message}>
                  {message.sender === "ChatGPT" ? (
                    <Avatar src={GPTLogo} name={message.sender} size="md" />
                  ) : (
                    <Avatar src={UserLogo} name={message.sender} size="md" />
                  )}
                  <Message.CustomContent>
                    <ReactMarkdown>{message.message}</ReactMarkdown>
                  </Message.CustomContent>
                  <Message.Footer sentTime={message.sentTime} />
                </Message>
              );
            })}
          </MessageList>

          <MessageInput placeholder="Type message here" onSend={handleSend} />
        </ChatContainer>
      </MainContainer>
    </Container>
  );
}

export default ChatPage;
