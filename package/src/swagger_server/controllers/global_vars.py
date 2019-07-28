from pymongo import MongoClient

CLIENT = MongoClient('mongodb://mongodb:27017/')
DB = CLIENT.database
MDBC = DB.student_db