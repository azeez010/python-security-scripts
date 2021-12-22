from week5cheflib.utils import *

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

    def natural_search(self, customer_name, customer_list):
        order = questions(f"{customer_name}, What do you want?")
        search_feature = search(self.proteins, self.seasoning, self.vegetable)
        orderlist = search_feature(order)

        for _order in orderlist:
            if _order in self.seasoning:
                if customer_list.get("seasoning"): 
                    customer_list["seasoning"].append(_order)
                else:
                    customer_list["seasoning"] = [_order]
            
            
            elif _order in self.proteins:
                if customer_list.get("proteins"): 
                    customer_list["proteins"].append(_order)
                else:
                    customer_list["proteins"] = [_order]
            
            elif _order in self.vegetable:
                if customer_list.get("vegetable"): 
                    customer_list["vegetable"].append(_order)
                else:
                    customer_list["vegetable"] = [_order]
    
    # Initialize class
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
        self.servings = ask_for_digits("You many plates would you like to order", self.max_servings_at_once)
        for _ in range(self.servings):
            name = questions("What's your name?") 
            self.customers.append([name, {}])

        for customer in self.customers:
            service_choice = ask_for_digits(f"Dear {customer[0]}, \n1 - Do you wanna see the menu-list \n2 - Do you wanna ask for what we have orally", 2)
            if service_choice == 1:
                for ingredient_name, ingredient_values in self.ingredients.items():
                    select_ingredient(customer[0], customer[1], ingredient_name, ingredient_values)
            else:
                self.natural_search(customer[0], customer[1])

    # Read the recipe from file with readline  and replace some steps with user's choice       
    def cook(self):
        recipe = read_recipe()
        for customer in self.customers:
            print(f"Now Cooking {customer[0]} meal")
            for index, each_step in enumerate(recipe):
                if index == 6:
                    add_ingredient = generate_step("proteins", customer[1].get("proteins"))
                    if add_ingredient:
                        print(add_ingredient)

                elif index == 7:
                    add_ingredient = generate_step("vegetable", customer[1].get("vegetable"))
                    if add_ingredient:
                        print(add_ingredient)

                elif index == 8:
                    add_ingredient = generate_step("seasoning", customer[1].get("seasoning"))
                    if add_ingredient:
                        print(add_ingredient)
                else:
                    print(each_step)

    # printing out Servings to customers      
    def serve(self):
        for customer in self.customers:
            print(f"Now serving {customer[0]}'s meal")
