import os
from twitchio.ext import commands
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

class ChatReader(commands.Bot):
    def __init__(self):
        # Get credentials from environment variables
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        if not token:
            raise ValueError("TWITCH_OAUTH_TOKEN not found in environment variables")
        
        channel = os.getenv('TWITCH_CHANNEL')
        if not channel:
            raise ValueError("TWITCH_CHANNEL not found in environment variables")

        # Initialize the bot with your credentials
        super().__init__(
            token=token,
            prefix='!',
            initial_channels=[channel]
        )

    async def event_ready(self):
        # Called once when the bot goes online
        print(f'Bot is ready! Username: {self.nick}')
        print(f'Connected to channel: {os.getenv("TWITCH_CHANNEL")}')

    async def event_message(self, message):
        # This will be called every time a message is sent in the chat
        if message.echo:
            return

        # Print message details
        print(f'[{message.channel.name}] {message.author.name}: {message.content}')

        # Check if message is a command
        if message.content.startswith('!'):
            await self.handle_commands(message)

    @commands.command(name='ping')
    async def ping_command(self, ctx):
        # A simple command that responds to !ping
        await ctx.send(f'Pong! {ctx.author.name}')

    @commands.command(name='uptime')
    async def uptime_command(self, ctx):
        # Example of a command that could check stream uptime
        await ctx.send(f'Uptime command received from {ctx.author.name}')

async def main():
    try:
        # Create and run the bot
        bot = ChatReader()
        await bot.start()
    except Exception as e:
        print(f"Error starting bot: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a Twitch Developer Application at https://dev.twitch.tv/console")
        print("2. Generated an OAuth token with chat:read and chat:edit scopes")
        print("3. Set up your .env file with the correct credentials")

if __name__ == '__main__':
    asyncio.run(main()) 