# Twitch Chat Bot

A simple Twitch chat bot built with Python and TwitchIO.

## Setup

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your Twitch credentials:
   ```
   TWITCH_BOT_USERNAME=your_bot_username
   TWITCH_OAUTH_TOKEN=oauth:your_oauth_token
   TWITCH_CHANNEL=channel_to_join
   ```

## Getting Twitch OAuth Token

1. Go to https://twitchapps.com/tmi/
2. Click "Connect with Twitch"
3. Authorize the application
4. Copy the OAuth token (it will start with "oauth:")

## Running the Bot

```bash
python src/bot.py
```

## Features

- Connects to Twitch chat
- Responds to !hello command
- Logs all chat messages to console

## Adding New Commands

To add new commands, add new methods to the Bot class with the @commands.command decorator:

```python
@commands.command(name='command_name')
async def command_method(self, ctx):
    await ctx.send('Response message')
``` # twitchboy
