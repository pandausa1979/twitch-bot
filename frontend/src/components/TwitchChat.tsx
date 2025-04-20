'use client';

import { useEffect, useState } from 'react';

interface ChatMessage {
  author: string;
  content: string;
  timestamp: string;
}

export default function TwitchChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // TODO: Implement WebSocket connection to our Python backend
    const mockMessages = [
      {
        author: 'TestUser1',
        content: 'Hello from Twitch!',
        timestamp: new Date().toISOString()
      },
      {
        author: 'TestUser2',
        content: 'Testing the chat interface',
        timestamp: new Date().toISOString()
      }
    ];

    setMessages(mockMessages);
    setConnected(true);
  }, []);

  return (
    <div className="flex flex-col h-full bg-gray-800 text-white p-4 rounded-lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold">Twitch Chat</h2>
        <div className={`w-3 h-3 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
      </div>
      
      <div className="flex-1 overflow-y-auto space-y-2">
        {messages.map((message, index) => (
          <div key={index} className="bg-gray-700 p-2 rounded">
            <div className="flex items-center gap-2">
              <span className="font-bold text-purple-400">{message.author}</span>
              <span className="text-xs text-gray-400">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <p className="text-gray-100">{message.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
} 