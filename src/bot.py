import os
from twitchio.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        # Initialize the bot with your credentials
        super().__init__(
            token=os.getenv('TWITCH_OAUTH_TOKEN'),
            prefix='!',
            initial_channels=[os.getenv('TWITCH_CHANNEL')]
        )

    async def event_ready(self):
        # Called once when the bot goes online
        print(f'Bot is ready! Username: {self.nick}')

    async def event_message(self, message):
        # This will be called every time a message is sent in the chat
        if message.echo:
            return

        print(f'Message from {message.author.name}: {message.content}')

        # Process commands
        await self.handle_commands(message)

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        # A simple command that responds to !hello
        await ctx.send(f'Hello {ctx.author.name}!')

def main():
    bot = Bot()
    bot.run()

if __name__ == '__main__':
    main() 