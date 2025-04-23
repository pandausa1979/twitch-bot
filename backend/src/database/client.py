"""MongoDB client module for managing database connections and operations."""
from typing import Optional, Dict, Tuple, List, Any
import logging
import asyncio
from datetime import datetime, UTC
from pymongo import MongoClient, ASCENDING
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, OperationFailure, DuplicateKeyError
from ..config import MongoConfig
from .models import Channel

logger = logging.getLogger(__name__)

class DatabaseClient:
    """MongoDB client wrapper with connection management and retry logic."""
    
    def __init__(self, config: MongoConfig):
        """Initialize the database client with configuration."""
        self.config = config
        self._client: Optional[MongoClient] = None
        self._channel_dbs: Dict[str, Database] = {}
        self._channels_db: Optional[Database] = None
    
    async def connect(self, max_retries: int = 3, retry_delay: int = 5) -> None:
        """
        Establish connection to MongoDB with retry logic.
        
        Args:
            max_retries: Maximum number of connection attempts
            retry_delay: Delay in seconds between retries
        
        Raises:
            ConnectionFailure: If connection cannot be established after max retries
        """
        for attempt in range(max_retries):
            try:
                self._client = MongoClient(self.config.uri)
                # Test the connection
                self._client.admin.command('ping')
                
                # Initialize channels database
                self._channels_db = self._client['channels']
                channels_collection = self._channels_db['channels']
                
                # Create indexes for channels collection
                if 'name_1' not in channels_collection.index_information():
                    channels_collection.create_index([("name", ASCENDING)], unique=True)
                    logger.info("Created unique index on channel name")
                
                logger.info("Successfully connected to MongoDB")
                return
            except (ConnectionFailure, OperationFailure) as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error("Failed to connect to MongoDB after all retries")
                    raise
    
    def get_channel_collections(self, channel_name: str) -> Tuple[Collection, Collection]:
        """
        Get or create collections for a specific channel.
        
        Args:
            channel_name: Name of the Twitch channel
            
        Returns:
            Tuple of (messages_collection, config_collection)
        """
        # Sanitize channel name for database name (remove special characters)
        db_name = f"twitch_{channel_name.lower().replace('#', '')}"
        
        # Get or create channel database
        if db_name not in self._channel_dbs:
            db = self._client[db_name]
            self._channel_dbs[db_name] = db
            
            # Initialize collections if they don't exist
            messages_collection = db['messages']
            config_collection = db['config']
            
            # Create TTL index for message retention
            if 'timestamp_1' not in messages_collection.index_information():
                messages_collection.create_index("timestamp", expireAfterSeconds=30*24*60*60)
                logger.info(f"Created TTL index for messages in channel: {channel_name}")
            
            # Create unique index on channel field in config collection
            if 'channel_1' not in config_collection.index_information():
                config_collection.create_index("channel", unique=True)
                logger.info(f"Created unique index for config in channel: {channel_name}")
            
            logger.info(f"Initialized database for channel: {channel_name}")
        else:
            db = self._channel_dbs[db_name]
            messages_collection = db['messages']
            config_collection = db['config']
        
        return messages_collection, config_collection
    
    async def add_channel(self, channel: Channel) -> bool:
        """
        Add a new channel to the channels collection.
        
        Args:
            channel: Channel object to add
            
        Returns:
            bool: True if successful, False if channel already exists
        """
        try:
            channel.joined_at = datetime.now(UTC)
            channel.last_active = datetime.now(UTC)
            self._channels_db.channels.insert_one(channel.to_dict())
            logger.info(f"Added new channel: {channel.name}")
            return True
        except DuplicateKeyError:
            logger.warning(f"Channel already exists: {channel.name}")
            return False
    
    async def get_all_channels(self) -> List[Channel]:
        """
        Get all channels from the channels collection.
        
        Returns:
            List[Channel]: List of all channels
        """
        channels = []
        for doc in self._channels_db.channels.find({"is_active": True}):
            channels.append(Channel.from_dict(doc))
        return channels
    
    async def update_channel_activity(self, channel_name: str) -> None:
        """
        Update the last_active timestamp for a channel.
        
        Args:
            channel_name: Name of the channel to update
        """
        self._channels_db.channels.update_one(
            {"name": channel_name},
            {"$set": {"last_active": datetime.now(UTC)}}
        )
    
    async def deactivate_channel(self, channel_name: str) -> None:
        """
        Mark a channel as inactive.
        
        Args:
            channel_name: Name of the channel to deactivate
        """
        self._channels_db.channels.update_one(
            {"name": channel_name},
            {"$set": {"is_active": False}}
        )
        logger.info(f"Deactivated channel: {channel_name}")
    
    def close(self) -> None:
        """Close the database connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._channel_dbs.clear()
            self._channels_db = None
            logger.info("Closed MongoDB connection")
    
    @property
    def client(self) -> Optional[MongoClient]:
        """Get the MongoDB client instance."""
        return self._client 

    async def get_channel(self, name: str) -> Optional[Channel]:
        """
        Get a channel from the database.
        
        Args:
            name: The channel name
            
        Returns:
            Optional[Channel]: The channel if found, None otherwise
        """
        channel_data = self._channels_db.channels.find_one({"name": name})
        if channel_data:
            return Channel.from_dict(channel_data)
        return None
        
    async def update_channel_activity(self, name: str, timestamp: datetime) -> bool:
        """
        Update a channel's last activity timestamp.
        
        Args:
            name: The channel name
            timestamp: The activity timestamp
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            result = self._channels_db.channels.update_one(
                {"name": name},
                {"$set": {"last_activity": timestamp}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating channel activity for {name}: {str(e)}")
            return False
            
    async def get_active_channels(self, since: datetime) -> List[Channel]:
        """
        Get all channels active since the given timestamp.
        
        Args:
            since: The timestamp to check activity against
            
        Returns:
            List[Channel]: List of active channels
        """
        channels = []
        cursor = self._channels_db.channels.find({"last_activity": {"$gte": since}})
        for channel_data in cursor:
            channels.append(Channel.from_dict(channel_data))
        return channels
        
    async def remove_channel(self, name: str) -> bool:
        """
        Remove a channel from the database.
        
        Args:
            name: The channel name
            
        Returns:
            bool: True if removed successfully, False otherwise
        """
        try:
            result = self._channels_db.channels.delete_one({"name": name})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error removing channel {name}: {str(e)}")
            return False 