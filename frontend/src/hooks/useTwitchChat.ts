'use client';

import { useState, useEffect, useCallback } from 'react';
import type { TwitchMessage } from '../types';
import { MAX_CHAT_MESSAGES, RECONNECT_INTERVAL } from '../lib/constants';

export function useTwitchChat(channelName: string) {
  const [messages, setMessages] = useState<TwitchMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const addMessage = useCallback((message: TwitchMessage) => {
    setMessages(prev => {
      const newMessages = [...prev, message];
      return newMessages.slice(-MAX_CHAT_MESSAGES); // Keep only the latest messages
    });
  }, []);

  const connect = useCallback(() => {
    try {
      // WebSocket connection logic will go here
      setIsConnected(true);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect to chat');
      setIsConnected(false);
      
      // Attempt to reconnect
      setTimeout(connect, RECONNECT_INTERVAL);
    }
  }, [channelName]);

  useEffect(() => {
    connect();
    
    return () => {
      // Cleanup WebSocket connection
      setIsConnected(false);
    };
  }, [connect]);

  return {
    messages,
    isConnected,
    error,
    addMessage,
  };
} 