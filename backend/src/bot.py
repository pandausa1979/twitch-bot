import os
import logging
from dotenv import load_dotenv
from twitchio.ext import commands
from pymongo import MongoClient
from datetime import datetime, UTC
from urllib.parse import quote_plus

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
        password = quote_plus('/8vqZjEBJv9v8DZvpuHASAdyOllng7gV39rE0eKkuvc=')  # Root password from MongoDB pod
        mongo_uri = f"mongodb://TwitchBot:{password}@localhost:32458/admin"
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client['twitch']  # Use twitch database after authenticating with admin
        self.messages = self.db['messages']
        
        # Initialize the bot with token and prefix
        channel = os.getenv('TWITCH_CHANNEL')
        if channel.startswith('#'):
            channel = channel[1:]  # Remove the # if present
        super().__init__(
            token=os.getenv('TWITCH_TMI_TOKEN'),
            prefix='!',
            initial_channels=[channel]
        )
        logger.info("Bot initialized with MongoDB connection")

    async def event_ready(self):
        logger.info(f'Bot is ready! Username: {self.nick}')
        channel = self.get_channel(os.getenv('TWITCH_CHANNEL').lstrip('#'))
        if channel:
            await channel.send("Bot is now online!")
            logger.info(f'Connected to channel: {channel.name}')
        else:
            logger.error(f'Could not find channel: {os.getenv("TWITCH_CHANNEL")}')

    async def event_message(self, message):
        # Ignore messages from the bot itself
        if message.echo:
            return

        logger.debug(f"Received message: {message.content} from {message.author.name}")
        
        # Log the message to MongoDB
        self.messages.insert_one({
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

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        logger.info("Created logs directory")

    # Start the bot
    bot = Bot()
    bot.run() 