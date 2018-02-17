PAL = {'extremely_inactve': 1.35, 'sedentary': 1.53, 'moderately_active': 1.76, 'vigorously_active': 2.25, 'extremely_active': 2.4}

kg_to_lbs = 2.20462

cm_to_inches = 0.393701



def calculate_bmr(imperial_or_metric, weight, sex, age, height, activity_level):
    '''
    Calculate calories given a user profile.

    Precondition: Weight and Height are in metric system.

    Credit: Took function from Wikipedia page on Harris-Benedict equation.
            URL: https://en.wikipedia.org/wiki/Harris%E2%80%93Benedict_equation

    @param weight: int
    @param sex: str
    @param age: int
    @param height: int
    @param pal: int
    @return:
    '''

    user_bmr = 0

    if imperial_or_metric == 'imperial':
        if sex == 'female':
            user_bmr = (10 * (weight / kg_to_lbs)) + (6.25 * (height / cm_to_inches)) - (5 * age) - 161
        if sex == 'male':
            user_bmr = (10 * (weight / kg_to_lbs)) + (6.25 * (height / cm_to_inches)) - (5 * age) + 5

    if imperial_or_metric == 'metric':
        if sex == 'female':
            user_bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        if sex == 'male':
            user_bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    return user_bmr * PAL[activity_level]


