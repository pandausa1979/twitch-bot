"""Main entry point for the Twitch bot application."""
import os
import sys
import logging
from typing import List
from dotenv import load_dotenv

from .bot import TwitchBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_channels() -> List[str]:
    """
    Load channel names from environment variables.
    
    Returns:
        List[str]: List of channel names to monitor
    """
    channels_str = os.getenv('TWITCH_CHANNELS')
    if not channels_str:
        logger.error("No channels specified in TWITCH_CHANNELS environment variable")
        sys.exit(1)
    
    # Split channels by comma and clean up
    channels = [
        channel.strip().lower()
        for channel in channels_str.split(',')
        if channel.strip()
    ]
    
    if not channels:
        logger.error("No valid channels found in TWITCH_CHANNELS")
        sys.exit(1)
    
    return channels

def main():
    """Main entry point for the application."""
    # Load environment variables
    load_dotenv()
    
    try:
        # Get channels to monitor
        channels = load_channels()
        logger.info(f"Starting bot for channels: {', '.join(channels)}")
        
        # Start the bot
        bot = TwitchBot(channels)
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 