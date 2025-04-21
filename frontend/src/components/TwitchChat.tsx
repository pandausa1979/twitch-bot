'use client';

import { useEffect, useState, useCallback } from 'react';

interface ChatMessage {
  author: string;
  content: string;
  timestamp: string;
}

export default function TwitchChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [ws, setWs] = useState<WebSocket | null>(null);

  const connectWebSocket = useCallback(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.hostname}:8080/ws`;
    
    const socket = new WebSocket(wsUrl);
    
    socket.onopen = () => {
      setConnected(true);
      setError(null);
      console.log('WebSocket connected');
    };
    
    socket.onclose = () => {
      setConnected(false);
      console.log('WebSocket disconnected');
      // Attempt to reconnect after 5 seconds
      setTimeout(connectWebSocket, 5000);
    };
    
    socket.onerror = (event) => {
      setError('Connection error occurred');
      console.error('WebSocket error:', event);
    };
    
    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        setMessages(prev => [...prev, message]);
      } catch (err) {
        console.error('Error parsing message:', err);
      }
    };
    
    setWs(socket);
    
    return () => {
      socket.close();
    };
  }, []);

  useEffect(() => {
    const cleanup = connectWebSocket();
    return cleanup;
  }, [connectWebSocket]);

  return (
    <div className="flex flex-col h-full bg-gray-800 text-white p-4 rounded-lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold">Twitch Chat</h2>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-sm">{connected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </div>
      
      {error && (
        <div className="bg-red-500 text-white p-2 rounded mb-4">
          {error}
        </div>
      )}
      
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