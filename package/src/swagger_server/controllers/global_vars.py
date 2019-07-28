from pymongo import MongoClient

MC = MongoClient('mongodb', 27017)
MDB = MC.data
MDBC = MDB.student_data