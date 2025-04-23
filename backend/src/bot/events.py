"""Event handling for the Twitch bot."""
import logging
from typing import TYPE_CHECKING
from datetime import datetime, UTC

from twitchio.ext import commands

if TYPE_CHECKING:
    from . import TwitchBot
    from ..database.client import DatabaseClient

logger = logging.getLogger(__name__)

class EventHandler:
    """Handles Twitch events."""
    
    def __init__(self, bot: 'TwitchBot', db_client: 'DatabaseClient'):
        """
        Initialize the event handler.
        
        Args:
            bot: The TwitchBot instance
            db_client: The database client
        """
        self.bot = bot
        self.db_client = db_client
    
    async def on_ready(self):
        """Handle ready event."""
        logger.info(f"Bot is ready! Username: {self.bot.nick}")
        channels = [ch.lstrip('#') for ch in self.bot.initial_channels]
        logger.info(f"Joined channels: {', '.join(channels)}")
    
    async def on_message(self, message):
        """
        Handle message events.
        
        Args:
            message: The message object
        """
        # Skip messages from the bot
        if message.echo:
            return
            
        # Update channel activity
        await self.db_client.update_channel_activity(
            message.channel.name,
            datetime.now(UTC)
        )
        
        # Log message
        logger.debug(
            f"Message in {message.channel.name} from {message.author.name}: {message.content}"
        )
    
    async def on_error(self, error: Exception, data: str = None):
        """
        Handle error events.
        
        Args:
            error: The error that occurred
            data: Additional error data
        """
        error_msg = f"Error occurred: {str(error)}"
        if data:
            error_msg += f" Data: {data}"
        logger.error(error_msg) 