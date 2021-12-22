from copy import copy

def ask_for_digits(query, max):
    while True:
        try: 
            input_value = int(input(f"{query}\n"))
            if input_value < 0 and input_value > max:
                raise Exception
        except ValueError:
            continue
        except Exception:
            print(f"Enter number between 0 - {max}")
            continue
        
        return input_value

def questions(query, options=None):
    while True:
        try: 
            input_value = input(f"{query}\n")
            if options:
                if input_value.lower() not in options:
                    raise Exception
        except ValueError:
            continue
        except Exception:
            print("Enter value between %s " % (" and ".join(options)) )
            continue

        return input_value

def select_ingredient(customer, order_list, ingredient_type, ingredients):
    _ingredients = copy(ingredients)
    while True:
        for index, ingredient in enumerate(_ingredients):
            print(f"{index} -\t{ingredient}")
        
        choosen_ingredient = ask_for_digits(f"{customer}, what {ingredient_type} would you like to use", 4)
        ingredient_name = _ingredients[choosen_ingredient]
        _ingredients.remove(ingredient_name)
        
        if order_list.get(ingredient_type): 
            order_list[ingredient_type].append(ingredient_name)
        else:
            order_list[ingredient_type] = [ingredient_name]

        result = questions(f"would you like to use more {ingredient_type}, yes or no", ["yes", "no"])
        
        if result.lower() == "no":
            break

        if not _ingredients:
            break

def generate_step(step_name, step):
    ingredient_name = step_name
    if len(step) > 1:
        pronoun = "these"
        last_word = step[len(step) - 1]
        rest_of_step = step[:-1]
        ingredients = ", ".join(rest_of_step)
        ingredients = f"{ingredients} and {last_word}"
    else:
        pronoun = "this"
        ingredients = ", ".join(step)
        
    return f" - Add {pronoun} {ingredient_name} - {ingredients}\n"

def read_recipe():
    with open("assets/week2_recipe.txt") as recipe:
            recipe = recipe.readlines()

    return recipe  


class Chef:
    customers = []

    proteins = ["meat", "milk", "fish", "cheese"]
    seasoning = ["salt", "pepper", "curry"]
    vegetable = ["pumpkin leave", "bitter leaf", "cassava leaf"]

    ingredients = {
        "proteins": proteins,
        "seasoning": seasoning,
        "vegetable": vegetable
    }

    def __init__(self):
        # Default
        self.servings = 1
        self.max_servings_at_once = 10

    # A dunder method to ease function call  
    def __call__(self):
        self.take_orders()
        self.cook()
        self.serve()

    # Give user Choices to choose from the buffet
    def take_orders(self):
        self.servings = ask_for_digits("How many plates would you like to order", self.max_servings_at_once)
        for _ in range(self.servings):
            name = questions("What's your name?")
            # To 
            self.customers.append([name, {}])

        for customer in self.customers:
            for ingredient_name, ingredient_values in self.ingredients.items():
                select_ingredient(customer[0], customer[1], ingredient_name, ingredient_values)
    
    
    # Read the recipe from file with readline  and replace some steps with user's choice
    def cook(self):
        recipe = read_recipe()
        for customer in self.customers:
            print(f"Now Cooking {customer[0]} meal")
            for index, each_step in enumerate(recipe):
                if index == 6:
                    print(generate_step("proteins", customer[1].get("proteins")))
                elif index == 7:
                    print(generate_step("vegetable", customer[1].get("vegetable")))
                elif index == 8:
                    print(generate_step("seasoning", customer[1].get("seasoning")))
                else:
                    print(each_step)
    
    # printing out Servings to customers 
    def serve(self):
        for customer in self.customers:
            print(f"Now serving {customer[0]}'s meal")

# Call the method
chef = Chef()
chef()
    
