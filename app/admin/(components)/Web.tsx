import React, { useEffect, useState } from 'react';

// Define props type
interface WebSocketComponentProps {
  wsUrl: string;
}

const WebSocketComponent: React.FC<WebSocketComponentProps> = ({ wsUrl }) => {
  const [messages, setMessages] = useState<any[]>([]);

  useEffect(() => {
    // Create WebSocket connection.
    const socket = new WebSocket(wsUrl);

    // Connection opened
    socket.addEventListener('open', () => {
    });

    // Listen for messages
    socket.addEventListener('message', (event) => {
      const data= JSON.parse(event.data).users
      setMessages((prev) => [...prev, ...data]);
    });

    // Cleanup on unmount
    return () => {
      socket.close();
    };
  }, [wsUrl]); // Re-run effect if wsUrl changes

  return (
    <div>
      <h2>Messages from WebSocket:</h2>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message?.username}</li>
        ))}
      </ul>
    </div>
  );
};

export default WebSocketComponent;
