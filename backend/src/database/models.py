"""Data models for the Twitch bot application."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ChatMessage:
    """Represents a chat message from Twitch."""
    channel: str
    user: str
    message: str
    timestamp: datetime
    user_id: Optional[str] = None
    message_id: Optional[str] = None
    is_mod: bool = False
    is_subscriber: bool = False
    
    def to_dict(self) -> dict:
        """Convert the message to a dictionary for MongoDB storage."""
        return {
            'channel': self.channel,
            'user': self.user,
            'message': self.message,
            'timestamp': self.timestamp,
            'user_id': self.user_id,
            'message_id': self.message_id,
            'is_mod': self.is_mod,
            'is_subscriber': self.is_subscriber
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ChatMessage':
        """Create a ChatMessage instance from a dictionary."""
        return cls(
            channel=data['channel'],
            user=data['user'],
            message=data['message'],
            timestamp=data['timestamp'],
            user_id=data.get('user_id'),
            message_id=data.get('message_id'),
            is_mod=data.get('is_mod', False),
            is_subscriber=data.get('is_subscriber', False)
        ) 