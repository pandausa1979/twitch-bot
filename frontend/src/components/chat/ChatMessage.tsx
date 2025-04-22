'use client';

import { memo } from 'react';
import type { TwitchMessage } from '@/types';
import { formatTimestamp, formatChatMessage } from '@/utils/twitch-helpers';

interface ChatMessageProps {
  message: TwitchMessage;
}

const ChatMessage = memo(function ChatMessage({ message }: ChatMessageProps) {
  return (
    <div className="message-container group">
      <span className="text-xs text-gray-400">
        {formatTimestamp(new Date(message.timestamp))}
      </span>
      {message.badges?.map((badge, index) => (
        <span key={index} className="twitch-badge">
          {badge}
        </span>
      ))}
      <span 
        className="username" 
        style={{ color: message.color || '#ffffff' }}
      >
        {message.username}
      </span>
      <span 
        className="message"
        dangerouslySetInnerHTML={{ __html: formatChatMessage(message) }}
      />
    </div>
  );
});

export { ChatMessage }; 