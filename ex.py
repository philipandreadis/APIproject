import pymongo
from flask import Flask

client = pymongo.MongoClient('localhost', 27017)
db = client['tweets']
