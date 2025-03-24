from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
from datetime import datetime
from src.config.settings import settings
from src.utils.logging import logger
import time

class MongoDBClient:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        for attempt in range(settings.MAX_RETRIES):
            try:
                self.client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=30000)
                self.db = self.client["emailagent"]
                self.collection = self.db["responses"]
                self.db.command("ping")
                logger.info("Connected to MongoDB Atlas successfully")
                break
            except ConnectionFailure as e:
                logger.error(f"Attempt {attempt + 1}/{settings.MAX_RETRIES} failed: {str(e)}")
                if attempt < settings.MAX_RETRIES - 1:
                    time.sleep(settings.RETRY_DELAY)
                else:
                    logger.error("Failed to connect to MongoDB Atlas after retries.")
                    raise

    def insert_response(self, data: dict) -> str:
        data["timestamp"] = datetime.utcnow()
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update_response(self, response_id: str, update_data: dict) -> None:
        self.collection.update_one({"_id": ObjectId(response_id)}, {"$set": update_data})

    def find_response(self, response_id: str) -> dict:
        response = self.collection.find_one({"_id": ObjectId(response_id)})
        if response:
            response["_id"] = str(response["_id"])
        return response

mongo_db = MongoDBClient()