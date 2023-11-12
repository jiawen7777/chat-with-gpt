import { useState } from "react";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { Button } from "@chatscope/chat-ui-kit-react";

const serverBaseURL = "http://localhost:8000";

const App = () => {
  const [data, setData] = useState([]);

  const fetchData = async () => {
      await fetchEventSource(`${serverBaseURL}/api/chat/stream`, {
        method: "GET",
        headers: {
          Accept: "text/event-stream",
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
          
          console.log(event.data);
          const parsedData = event.data;
          setData((data) => [...data, parsedData]);
        },
        onclose() {
          console.log("Connection closed by the server");
        },
        onerror(err) {
          console.log("There was an error from server", err);
        },
      });
    };

  return (
    <div style={{ display: "grid", placeItems: "center" }}>
      <h1>Anwser</h1>
      <Button onClick={fetchData}></Button>
      
        {data}
      
    </div>
  );
};

export default App;
