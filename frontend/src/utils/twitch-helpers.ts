import type { TwitchMessage } from '../types';

/**
 * Parse Twitch chat message badges
 */
export function parseBadges(badgesString: string): string[] {
  if (!badgesString) return [];
  return badgesString.split(',').map(badge => badge.split('/')[0]);
}

/**
 * Format timestamp for chat messages
 */
export function formatTimestamp(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}

/**
 * Sanitize chat message to prevent XSS
 */
export function sanitizeMessage(message: string): string {
  return message
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Format chat message with emotes and mentions
 */
export function formatChatMessage(message: TwitchMessage): string {
  let formattedMessage = sanitizeMessage(message.message);
  
  // Add user mentions highlighting
  formattedMessage = formattedMessage.replace(
    /@(\w+)/g,
    '<span class="text-primary">@$1</span>'
  );
  
  return formattedMessage;
} 