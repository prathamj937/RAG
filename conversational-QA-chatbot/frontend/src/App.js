import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  const [loading, setLoading] = useState(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    const userMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/ask", {
        question: question,
        session_id: "user1",
      });

      const botMessage = { role: "bot", content: res.data.answer };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "Something went wrong!" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>💬 Conversational RAG Chat</h2>
      <div style={styles.chatBox}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              ...styles.message,
              alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
              backgroundColor: msg.role === "user" ? "#DCF8C6" : "#E5E5EA",
              color: "#000",
            }}
          >
            <strong>{msg.role === "user" ? "You" : "Bot"}:</strong>{" "}
            {msg.content}
          </div>
        ))}
        {loading && <div style={styles.loading}>Bot is typing...</div>}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something..."
          style={styles.input}
        />
        <button type="submit" style={styles.button}>
          Send
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 600,
    margin: "auto",
    padding: 20,
    fontFamily: "Segoe UI, sans-serif",
  },
  heading: {
    textAlign: "center",
    color: "#333",
  },
  chatBox: {
    border: "1px solid #ccc",
    borderRadius: 10,
    padding: 10,
    minHeight: 300,
    maxHeight: 400,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    backgroundColor: "#f9f9f9",
    boxShadow: "0 0 10px rgba(0,0,0,0.05)",
  },
  message: {
    maxWidth: "80%",
    padding: "10px 15px",
    borderRadius: 15,
    margin: "5px 0",
    fontSize: 15,
    lineHeight: 1.4,
    wordWrap: "break-word",
  },
  loading: {
    alignSelf: "flex-start",
    fontStyle: "italic",
    color: "#999",
  },
  form: {
    display: "flex",
    marginTop: 10,
  },
  input: {
    flex: 1,
    padding: 10,
    borderRadius: 20,
    border: "1px solid #ccc",
    outline: "none",
    marginRight: 10,
    fontSize: 14,
  },
  button: {
    padding: "10px 20px",
    borderRadius: 20,
    border: "none",
    backgroundColor: "#007bff",
    color: "#fff",
    fontWeight: "bold",
    cursor: "pointer",
  },
};

export default App;
