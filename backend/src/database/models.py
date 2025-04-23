"""Data models for the Twitch bot application."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

class Channel:
    """Represents a Twitch channel being monitored."""
    
    def __init__(
        self,
        name: str,
        joined_at: datetime,
        last_activity: Optional[datetime] = None,
        is_active: bool = True
    ):
        """
        Initialize a Channel instance.
        
        Args:
            name: The channel name
            joined_at: When the bot joined the channel
            last_activity: When the channel was last active
            is_active: Whether the channel is currently being monitored
        """
        self.name = name
        self.joined_at = joined_at
        self.last_activity = last_activity or joined_at
        self.is_active = is_active
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Channel':
        """
        Create a Channel instance from a dictionary.
        
        Args:
            data: Dictionary containing channel data
            
        Returns:
            Channel: A new Channel instance
        """
        return cls(
            name=data['name'],
            joined_at=data['joined_at'],
            last_activity=data.get('last_activity'),
            is_active=data.get('is_active', True)
        )
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Channel instance to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the channel
        """
        return {
            'name': self.name,
            'joined_at': self.joined_at,
            'last_activity': self.last_activity,
            'is_active': self.is_active
        }

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

@dataclass
class ChannelConfig:
    """Represents channel-specific configuration."""
    channel: str
    enabled_commands: List[str]
    custom_commands: Dict[str, str]
    message_retention_days: int = 30
    auto_mod_settings: Dict[str, Any] = None
    welcome_message: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert the config to a dictionary for MongoDB storage."""
        return {
            'channel': self.channel,
            'enabled_commands': self.enabled_commands,
            'custom_commands': self.custom_commands,
            'message_retention_days': self.message_retention_days,
            'auto_mod_settings': self.auto_mod_settings or {},
            'welcome_message': self.welcome_message
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ChannelConfig':
        """Create a ChannelConfig instance from a dictionary."""
        return cls(
            channel=data['channel'],
            enabled_commands=data['enabled_commands'],
            custom_commands=data['custom_commands'],
            message_retention_days=data.get('message_retention_days', 30),
            auto_mod_settings=data.get('auto_mod_settings', {}),
            welcome_message=data.get('welcome_message')
        ) 