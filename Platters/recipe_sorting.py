breakfast_percentage = .25
lunch_percentage = .35
dinner_percentage = .40


def sort_recipes(breakfast_recipes ,lunch_recipes, dinner_recipes, user_caloric_intake):
    """
    Return a dictionary of dictionaries.
    {Monday: {Breakfast: , Lunch: ,Dinner: }, Tuesday...etc}
    :param breakfast_recipes:
    :param lunch_recipes:
    :param dinner_recipes:
    :return:
    """
    weekly_recipe = {"Monday": {}, "Tuesday": {}, "Wednesday": {}, "Thursday":{}, "Friday": {} ,"Saturday": {}, "Sunday": {}}
    caloric_intake = round(user_caloric_intake)
    breakfast_allotment = round(caloric_intake * breakfast_percentage)
    lunch_allotment = round(caloric_intake*lunch_percentage)
    dinner_allotment = round(caloric_intake*dinner_percentage)
    tolerance = 100

    for day in weekly_recipe.keys():
        for recipe in breakfast_recipes:
            if recipe[1].nutrition['ENERC_KCAL'] in range(breakfast_allotment - tolerance, breakfast_allotment + tolerance):
                weekly_recipe[day]["Breakfast"] = recipe
        for recipe in lunch_recipes:
            if recipe[1].nutrition['ENERC_KCAL'] in range(lunch_allotment - tolerance, lunch_allotment + tolerance):
                weekly_recipe[day]["Lunch"] = recipe
        for recipe in dinner_recipes:
            if recipe[1].nutrition['ENERC_KCAL'] in range(dinner_allotment - tolerance, dinner_allotment + tolerance):
                weekly_recipe[day]["Dinner"] = recipe

    return weekly_recipe
    # """
    # user_breakfast_range = ((caloric_intake*breakfast_percentage)-100, (caloric_intake*breakfast_percentage)+100)
    # user_lunch_range = ((caloric_intake*lunch_percentage)-100, (caloric_intake*lunch_percentage)+100)
    # user_dinner_range = ((caloric_intake*breakfast_percentage)-100, (caloric_intake*breakfast_percentage)+100)
    # """