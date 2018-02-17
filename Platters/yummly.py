import os, requests, heapq

SEARCH_URL = 'http://api.yummly.com/v1/api/recipes'
GET_URL = 'http://api.yummly.com/v1/api/recipe/'

class Recipe:
    """
    Object representing a recipe.
    """
    def __init__(self, ID, name, ingredients, ingredient_lines, size='', images=[], nutrition=[], thumbnails=[], site='', cook_time=0):
        self.ID = ID        
        self.name = name
        self.ingredients = ingredients
        self.ingredient_lines = ingredient_lines

        self.size = size
        self.images = images
        self.thumbnails = thumbnails
        self.site = site
        self.nutrition = nutrition
        self.cook_time = cook_time


class Nutrient:
    """
    Model for the values of a single nutrient (e.g. protein) in a given Recipe.
    """

    def __init__(self, attribute, description, value, unit, name, abbreviation, plural, plural_abbreviation):
        self.attribute = attribute
        self.description = description
        self.value = value
        self.unit = unit

        self.name = name
        self.abbreviation = abbreviation
        self.plural = plural
        self.plural_abbreviation = plural_abbreviation


def get_app_id():
    """Return app ID from environment variable for safety."""
    return os.environ.get('YUMMLY_APP_ID')


def get_app_key():
    """Return secret key from environment variable for safety."""
    return os.environ.get('YUMMLY_KEY')


def search_recipes(likes, dislikes, diet, allergy, courses, results, q=''):
    """
    Send a search request to yummly.

    likes - list of strings : keywords of foods user likes
    dislikes - list of strings : keywords of foods user dislikes
    diet - list of strings : keywords of Edamam diet filters
    allergy - list of strings : keywords of Edamam health filters
    courses - list of strings : breakfast, lunch, or dinner(include brunch etc)
    q - string : search query string
    results - int : max number of results to request
    """

    PARAMETERS = {'_app_id':[get_app_id()], '_app_key':[get_app_key()]}

    if not dislikes == [u'']:
        PARAMETERS['excludedIngredient[]'] = dislikes

    if not q == '':
        PARAMETERS['q'] = q

    if not diet == []:
        PARAMETERS['allowedDiet[]'] = diet

    if not allergy == []:
        PARAMETERS['allowedAllergy[]'] = diet

    if not courses == []:
        PARAMETERS['allowedCourse[]'] = courses

    PARAMETERS['maxResult'] = results

    request = requests.get(url = SEARCH_URL, params = PARAMETERS)
    response = request.json()
    recipes = parse_search_response(response)

    queue_recipes = []
    if not likes == [u'']:
        for recipe in recipes:
            rating = 0
            for like in likes:
                if like in recipe.ingredients:
                    rating = rating - 1
            heapq.heappush(queue_recipes,(rating, recipe))

    else:
        for recipe in recipes:
            heapq.heappush(queue_recipes,(0, recipe))

    return queue_recipes


def parse_search_response(response):
    """Helper function to search_recipes to encapsulate JSON parsing."""

    recipes = []
    matches = response['matches']
    for recipe in matches:
        thumbnails = []
        if 'smallImageUrls' in recipe.keys():
            thumbnails = recipe['smallImageUrls']

        site = ''
        if 'sourceDisplayName' in recipe.keys():
            site = recipe['sourceDisplayName']

        cook_time = 0
        if 'totalTimeInSeconds' in recipe.keys():
            thumbnails = recipe['totalTimeInSeconds']
    
        #Get further information for nutrition and steps etc.
        PARAMETERS = {'_app_id':[get_app_id()], '_app_key':[get_app_key()]}
        URL = GET_URL + recipe['id']
        get_request = requests.get(url = URL, params = PARAMETERS)
        get_response = get_request.json()

        nutrition = {}
        if 'nutritionEstimates' in get_response.keys():
            values = get_response['nutritionEstimates']
            for value in values:
                nutrition[value['attribute']] = {}

                if 'description' in value.keys():
                    nutrition[value['attribute']]['description'] = value['description']

                if 'value' in value.keys():
                    nutrition[value['attribute']]['value'] = value['value']

                if 'unit' in value.keys():
                    nutrition[value['attribute']]['unit'] = value['unit']

                if 'name' in value.keys():
                    nutrition[value['attribute']]['name'] = value['name']

                if 'abbreviation' in value.keys():
                    nutrition[value['attribute']]['abbreviation'] = value['abbreviation']

                if 'plural' in value.keys():
                    nutrition[value['attribute']]['plural'] = value['plural']

                if 'pluralAbbreviation' in value.keys():
                    nutrition[value['attribute']]['pluralAbbreviation'] = value['pluralAbbreviation']

        images = []
        if 'images' in get_response.keys():
            images = get_response['images']

        size = ''
        if 'yield' in get_response.keys():
            size = get_response['yield']

        recipes.append(Recipe(recipe['id'], recipe['recipeName'], recipe['ingredients'], get_response['ingredientLines'], size, images, nutrition, thumbnails, site, cook_time))
    return recipes


