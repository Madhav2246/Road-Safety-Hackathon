import { useState } from "react";
import { api } from "../api/backend";
import "./ChatBot.css";

export default function ChatBot({ context }) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const send = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages(m => [...m, userMsg]);
    setInput("");

    const res = await api.askChatbot(input, context);
    setMessages(m => [...m, { role: "bot", text: res.answer }]);
  };

  return (
    <div className="chatbot">
      <button className="chat-toggle" onClick={() => setOpen(!open)}>
        AI Assistant
      </button>

      {open && (
        <div className="chat-window">
          <div className="chat-messages">
            {messages.map((m, i) => (
              <div key={i} className={`msg ${m.role}`}>
                {m.text}
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Ask about cost, clause, chart..."
            />
            <button onClick={send}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}
