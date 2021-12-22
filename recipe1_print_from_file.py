class Recipe:
    recipe_name = "Basil Flavoured Mac and Cheese"
    servings = 1

    def __init__(self):
        # Reads the file in to memory and attach to a variable before close the file
        with open("assets/week2_recipe.txt") as recipe:
            self.recipe = recipe.read()  

    # Display file contain unbuffered
    def show(self ):
        print(self.recipe_name)
        print("============================================")
        print(f'Serving Size: {self.servings}')
        print("============================================")
        print(self.recipe)


recipe = Recipe()
recipe.show()