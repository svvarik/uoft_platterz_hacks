PAL = {'extremely_inactve': 1.1, 'sedentary': 1.2, 'moderately_active': 1.4, 'vigorously_active': 1.8, 'extremely_active': 2.0}

def calculate_tee(weight, sex, age, height, activity_level):
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

    if sex == 'female':
        user_bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    if sex == 'male':
        user_bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    if sex == 'other':
        user_bmr = (10 * weight) + (6.25 * height) - (5 * age) - 83

    return user_bmr * PAL[activity_level]


