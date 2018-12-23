import pymongo
from flask import Flask, request
import json

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
from flask import render_template
from flask_restful import Resource, Api
from flask_restful import abort

app = Flask(__name__)
api = Api(app)

class getTweets(Resource):
    def get(self):

        args = request.args
        #print(args)
        #if parameter isn't morethan
        for arg in args:
            if(arg!='morethan'):
                #return json text "Bad request"
                return abort(400)
            else:
                #if value int
                try:
                    int(args[arg])
                #if value not int
                except ValueError:
                    abort(400)


        x = request.args.get('morethan', default=-1, type=int)
        #if no parameters (i.e x=-1 by default) then return all tweets(documents)
        if(x == -1):
            parsed = json.dumps(all_documents)
            if isinstance(parsed, str):
                print("STR")

            return parsed

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


class ByHashtag(Resource):
    def get(self,hashtag):
        print(hashtag)
        #for each document if hashtag passed via URL is in it then add it to the list
        have_hashtag = list()

        cursor = collection.find({})

        for document in cursor:

            document['_id'] = str(document['_id'])
            document['created_at'] = str(document['created_at'])
            document_hashtags = document['entities']['hashtags']

            # Append all documents to the list that include this hashtag.
            for included_hashtag in document_hashtags:
                if (included_hashtag['text']==hashtag):
                    have_hashtag.append(document)

        return have_hashtag

    def delete(self, hashtag):
        hashtagToDelete = hashtag
        cursor = collection.find({})
        #number of deleted tweets
        n_of_deleted = 0
        print(hashtagToDelete)


        #hashtags = document['entities']['hashtags' : {"$all":[hashtagToDelete]}]
        #query =
        #n_of_deleted = collection.find( { "entities":{"hashtags":{"text":hashtagToDelete}}})
        #n_of_deleted = collection.find( { "entities":{"hashtags":{ "$elemMatch": {"text":hashtagToDelete}}}})
        #docsToDelete = [doc for doc in n_of_deleted]
        cursor = collection.find({})
        #ids = list()

        for doc in cursor:
            hashtags = doc['entities']['hashtags']
            for each in hashtags:
                if each ['text'] == hashtagToDelete:
                    n_of_deleted+=1
                    doc_id = doc['id']
                    #ids.append(doc_id)
                    collection.remove({'id':doc_id})

        return {'removedCount':n_of_deleted}





api.add_resource(getTweets, '/tweets')
api.add_resource(ByHashtag, '/tweets/hashtag/<string:hashtag>')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5110)




