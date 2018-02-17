from yummly import Recipe


class ShoppingList:
    def __init__(self):
        self.lst = {}
        self.measurements = ['whole', 'cup', 'cups', 'tsp', 'teaspoon', 'teaspoons', 'tbsp', 'tablespoons',
               'tablespoon', 'ounce', 'ounces', 'grams', 'pounds', 'pound' ,'lbs', 'lb',
               'kilograms', 'stick', 'cloves', 'ml', 'millilitres', 'L', 'mL', 'litres', 'slices', 'slices']

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
                        if len(amount) >= 2 and amount[1] == (self.lst[cur_ingredient].split(" "))[1]:
                            try:
                                value = str(int(ingredient_line_split[0]) + int(amount[0]))
                                self.lst[cur_ingredient] = value + " " + amount[1]
                            except ValueError:
                                value = amount[0] + " " + amount[1]
                                self.lst[cur_ingredient] = self.lst[cur_ingredient] + " + " + value
                        elif len(amount) >= 2:
                            value = amount[0] + " " + amount[1]
                            self.lst[cur_ingredient] = self.lst[cur_ingredient] + " + " + value

                        else:
                            self.lst[cur_ingredient] = self.lst[cur_ingredient] + " + " + amount[0]

                    else:
                        self.lst[cur_ingredient] = "unknown"

                i += 1

        return self.lst




