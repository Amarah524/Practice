from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["ExpenseTracker"]
expenses_collection = db["expenses"]
print("MongoDB connected successfully")