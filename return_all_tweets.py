import pymongo
from flask import Flask, request

client = pymongo.MongoClient('localhost', 27017)
db = client['tweets']
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

class all_tweets(Resource):
    def get(self):
        x = request.args.get('morethan', default=-1, type=int)
        #if no parameters (i.e x=-1 by default) then return all tweets(documents)
        if(x == -1):
            return all_documents

        #if x != -1 return all tweets where num_of_hashtags > x
        else:
            # List of all tweets with more than x hashtags
            more_than_x_tweets = list()
            cursor = collection.find({})
            #for each json object in the collection convert Mongo objects to string
            # and access 'hashtags' list to get its length
            for document in cursor:

                document['_id'] = str(document['_id'])
                document['created_at'] = str(document['created_at'])
                num_of_hashtags = len(document['entities']['hashtags'])

                #Append all documents that hashtags > x to the list.
                if(num_of_hashtags > x):
                    more_than_x_tweets.append(document)

            return more_than_x_tweets



api.add_resource(all_tweets, '/tweets')
#api.add_resource(more_than_tweets, '/tweets')

if __name__ == '__main__':
    app.run(debug=True)
