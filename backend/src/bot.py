import os
import logging
import argparse
import asyncio
from dotenv import load_dotenv
from twitchio.ext import commands
from pymongo import MongoClient
from datetime import datetime, UTC
from urllib.parse import quote_plus
from aiohttp import web
from health import setup_health_routes

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        # Initialize MongoDB connection
        try:
            mongo_user = os.getenv('MONGODB_USER', 'TwitchBot')
            mongo_password = os.getenv('MONGODB_PASSWORD', 'TwitchBotSecurePass123')
            mongo_host = os.getenv('MONGODB_HOST', 'localhost')
            mongo_port = os.getenv('MONGODB_PORT', '27017')
            
            if not mongo_password:
                logger.error("MONGODB_PASSWORD environment variable not set")
                raise ValueError("MongoDB password not configured")
                
            mongo_uri = f"mongodb://{mongo_user}:{quote_plus(mongo_password)}@{mongo_host}:{mongo_port}/twitch_bot?authSource=admin&retryWrites=true&w=majority"
            self.mongo_client = MongoClient(mongo_uri)
            
            # Test the connection
            self.mongo_client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            
            self.db = self.mongo_client['twitch_bot']
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

        # Get channels from environment variable
        channels_str = os.getenv('TWITCH_CHANNELS', '')
        if not channels_str:
            logger.error("TWITCH_CHANNELS environment variable not set")
            raise ValueError("No channels configured")
            
        # Split channels string into list and remove any whitespace
        channels = [ch.strip() for ch in channels_str.split(',')]
        logger.info(f"Connecting to channels: {channels}")
        
        # Initialize the bot with token and prefix
        super().__init__(
            token=os.getenv('TWITCH_TOKEN'),
            prefix='!',
            initial_channels=channels
        )

    def get_channel_collection(self, channel_name):
        """Get or create a collection for a specific channel"""
        collection_name = f"messages_{channel_name}"
        if collection_name not in self.db.list_collection_names():
            # Create collection with TTL index for message retention (30 days)
            collection = self.db[collection_name]
            collection.create_index("timestamp", expireAfterSeconds=30*24*60*60)
            logger.info(f"Created new collection for channel: {channel_name}")
        return self.db[collection_name]

    async def event_ready(self):
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f'Bot is ready! Username: {self.nick}')
                logger.info(f'Connected to channels: {", ".join(self._connection.joining_channels)}')

                # Start health server after bot is ready
                app = web.Application()
                setup_health_routes(app, self.mongo_client)
                runner = web.AppRunner(app)
                await runner.setup()
                site = web.TCPSite(runner, '0.0.0.0', 8080)
                await site.start()
                logger.info("Health check server started on port 8080")
                return
            except Exception as e:
                logger.error(f'Error in event_ready: {str(e)}')
                retry_count += 1
                if retry_count < max_retries:
                    logger.info(f'Retrying in 5 seconds... (Attempt {retry_count + 1}/{max_retries})')
                    await asyncio.sleep(5)
        
        logger.error(f'Failed to initialize after {max_retries} attempts')
        raise ConnectionError('Failed to initialize bot')

    async def event_error(self, error):
        logger.error(f'Bot encountered an error: {str(error)}')
        # Add any additional error handling logic here

    async def event_disconnect(self):
        logger.warning('Bot disconnected from Twitch')
        # Add reconnection logic here if needed

    async def event_message(self, message):
        # Ignore messages from the bot itself
        if message.echo:
            return

        logger.debug(f"Received message: {message.content} from {message.author.name}")
        
        # Get channel-specific collection and log the message
        collection = self.get_channel_collection(message.channel.name)
        collection.insert_one({
            'channel': message.channel.name,
            'user': message.author.name,
            'message': message.content,
            'timestamp': datetime.now(UTC)
        })

        # Process commands
        await self.handle_commands(message)

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        logger.debug(f"Hello command triggered by {ctx.author.name}")
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command(name='ping')
    async def ping_command(self, ctx):
        logger.debug(f"Ping command triggered by {ctx.author.name}")
        await ctx.send('Pong!')

def main():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        logger.info("Created logs directory")

    # Start the bot
    bot = Bot()
    bot.run()

if __name__ == '__main__':
    main() 