from pymongo import MongoClient
from flask import Flask, request, render_template


app = Flask(__name__)

MONGODB_URI = "mongodb://platters_hacks:platters@ds227168.mlab.com:27168/platters_hacks"
client = MongoClient(MONGODB_URI)
db = client.get_database('platters_hacks')


@app.route('/', methods=["POST", "GET"])
def my_form():
    if request.method == "GET":
        return render_template('user_info.html')
    else:
        info = request.form['user_height']
        return str(info)

if __name__ == '__main__':
    app.run()
