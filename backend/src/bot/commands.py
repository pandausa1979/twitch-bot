"""Command handlers for the Twitch bot."""
import logging
from typing import Callable, Dict
from twitchio.ext import commands

logger = logging.getLogger(__name__)

class CommandHandler:
    """Handles command registration and execution for the bot."""
    
    def __init__(self):
        """Initialize the command handler."""
        self.commands: Dict[str, Callable] = {}
    
    def command(self, name: str):
        """
        Decorator for registering commands.
        
        Args:
            name: Name of the command (without prefix)
        """
        def decorator(func: Callable):
            self.commands[name] = func
            return func
        return decorator

@commands.command(name='hello')
async def hello_command(ctx):
    """Respond to the !hello command."""
    logger.debug(f"Hello command triggered by {ctx.author.name}")
    await ctx.send(f'Hello {ctx.author.name}!')

@commands.command(name='ping')
async def ping_command(ctx):
    """Respond to the !ping command."""
    logger.debug(f"Ping command triggered by {ctx.author.name}")
    await ctx.send('Pong!') 