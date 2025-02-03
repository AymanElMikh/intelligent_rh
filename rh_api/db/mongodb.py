import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv



load_dotenv()  

class DBConnection:
    def __init__(self):
        """Initialize MongoDB connection with a remote MongoDB Compass (Atlas) database."""
        self.db_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DATABASE_NAME", "rhAPI")

        if not self.db_uri:
            raise ValueError("⚠️ MONGO_URI environment variable is missing!")

        try:
            self.client = MongoClient(self.db_uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command("ping")
            print("✅ Successfully connected to MongoDB Atlas!")
        except ConnectionFailure:
            raise ConnectionFailure("❌ Could not connect to MongoDB Compass Cloud. Check your MONGO_URI!")

        self.db = self.client[self.db_name]

    def get_collection(self, collection_name):
        """Retrieve a specific collection instance."""
        if not collection_name:
            raise ValueError("⚠️ Collection name must be provided!")
        return self.db[collection_name]

    def get_company_info(self):
        """Retrieve the company information document."""
        collection = self.db[self.company_collection_name]
        return collection.find_one()

    def get_employee(self, employee_id):
        """Retrieve an employee by ID."""
        collection = self.db[self.employee_collection_name]
        return collection.find_one({"employee_id": employee_id})
