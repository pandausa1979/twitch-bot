import os
from datetime import datetime
from dotenv import load_dotenv
from twitchio.ext import commands
from pymongo import MongoClient
from auth import TwitchAuth

# Load environment variables
load_dotenv()

# MongoDB setup
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('DB_NAME', 'twitch_chat_db')]
collection = db[os.getenv('COLLECTION_NAME', 'messages')]

class Bot(commands.Bot):
    def __init__(self):
        # Initialize auth
        auth = TwitchAuth()
        token = auth.get_token()

        # Initialize bot with OAuth token
        super().__init__(
            token=token,
            client_id=os.getenv('CLIENT_ID'),
            nick=os.getenv('BOT_NICK'),
            prefix='!',
            initial_channels=[os.getenv('CHANNEL')]
        )
        
        self.auth = auth

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'Connected to channel | {os.getenv("CHANNEL")}')

    async def event_message(self, message):
        # Ignore messages from the bot itself
        if message.echo:
            return

        # Create message document
        chat_message = {
            'channel': message.channel.name,
            'author': message.author.name,
            'content': message.content,
            'timestamp': datetime.utcnow(),
            'badges': [badge for badge in message.author.badges] if message.author.badges else [],
            'is_subscriber': message.author.is_subscriber,
            'is_mod': message.author.is_mod
        }

        # Store message in MongoDB
        try:
            collection.insert_one(chat_message)
            print(f'Stored message from {message.author.name}')
        except Exception as e:
            print(f'Error storing message: {e}')

        # Handle commands
        await self.handle_commands(message)

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

if __name__ == '__main__':
    bot = Bot()
    bot.run() 