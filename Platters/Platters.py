from pymongo import MongoClient
from flask import Flask, request, render_template
import yummly, heapq
from calorie_calculator import *
from recipe_sorting import *

app = Flask(__name__)

MONGODB_URI = "mongodb://platters_hacks:platters@ds227168.mlab.com:27168/platters_hacks"
client = MongoClient(MONGODB_URI)
db = client.get_database('platters_hacks')

BREAKFAST_COURSE = ['course^course-Breakfast and Brunch', 'course^course-Breads']
LUNCH_COURSE = ['course^course-Main Dishes', 'course^course-Appetizers', 'course^course-Salads','course^course-Lunch']
DINNER_COURSE = ['course^course-Main Dishes', 'course^course-Soups', 'course^course-Salads']

@app.route('/', methods=["POST", "GET"])
def my_form():
    if request.method == "GET":
        print("I AM AT THE GET METHOD")
        return render_template('user_info.html')
    else:
        print("I AM AT THE POST METHOD")
        diet = request.form.getlist('diet')
        allergy = request.form.getlist('health')
        likes = request.form['users_likes'].split(',')
        dislikes = request.form['users_dislikes'].split(',')
        user_age = int(request.form['user_age'])
        user_height = int(request.form['user_height'])
        user_gender = request.form['user_gender']
        user_weight = int(request.form['user_weight'])
        user_activity_level = request.form['user_activity']
        print("I'VE RECEIEVED ALL INFO")

        breakfast_recipes = yummly.search_recipes(likes, dislikes, diet, allergy, BREAKFAST_COURSE, [60])
        print(breakfast_recipes)
        print("GOT BREAKFAST")
        lunch_recipes = yummly.search_recipes(likes, dislikes, diet, allergy, LUNCH_COURSE, [60])
        print("GOT LUNCH")
        dinner_recipes = yummly.search_recipes(likes, dislikes, diet, allergy, DINNER_COURSE, [60])
        print("GOT DINNER")

        user_caloric_intake = calculate_tee(user_weight, user_gender, user_age, user_height, user_activity_level)
        weekly_recipes = sort_recipes(breakfast_recipes,lunch_recipes, dinner_recipes, user_caloric_intake)
        print(weekly_recipes)

        """
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
        """

        return render_template("home.html", weeklyrecipes = weekly_recipes)


if __name__ == '__main__':
    app.run(debug=True)
