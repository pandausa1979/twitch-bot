"""Main bot module that integrates all components."""
import logging
import os
from typing import List, Optional
from datetime import datetime, UTC
from twitchio.ext import commands
import asyncio

from ..config import AppConfig, load_config, MongoConfig
from ..database.client import DatabaseClient
from ..database.models import Channel
from .events import EventHandler
from .commands import CommandHandler

logger = logging.getLogger(__name__)

class TwitchBot(commands.Bot):
    """Main Twitch bot class."""
    
    def __init__(self, channels: List[str]):
        """
        Initialize the Twitch bot.
        
        Args:
            channels: List of channel names to join
        """
        # Get configuration from environment
        token = os.getenv('TWITCH_TOKEN')
        client_id = os.getenv('TWITCH_CLIENT_ID')
        
        if not token or not client_id:
            raise ValueError("Missing required environment variables: TWITCH_TOKEN, TWITCH_CLIENT_ID")
        
        # Initialize the bot
        super().__init__(
            token=token,
            client_id=client_id,
            nick="TwitchBot",
            prefix="!",
            initial_channels=channels
        )
        
        # Initialize database client
        mongo_config = MongoConfig(
            host=os.getenv('MONGO_HOST', 'localhost'),
            port=int(os.getenv('MONGO_PORT', '27017')),
            username=os.getenv('MONGO_USER', 'twitch_bot_app'),
            password=os.getenv('MONGO_PASSWORD', '')
        )
        self.db_client = DatabaseClient(mongo_config)
        
        # Initialize handlers
        self.event_handler = EventHandler(self, self.db_client)
        self.command_handler = CommandHandler(self, self.db_client)
        
        # Register event handlers
        self.register_events()
    
    async def setup_channels(self):
        """Set up channels in the database."""
        for channel_name in self.initial_channels:
            # Create channel object
            channel = Channel(
                name=channel_name.lower(),
                display_name=channel_name,
                is_active=True,
                joined_at=datetime.now(UTC),
                last_active=datetime.now(UTC)
            )
            
            # Add to database if not exists
            await self.db_client.add_channel(channel)
    
    def register_events(self):
        """Register event handlers."""
        self.event_ready = self.event_handler.on_ready
        self.event_message = self.event_handler.on_message
        self.event_error = self.event_handler.on_error
        self.event_command_error = self.event_handler.on_error
    
    async def event_command(self, ctx: commands.Context):
        """
        Handle command events.
        
        Args:
            ctx: The command context
        """
        await self.command_handler.handle_command(ctx)
    
    async def close(self):
        """Clean up resources when shutting down."""
        self.db_client.close()
        await super().close()
    
    def run(self):
        """Run the bot with proper setup and cleanup."""
        try:
            # Configure logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # Connect to database and set up channels
            self.db_client.connect()
            asyncio.run(self.setup_channels())
            
            # Start the bot
            super().run()
        except Exception as e:
            logger.error(f"Failed to start bot: {str(e)}")
            raise
        finally:
            # Cleanup
            self.db_client.close() 