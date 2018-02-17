from pymongo import MongoClient
from flask import Flask, request, render_template
import yummly

app = Flask(__name__)

MONGODB_URI = "mongodb://platters_hacks:platters@ds227168.mlab.com:27168/platters_hacks"
client = MongoClient(MONGODB_URI)
db = client.get_database('platters_hacks')

@app.route('/', methods=["POST", "GET"])
def my_form():
    if request.method == "GET":
        return render_template('user_info.html')
    else:
        diet = request.form.getlist('diet')
        allergy = request.form.getlist('health')
        likes = request.form['users_likes'].split(',')
        dislikes = request.form['users_dislikes'].split(',')
        recipes = yummly.search_recipes(likes, dislikes, diet, allergy, [''], [20])
        
        answer = ''
        for recipe in recipes:
            answer = answer + recipe.name + '\r\n'
        return answer


if __name__ == '__main__':
    app.run()
