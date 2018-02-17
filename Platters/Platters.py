from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

MONGODB_URI = "mongodb://platters_hacks:platters@ds227168.mlab.com:27168/platters_hacks"
client = MongoClient(MONGODB_URI)
db = client.get_database('platters_hacks')



@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
