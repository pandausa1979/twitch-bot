"""Main entry point for the Twitch bot application."""
import argparse
import logging
from bot import TwitchBot

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the application."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Twitch Bot')
    parser.add_argument('--channel', required=True, help='Twitch channel to monitor')
    args = parser.parse_args()
    
    try:
        # Start the bot
        bot = TwitchBot(args.channel)
        bot.run()
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        raise

if __name__ == '__main__':
    main() 