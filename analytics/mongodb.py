from pymongo import MongoClient
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)

class MongoDBConnection:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        try:
            connection_string = os.getenv('MONGO_CONNECTION_STRING')
            
            if connection_string:
                self._client = MongoClient(
                    connection_string,
                    serverSelectionTimeoutMS=5000
                )
            else:
                mongo_host = os.getenv('MONGO_HOST', 'localhost')
                mongo_port = int(os.getenv('MONGO_PORT', 27017))
                self._client = MongoClient(
                    host=mongo_host,
                    port=mongo_port,
                    serverSelectionTimeoutMS=5000
                )
            
            # Get database
            db_name = os.getenv('MONGO_DB', 'irctc_analytics')
            self._db = self._client[db_name]
            
            # Test connection
            self._client.server_info()
            logger.info(f"MongoDB connected successfully to: {db_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            self._client = None
            self._db = None

    @property
    def db(self):
        return self._db

    @property
    def client(self):
        return self._client

    def is_connected(self):
        return self._client is not None and self._db is not None

# Singleton instance
mongo_connection = MongoDBConnection()