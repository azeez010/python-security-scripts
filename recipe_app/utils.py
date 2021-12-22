import re
from copy import copy

# Ask for number with maximum, raise exception and loop on any wrong input
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

# Ask question in string format with optional options, raise exception and loop on any wrong input 
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

# A series of loops to ask questions and save it output in a data structure
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

# A function to generate string from it inputs
# It generate Food recipe step from arrays with logics
def generate_step(step_name, step):
    ingredient_name = step_name
    if step:
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
    return ""

# To simply read file
def read_recipe():
    with open("assets/week2_recipe.txt") as recipe:
            recipe = recipe.readlines()

    return recipe

# Uses regex to enable user to make order by typing
def search(*args):
    proteins, seasoning, vegetable = args
    protein = "|".join(proteins)
    seasonings = "|".join(seasoning)
    vegetables = "|".join(vegetable)
    all_query = f"{protein}|{seasonings}|{vegetables}"
    all_query = re.sub(" ", "|", all_query)
    search_query = re.compile(r"(?:%s)" %all_query, re.I)
    
    def querysearch(query):
        match = re.findall(search_query, query)
        return match

    return querysearch