from edamam import Ingredient
from edamam import Recipe


class ShoppingList:
    def __init__(self, text, weight):
        self.list = {}

    def add(self, ingredient):
        if isinstance(ingredient, Ingredient):
            if ingredient.text in self.list:
                self.list[ingredient.text] = self.list[ingredient.text] + \
                                             ingredient.weight
            else:
                self.list[ingredient.text] = ingredient.weight
        return self.list



        # def remove(self, ):
        #     if isinstance(name, str):
        #         if name in self.list:
        #             if weight < self.list[name]:
        #                 self.list[name] -= weight
        #             else:
        #                 self.list.pop(name)
        #
        #
