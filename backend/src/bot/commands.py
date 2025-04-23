"""Command handlers for the Twitch bot."""
import logging
from typing import Optional, Dict, Any
from datetime import datetime, UTC
from twitchio.ext import commands

from ..database.client import DatabaseClient
from ..database.models import ChannelConfig

logger = logging.getLogger(__name__)

class CommandHandler:
    """Handles bot commands and channel configuration."""
    
    def __init__(self, bot: commands.Bot, db_client: DatabaseClient):
        """
        Initialize the command handler.
        
        Args:
            bot: The TwitchIO bot instance
            db_client: Database client for MongoDB operations
        """
        self.bot = bot
        self.db_client = db_client
    
    async def handle_command(self, ctx: commands.Context) -> None:
        """
        Handle a command from a channel.
        
        Args:
            ctx: The command context
        """
        channel_name = ctx.channel.name
        command_name = ctx.message.content.split()[0].lower()
        
        # Get channel collections
        _, config_collection = self.db_client.get_channel_collections(channel_name)
        
        # Get channel configuration
        config_data = config_collection.find_one({"channel": channel_name})
        if not config_data:
            await ctx.send("Channel configuration not found!")
            return
        
        config = ChannelConfig.from_dict(config_data)
        
        # Handle built-in commands
        if command_name == "!addcommand" and ctx.author.is_mod:
            await self._add_command(ctx, config, config_collection)
        elif command_name == "!delcommand" and ctx.author.is_mod:
            await self._delete_command(ctx, config, config_collection)
        elif command_name == "!commands":
            await self._list_commands(ctx, config)
        elif command_name == "!config" and ctx.author.is_mod:
            await self._show_config(ctx, config)
        elif command_name == "!setretention" and ctx.author.is_mod:
            await self._set_retention(ctx, config, config_collection)
        elif command_name in config.custom_commands:
            await ctx.send(config.custom_commands[command_name])
    
    async def _add_command(self, ctx: commands.Context, config: ChannelConfig, collection) -> None:
        """Add a custom command to the channel."""
        parts = ctx.message.content.split(maxsplit=2)
        if len(parts) != 3:
            await ctx.send("Usage: !addcommand !commandname response")
            return
        
        command_name = parts[1].lower()
        if not command_name.startswith('!'):
            command_name = '!' + command_name
        
        response = parts[2]
        config.custom_commands[command_name] = response
        collection.update_one(
            {"channel": config.channel},
            {"$set": {"custom_commands": config.custom_commands}}
        )
        await ctx.send(f"Added command: {command_name}")
    
    async def _delete_command(self, ctx: commands.Context, config: ChannelConfig, collection) -> None:
        """Delete a custom command from the channel."""
        parts = ctx.message.content.split()
        if len(parts) != 2:
            await ctx.send("Usage: !delcommand !commandname")
            return
        
        command_name = parts[1].lower()
        if not command_name.startswith('!'):
            command_name = '!' + command_name
        
        if command_name in config.custom_commands:
            del config.custom_commands[command_name]
            collection.update_one(
                {"channel": config.channel},
                {"$set": {"custom_commands": config.custom_commands}}
            )
            await ctx.send(f"Deleted command: {command_name}")
        else:
            await ctx.send(f"Command not found: {command_name}")
    
    async def _list_commands(self, ctx: commands.Context, config: ChannelConfig) -> None:
        """List all available commands for the channel."""
        built_in = ["!addcommand", "!delcommand", "!commands", "!config", "!setretention"]
        custom = list(config.custom_commands.keys())
        all_commands = sorted(built_in + custom)
        await ctx.send(f"Available commands: {', '.join(all_commands)}")
    
    async def _show_config(self, ctx: commands.Context, config: ChannelConfig) -> None:
        """Show the current channel configuration."""
        config_info = [
            f"Message retention: {config.message_retention_days} days",
            f"Enabled commands: {', '.join(config.enabled_commands)}",
            f"Custom commands: {len(config.custom_commands)}",
            f"AutoMod settings: {config.auto_mod_settings}"
        ]
        await ctx.send(" | ".join(config_info))
    
    async def _set_retention(self, ctx: commands.Context, config: ChannelConfig, collection) -> None:
        """Set the message retention period for the channel."""
        parts = ctx.message.content.split()
        if len(parts) != 2:
            await ctx.send("Usage: !setretention <days>")
            return
        
        try:
            days = int(parts[1])
            if days < 1 or days > 365:
                await ctx.send("Retention period must be between 1 and 365 days")
                return
            
            config.message_retention_days = days
            collection.update_one(
                {"channel": config.channel},
                {"$set": {"message_retention_days": days}}
            )
            
            # Update TTL index
            messages_collection, _ = self.db_client.get_channel_collections(ctx.channel.name)
            messages_collection.drop_index("timestamp_1")
            messages_collection.create_index("timestamp", expireAfterSeconds=days*24*60*60)
            
            await ctx.send(f"Message retention period set to {days} days")
        except ValueError:
            await ctx.send("Please provide a valid number of days")

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