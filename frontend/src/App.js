// src/App.js
import React, { useState, useRef, useEffect } from 'react';
import './App.css'; // Có thể cần điều chỉnh CSS

// Component cho một tin nhắn
function Message({ message, sources }) {
  const { role, content, timestamp } = message;
  const isUser = role === 'user';

  return (
    <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-header">
        <strong>{isUser ? 'Bạn' : 'Sapali-GPT'}</strong>
        <span className="timestamp"> {new Date(timestamp).toLocaleTimeString()}</span>
      </div>
      <div className="message-content">
        {content}
        {sources && sources.length > 0 && (
          <div className="sources">
            <details>
              <summary>Nguồn tham khảo</summary>
              <ul>
                {sources.map((source, index) => (
                  <li key={index}>
                    {source.source} (Chunk: {source.chunk_id})
                  </li>
                ))}
              </ul>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}

function App() {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState([
    // { id: 1, role: 'assistant', content: 'Xin chào! Bạn cần hỏi gì về sản phẩm hoặc chính sách công ty?', timestamp: new Date().toISOString() }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Tự động cuộn xuống tin nhắn mới nhất
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus vào ô input khi component mount
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return; // Ngăn gửi khi rỗng hoặc đang load

    const userMessage = {
      id: Date.now(), // ID tạm thời
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    // Cập nhật UI ngay lập tức với tin nhắn của người dùng
    setMessages((prev) => [...prev, userMessage]);
    setInputValue(''); // Xóa ô input
    setIsLoading(true); // Bắt đầu trạng thái loading

    try {
      // Gửi yêu cầu đến API backend
      const response = await fetch('http://localhost:8000/query', { // Đảm bảo URL đúng
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage.content }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('API Response:', data); // Debug

      const botMessage = {
        id: Date.now() + 1, // ID tạm thời
        role: 'assistant',
        content: data.answer || 'Xin lỗi, tôi không thể trả lời câu hỏi này.',
        timestamp: new Date().toISOString(),
        sources: data.sources || [], // Dữ liệu nguồn từ API
      };

      // Cập nhật UI với phản hồi của bot
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Lỗi khi gọi API:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Xin lỗi, đã có lỗi xảy ra khi kết nối với hệ thống: ${error.message}`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false); // Kết thúc trạng thái loading
      if (inputRef.current) {
        inputRef.current.focus(); // Focus lại vào ô input sau khi gửi
      }
    }
  };

  return (
    <div className="App">
      <header className="chat-header">
        <h1>SapaliGPT</h1>
      </header>
      <main className="chat-container">
        <div className="messages-panel">
          {messages.map((msg) => (
            <Message key={msg.id} message={msg} sources={msg.sources} />
          ))}
          {isLoading && (
            <div className="message bot-message">
              <div className="message-content">
                <em>Đang xử lý...</em>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Hỏi tôi bất cứ điều gì..."
            ref={inputRef} // Tham chiếu để focus
            disabled={isLoading} // Vô hiệu hóa khi đang load
          />
          <button type="submit" disabled={isLoading || !inputValue.trim()}> {/* Vô hiệu hóa khi rỗng hoặc đang load */}
            Gửi
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;