import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['admin']
collection = db['pspi students']


all_documents = list()
# cursor holds the whole collection.
cursor = collection.find({})

# For each document (i.e each json object in cursor)
# Convert mongoDB ObjectID and ISODate objects to string otherwise error
# Append everything after conversion to 'all_documents' list
for document in cursor:
    document['_id'] = str(document['_id'])
    document['created_at'] = str(document['created_at'])
    all_documents.append(document)




from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return all_documents

api.add_resource(HelloWorld, '/tweets')

if __name__ == '__main__':
    app.run(debug=True)
