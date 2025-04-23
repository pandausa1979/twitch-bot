"""Main bot module that integrates all components."""
import logging
import os
from typing import Optional, List
from twitchio.ext import commands

from ..config import AppConfig, load_config
from ..database.client import DatabaseClient
from .events import EventHandler
from .commands import hello_command, ping_command

logger = logging.getLogger(__name__)

class TwitchBot(commands.Bot):
    """Main Twitch bot class that integrates all components."""
    
    def __init__(self, channel: str):
        """
        Initialize the Twitch bot.
        
        Args:
            channel: The Twitch channel to join
        """
        # Load configuration
        self.config = load_config()
        
        # Initialize database client
        self.db_client = DatabaseClient(self.config.mongo)
        
        # Initialize the bot with token and prefix
        if channel.startswith('#'):
            channel = channel[1:]  # Remove the # if present
            
        super().__init__(
            token=self.config.bot.tmi_token,
            prefix=self.config.bot.prefix,
            initial_channels=[channel]
        )
        
        # Initialize event handler
        self.event_handler = EventHandler(self, self.db_client)
        
        # Register commands
        self.add_command(hello_command)
        self.add_command(ping_command)
        
        logger.info(f"Bot initialized for channel: {channel}")
    
    async def event_ready(self):
        """Handle the ready event."""
        await self.event_handler.on_ready()
    
    async def event_message(self, message):
        """Handle incoming messages."""
        await self.event_handler.on_message(message)
        # Process commands after handling the message
        await self.handle_commands(message)
    
    async def event_error(self, error: Exception):
        """Handle errors."""
        await self.event_handler.on_error(error)
    
    async def event_disconnect(self):
        """Handle disconnection."""
        await self.event_handler.on_disconnect()
    
    def run(self):
        """Run the bot with proper setup and cleanup."""
        try:
            # Ensure logs directory exists
            os.makedirs(self.config.log.log_dir, exist_ok=True)
            
            # Configure logging
            logging.basicConfig(
                level=getattr(logging, self.config.log.level),
                format=self.config.log.format,
                handlers=[
                    logging.FileHandler(self.config.log.log_path),
                    logging.StreamHandler()
                ]
            )
            
            # Connect to database
            self.db_client.connect()
            
            # Start the bot
            super().run()
        except Exception as e:
            logger.error(f"Failed to start bot: {str(e)}")
            raise
        finally:
            # Cleanup
            self.db_client.close() 