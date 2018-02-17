from pymongo import MongoClient
from flask import Flask, request, render_template
import yummly, heapq

app = Flask(__name__)

MONGODB_URI = "mongodb://platters_hacks:platters@ds227168.mlab.com:27168/platters_hacks"
client = MongoClient(MONGODB_URI)
db = client.get_database('platters_hacks')

BREAKFAST_COURSE = ['course^course-Breakfast and Brunch', 'course^course-Breads']
LUNCH_COURSE = ['course^course-Main Dishes', 'course^course-Appetizers', 'course^course-Salads','course^course-Lunch']
DINNER_COURSE = ['course^course-Main Dishes', 'course^course-Soups']

@app.route('/', methods=["POST", "GET"])
def my_form():
    if request.method == "GET":
        return render_template('user_info.html')
    else:
        diet = request.form.getlist('diet')
        allergy = request.form.getlist('health')
        likes = request.form['users_likes'].split(',')
        dislikes = request.form['users_dislikes'].split(',')

        breakfast_recipes = yummly.search_recipes(likes, dislikes, diet, allergy, BREAKFAST_COURSE, [21])
        lunch_recipes = yummly.search_recipes(likes, dislikes, diet, allergy, LUNCH_COURSE, [21])
        dinner_recipes = yummly.search_recipes(likes, dislikes, diet, allergy, DINNER_COURSE, [21])
        
        answer = ''
        for i in range(len(breakfast_recipes)):
            rating, recipe = heapq.heappop(breakfast_recipes)
            answer = answer + recipe.name + '\r\n'
        answer = answer + '----------'

        for i in range(len(lunch_recipes)):
            rating, recipe = heapq.heappop(lunch_recipes)
            answer = answer + recipe.name + '\r\n'
        answer = answer + '----------'

        for i in range(len(dinner_recipes)):
            rating, recipe = heapq.heappop(dinner_recipes)
            answer = answer + recipe.name + '\r\n'
        answer = answer + '----------'

        return answer


if __name__ == '__main__':
    app.run()
