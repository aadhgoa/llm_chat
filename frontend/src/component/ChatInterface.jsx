// src/ChatInterface.js
import React, { useState } from 'react';
import axios from 'axios';
import '../chatinterface.css'

const ChatInterface = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  const handleAskQuestion = async () => {
    try {
      const requestBody = { question };
      const response = await axios.post('https://llm-chat-backend.onrender.com/chat', requestBody);
      setResponse(response.data.response);
    } catch (error) {
      console.error('Error asking question:', error);
    }
  };

  const handleClearMemory = async () => {
    try {
      await axios.get('https://llm-chat-backend.onrender.com/clear-memory');
      setResponse('Memory cleared successfully.');
    } catch (error) {
      console.error('Error clearing memory:', error);
    }
  };

  
  return (
    <div className="container">
      <div className="chat-box">
        <h1>Chat Interface</h1>
        <input
          className="question-input"
          type="text"
          placeholder="Enter your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <div className="buttons">
          <button onClick={handleAskQuestion}>Ask</button>
          <button onClick={handleClearMemory}>Clear Memory</button>
        </div>
        {response && <p className="response">AI Response: {response}</p>}
      </div>
    </div>
  );
};

export default ChatInterface;
