"""MongoDB client module for managing database connections and operations."""
from typing import Optional
import logging
import asyncio
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from ..config import MongoConfig

logger = logging.getLogger(__name__)

class DatabaseClient:
    """MongoDB client wrapper with connection management and retry logic."""
    
    def __init__(self, config: MongoConfig):
        """Initialize the database client with configuration."""
        self.config = config
        self._client: Optional[MongoClient] = None
        self._db = None
    
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
                self._db = self._client[self.config.database]
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
    
    def get_channel_collection(self, channel_name: str):
        """
        Get or create a collection for a specific channel.
        
        Args:
            channel_name: Name of the Twitch channel
            
        Returns:
            Collection object for the specified channel
        """
        collection_name = f"messages_{channel_name}"
        if collection_name not in self._db.list_collection_names():
            collection = self._db[collection_name]
            # Create TTL index for message retention (30 days)
            collection.create_index("timestamp", expireAfterSeconds=30*24*60*60)
            logger.info(f"Created new collection for channel: {channel_name}")
            return collection
        return self._db[collection_name]
    
    def close(self) -> None:
        """Close the database connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("Closed MongoDB connection")
    
    @property
    def client(self) -> Optional[MongoClient]:
        """Get the MongoDB client instance."""
        return self._client
    
    @property
    def db(self):
        """Get the database instance."""
        return self._db 