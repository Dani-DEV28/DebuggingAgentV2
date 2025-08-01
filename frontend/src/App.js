import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([
    { sender: "agent", text: "Describe your symptoms to begin." }
  ]);
  const [input, setInput] = useState("");
  const [followupAnswers, setFollowupAnswers] = useState({});

  const sendMessage = async (text) => {
    setMessages((msgs) => [...msgs, { sender: "user", text }]);
    const payload = {
      symptoms: text,
      followupAnswers
    };
    const res = await fetch("http://localhost:3001/analyze-symptoms", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    setMessages((msgs) => [
      ...msgs,
      { sender: "agent", text: data.analysis }
    ]);
    if (data.requiresFollowup && data.followupQuestions.length > 0) {
      data.followupQuestions.forEach((q) => {
        setMessages((msgs) => [
          ...msgs,
          { sender: "agent", text: q }
        ]);
      });
    }
  };

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage(input.trim());
    setInput("");
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>DebuggingAgentV2: Medical AI Chat</h2>
      <div style={{
        border: "1px solid #ccc", borderRadius: 8, padding: 16, minHeight: 300, marginBottom: 16
      }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            textAlign: msg.sender === "user" ? "right" : "left",
            margin: "8px 0"
          }}>
            <b>{msg.sender === "user" ? "You" : "Agent"}:</b> {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSend} style={{ display: "flex" }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          style={{ flex: 1, padding: 8, borderRadius: 4, border: "1px solid #ccc" }}
          placeholder="Type your symptoms..."
        />
        <button type="submit" style={{ marginLeft: 8, padding: "8px 16px" }}>Send</button>
      </form>
    </div>
  );
}

export default App;
