"""Event handlers for the Twitch bot."""
import logging
import asyncio
from datetime import datetime, UTC
from typing import Optional
from aiohttp import web
from twitchio.ext import commands

from ..database.client import DatabaseClient
from ..database.models import ChatMessage
from ..health import setup_health_routes

logger = logging.getLogger(__name__)

class EventHandler:
    """Handles Twitch bot events."""
    
    def __init__(self, bot: commands.Bot, db_client: DatabaseClient):
        """
        Initialize the event handler.
        
        Args:
            bot: The TwitchIO bot instance
            db_client: Database client for MongoDB operations
        """
        self.bot = bot
        self.db_client = db_client
        self._health_runner: Optional[web.AppRunner] = None
    
    async def on_ready(self):
        """Handle the ready event when the bot connects to Twitch."""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f'Bot is ready! Username: {self.bot.nick}')
                channel = self.bot.get_channel(self.bot.initial_channels[0])
                
                if channel:
                    await channel.send("Bot is now online!")
                    logger.info(f'Connected to channel: {channel.name}')
                    await self._start_health_server()
                    return
                else:
                    logger.error(f'Could not find channel: {self.bot.initial_channels[0]}')
                    retry_count += 1
                    if retry_count < max_retries:
                        logger.info(f'Retrying in 5 seconds... (Attempt {retry_count + 1}/{max_retries})')
                        await asyncio.sleep(5)
            except Exception as e:
                logger.error(f'Error in event_ready: {str(e)}')
                retry_count += 1
                if retry_count < max_retries:
                    logger.info(f'Retrying in 5 seconds... (Attempt {retry_count + 1}/{max_retries})')
                    await asyncio.sleep(5)
        
        logger.error(f'Failed to connect to channel after {max_retries} attempts')
        raise ConnectionError(f'Could not connect to channel {self.bot.initial_channels[0]}')
    
    async def on_message(self, message):
        """
        Handle incoming chat messages.
        
        Args:
            message: The incoming chat message
        """
        # Ignore messages from the bot itself
        if message.echo:
            return

        logger.debug(f"Received message: {message.content} from {message.author.name}")
        
        # Create and store chat message
        chat_message = ChatMessage(
            channel=message.channel.name,
            user=message.author.name,
            message=message.content,
            timestamp=datetime.now(UTC),
            user_id=str(message.author.id) if message.author.id else None,
            is_mod=message.author.is_mod,
            is_subscriber=message.author.is_subscriber
        )
        
        collection = self.db_client.get_channel_collection(message.channel.name)
        collection.insert_one(chat_message.to_dict())
    
    async def on_error(self, error: Exception):
        """
        Handle bot errors.
        
        Args:
            error: The error that occurred
        """
        logger.error(f'Bot encountered an error: {str(error)}')
    
    async def on_disconnect(self):
        """Handle bot disconnection."""
        logger.warning('Bot disconnected from Twitch')
        if self._health_runner:
            await self._health_runner.cleanup()
            self._health_runner = None
    
    async def _start_health_server(self):
        """Start the health check server."""
        try:
            app = web.Application()
            setup_health_routes(app, self.db_client.client)
            self._health_runner = web.AppRunner(app)
            await self._health_runner.setup()
            site = web.TCPSite(self._health_runner, '0.0.0.0', 8080)
            await site.start()
            logger.info("Health check server started on port 8080")
        except Exception as e:
            logger.error(f"Failed to start health server: {str(e)}")
            raise 