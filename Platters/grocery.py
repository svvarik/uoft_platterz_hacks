from yummly import Recipe


class ShoppingList:
    def __init__(self):
        self.lst = {}
        self.measurements = ['whole', 'cup', 'cups', 'tsp', 'teaspoon', 'teaspoons', 'tbsp', 'tablespoons',
               'tablespoon', 'ounce', 'ounce', 'grams', 'pounds', 'pound' ,'lbs', 'lb',
               'kilograms', 'stick', 'cloves', 'ml', 'millilitres', 'L', 'mL', 'litres']

    def add(self, recipe):
        if isinstance(recipe, Recipe):
            i = 0
            while i < len(recipe.ingredients):
                ingredient_line = recipe.ingredient_lines[i]
                ingredient_line_split = ingredient_line.split(" ")
                if ingredient_line_split[1] in self.measurements:
                    amount = ingredient_line_split[:2]
                elif ingredient_line_split[0][0] in "0123456789":
                    amount = ingredient_line[0]
                else:
                    amount = "unknown"
                if recipe.ingredients[i] not in self.lst:
                    if isinstance(amount, list):
                        self.lst[recipe.ingredients[i]] = amount[0] + " " + amount[1]
                    else:
                        self.lst[recipe.ingredients[i]] = amount
                else:
                    cur_ingredient = recipe.ingredients[i]
                    if self.lst[cur_ingredient] != "unknown" and amount != "unknown":
                        print(amount[1])
                        print((self.lst[cur_ingredient].split(" "))[1])
                        if (amount[1] == ((self.lst[cur_ingredient]).split(" "))[1]):
                            try:
                                value = str(int(ingredient_line_split[0]) + int(amount.split(" ")[0]))
                                self.lst[cur_ingredient] = value + " " + amount[1]
                            except ValueError:
                                value = amount[0] + " " + amount[1]
                                self.lst[cur_ingredient] = self.lst[cur_ingredient] + " + " + value
                        else:
                            value = amount[0] + " " + amount[1]
                            self.lst[cur_ingredient] = self.lst[cur_ingredient] + " + " + value

                    else:
                        self.lst[cur_ingredient] = "unknown"

                i += 1

        return self.lst


if __name__ == '__main__':
    recipe = Recipe("French-Onion-Soup-The-Pioneer-Woman-Cooks-_-Ree-Drummond-41364","French Onion Soup",
                    ["Butter", "Yellow Onions", "White Wine", "Chicken Broth", "beef Broth", "Minced Garlic",
                     "Worcestershire Sauce", "French Bread", "Gruyere Cheese"],
                    ["1 stick Butter", "4 whole Large (or 6 Medium) Yellow Onions, Halved Root To Tip, And Sliced Thin",
                     "1 cup (generous) Dry White Wine", "4 cups Low Sodium Chicken Broth", "4 cups Beef Broth",
                     "2 cloves Minced Garlic",
                     "Worcestershire Sauce", "Several Thick Slices Of French Bread Or Baguette",
                     "5 ounces, weight (to 7 Ounces) Gruyere Cheese, Grated"])

    slst = ShoppingList()
    print(slst.add(recipe))

