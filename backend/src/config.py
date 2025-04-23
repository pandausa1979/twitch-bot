"""Configuration management for the Twitch bot application."""
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

@dataclass
class MongoConfig:
    """MongoDB configuration settings."""
    user: str
    password: str
    host: str
    port: str
    database: str = 'twitch'
    auth_source: str = 'admin'
    
    @property
    def uri(self) -> str:
        """Generate MongoDB connection URI."""
        from urllib.parse import quote_plus
        return (
            f"mongodb://{quote_plus(self.user)}:{quote_plus(self.password)}"
            f"@{self.host}:{self.port}/{self.auth_source}?retryWrites=true&w=majority"
        )

@dataclass
class BotConfig:
    """Twitch bot configuration settings."""
    tmi_token: str
    prefix: str = '!'
    initial_channels: list[str] = None
    
    def __post_init__(self):
        if self.initial_channels is None:
            self.initial_channels = []

@dataclass
class LogConfig:
    """Logging configuration settings."""
    level: str = 'DEBUG'
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_dir: str = 'logs'
    log_file: str = 'bot.log'
    
    @property
    def log_path(self) -> str:
        """Get the full path to the log file."""
        return os.path.join(self.log_dir, self.log_file)

@dataclass
class AppConfig:
    """Application configuration settings."""
    mongo: MongoConfig
    bot: BotConfig
    log: LogConfig
    health_port: int = 8080
    health_host: str = '0.0.0.0'

def load_config() -> AppConfig:
    """Load configuration from environment variables."""
    load_dotenv()
    
    # MongoDB configuration
    mongo_config = MongoConfig(
        user=os.getenv('MONGODB_USER', 'TwitchBot'),
        password=os.getenv('MONGODB_PASSWORD', 'TwitchBotSecurePass123'),
        host=os.getenv('MONGODB_HOST', 'localhost'),
        port=os.getenv('MONGODB_PORT', '30017')
    )
    
    # Bot configuration
    bot_config = BotConfig(
        tmi_token=os.getenv('TWITCH_TMI_TOKEN'),
    )
    
    # Logging configuration
    log_config = LogConfig(
        level=os.getenv('LOG_LEVEL', 'DEBUG'),
        log_dir=os.getenv('LOG_DIR', 'logs'),
        log_file=os.getenv('LOG_FILE', 'bot.log')
    )
    
    return AppConfig(
        mongo=mongo_config,
        bot=bot_config,
        log=log_config,
        health_port=int(os.getenv('HEALTH_PORT', '8080')),
        health_host=os.getenv('HEALTH_HOST', '0.0.0.0')
    ) 