import os
import requests

URL = 'https://api.edamam.com/search'

class Recipe:
    """
    Object representing a recipe
    label - string : name in English of recipe
    image - string : URL to image corresponding to this recipe
    servings - float : number of servings recipe creates
    cals - float: total calories for entire recipe
    mass - float: total weight for entire recipe
    tags - list of string : keywords for recipe (not guaranteed to be populated)
    ingredients - list of Ingredient : ingredients corresponding to recipe
    nutrients - list of Nutrient : nutrients corresponding to recipe
    """
    def __init__(self, label, image, servings, cals, mass, tags, ingredients, nutrients):
        self.label = label
        self.image = image
        self.servings = servings
        self.cals = cals
        self.mass = mass
        self.tags = tags
        self.ingredients = ingredients
        self.nutrients = nutrients


class Ingredient:
    """
    Object representing an ingredient for a given Recipe.
    
    text - string : line of ingredient (includes measurements)
    weight - float : weight in grams of ingredient necessary
    """
    def __init__(self, text, weight):
        self.text = text
        self.weight = weight


class Nutrient:
    """
    Model for the values of a single nutrient (e.g. protein) in a given Recipe.

    label - string : english name of nutrient
    quantity - float: quantity of the nutrient
    unit - string: unit to attach to quantity
    percentage - float: percentage of daily value
    """

    def __init__(self, label, quantity, unit, percentage):
        self.label = label
        self.quantity = quantity
        self.unit = unit
        self.percentage


def get_edamam_id():
    """Return app ID from environment variable for safety."""
    return os.environ.get(EDAMAM_APP_ID)


def get_edamam_key():
    """Return secret key from environment variable for safety."""
    return os.environ.get(EDAMAM_KEY)


def query_recipes(likes, dislikes, diet, health):
    """
    Send a GET request to Edamam to search first 100 recipe results for matching
    query inputs. Returns a list of Recipe objects.

    likes - list of strings : keywords of foods user likes
    dislikes - list of strings : keywords of foods user dislikes
    diet - list of strings : keywords of Edamam diet filters
    health - list of strings : keywords of Edamam health filters
    """

    PARAMETERS = {'q':[''], 'app_id':[get_edamam_id()], 'app_key':[get_edamam_key()], 'from':[0], 'to':[100], 'diet':diet, 'health':health}

    request = requests.get(url = URL, params = PARAMETERS)
    response = request.json()
    recipes = parse_response(response)
    #TODO:Potentially pare down list by ranking with likes/dislikes list here

    return recipes


def parse_response(response):
    """Helper function to query_recipes to encapsulate JSON parsing."""

    recipes = []
    hits = response['hits']
    for hit in hits:
        recipe = hit['recipe']

        tags = []
        if 'tags' in recipe.keys():
            tags = recipe['tags']

        ingredients = []
        for ingredient in recipe['ingredients']:
            ingredients.append(Ingredient(ingredient['text'], ingredient['weight']))

        nutrients = []
        raw_nutrients = recipe['totalNutrients']
        raw_nutrient_percentages = recipe['totalDaily']
        for nutrient in raw_nutrients.keys():
            nutrients.append(Nutrient(raw_nutrients[nutrient]['label'], raw_nutrients[nutrient]['quantity'], raw_nutrients[nutrient]['unit'], raw_nutrient_percentages[nutrient]['quantity']))
            
        recipes.append(Recipe(recipe['label'], recipe['image'], recipe['yield'], recipe['calories'], recipe['totalWeight'], tags, ingredients, nutrients))
    return recipes


