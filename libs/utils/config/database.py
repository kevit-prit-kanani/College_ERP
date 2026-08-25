from pymongo import MongoClient

from libs.utils.config import MONGODB_URL

client = MongoClient(MONGODB_URL)

db = client.todo_db

db_Students = db["Students"]
db_Staff = db["Staff"]
db_Attendance = db["Attendance"]
db_Batches = db["Batches"]
db_Department = db["Department"]
db_User_wise_Department = db['User_wise_Department']