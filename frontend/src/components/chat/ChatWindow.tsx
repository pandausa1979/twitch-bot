'use client';

import { useRef, useEffect } from 'react';
import { useTwitchChat } from '@/hooks/useTwitchChat';
import { ChatMessage } from './ChatMessage';
import { Button } from '../ui/button';

interface ChatWindowProps {
  channelName: string;
}

export function ChatWindow({ channelName }: ChatWindowProps) {
  const chatRef = useRef<HTMLDivElement>(null);
  const { messages, isConnected, error, addMessage } = useTwitchChat(channelName);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-full bg-zinc-900 rounded-lg overflow-hidden">
      {/* Chat header */}
      <div className="flex items-center justify-between px-4 py-2 bg-zinc-800">
        <h2 className="text-lg font-semibold text-white">
          Chat: {channelName}
        </h2>
        <div className="flex items-center space-x-2">
          <span className={`w-2 h-2 rounded-full ${
            isConnected ? 'bg-green-500' : 'bg-red-500'
          }`} />
          <span className="text-sm text-gray-300">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      {/* Chat messages */}
      <div 
        ref={chatRef}
        className="flex-1 overflow-y-auto chat-messages p-4 space-y-2"
      >
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {error && (
          <div className="text-red-500 text-center py-2">
            {error}
          </div>
        )}
      </div>

      {/* Chat input - placeholder for future implementation */}
      <div className="p-4 bg-zinc-800">
        <div className="flex space-x-2">
          <input
            type="text"
            placeholder="Send a message..."
            className="flex-1 bg-zinc-700 text-white rounded px-3 py-2"
            disabled
          />
          <Button variant="primary" disabled>
            Send
          </Button>
        </div>
      </div>
    </div>
  );
} 