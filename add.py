# Module for adding new airplane models and systems to the inventory.
# Contains functions to render menus, display options, and perform add operations.

# User will have an option any given time to select 0 and to go back to the menu.

from helpers import update_net_req as update_net_req
from helpers import get_dummy_data as get_dummy_data
from helpers import set_dummy_data as set_dummy_data
from helpers import intake_user_choice as intake_user_choice
from helpers import show_model_options as show_model_options
from helpers import get_models_options as get_models_options

### MENU HANDLING ###
def get_add_menu_options():
    """
    Return the list of add menu options.

    Returns:
        list[str]: Three menu items for adding models, systems, or returning to main.
    """
    options = [
        "Add new airplane model",
        "Add new system to airplane model",
        "Back to main menu"
    ]
    return options


def render_add_menu():
    """
    Render and return the formatted add menu as a string.

    Returns:
        str: Formatted ASCII menu with 3 add options (new model, new system, back).
    """
    title = "ADD MENU"

    message = f"""
{'=' * len(title)}
{title}
{'=' * len(title)}

"""
    i = 1
    for option in get_add_menu_options():
        message += f"\n{i}. {option}"
        i += 1
    message += "\n\n99 to go back to menu at any stage"

    return message


def show_add_menu():
    """
    Prints the add menu to the console.
    """
    print(render_add_menu())


### MODULE METHODS ###
def add_new_airplane_model(new_model):
    """
    Add a new airplane model to the dummy data with optional default systems.

    Args:
        new_model (str): The name of the new airplane model to add.

    Prompts the user for confirmation and initializes the model with default systems.
    """
    data = get_dummy_data()
    new_data = {'model': new_model}
    data.append(new_data)

    if new_model == 0: return 0

    continue_choice = input("Enter Y to initialize the new model with default data or press enter to abort: ").lower()
    if continue_choice == 'y':

        for model in data:

            if model['model'] == new_model:
                model['id'] = 34567890
                model['systems'] = {}
                cur_system_inventory = {}

                for system, inventory in data[0]['systems'].items():
                    cur_system_inventory.update({system: inventory})
                    model['systems'].update(cur_system_inventory)

    save_data_choice = input("The data is ready\nAre you sure you want to add it to the dummy-data?\nEnter Y for yes or press enter to abort: ").lower()
    if save_data_choice == 'y':
        set_dummy_data(data)
        update_net_req()

    print(f"New airplane {new_model} succesfully added to dummy-data")


def add_new_inventory(model, new_system):
    """
    Add a new system to an existing airplane model with default inventory.

    Args:
        model (int): 1-based menu index of the airplane model selection.
        new_system (str): The name of the new system to add.

    Initializes the new system with default inventory values.
    """
    
    data = get_dummy_data()
    model_options = get_models_options()
    cur_model = model_options[model - 1]

    for i in range(len(data)):
        if data[i]['model'] == cur_model:
            new_inventory = {new_system: {"available": 50, "gross": 100, "net-req": 70}}
            data[i]['systems'].update(new_inventory)
        i += 1
    save_data_choice = input("The data is ready\nAre you sure you want to add it to the dummy-data?\nEnter y for yes or press enter to abort: ").lower()
    if save_data_choice == 'y':
        set_dummy_data(data)
        update_net_req()
    print(f"New system {new_system} added to {cur_model} succesfully and added to dummy-data")


### MENU LOGIC ###
def add_menu():
    """
    Displays the add menu and handles user choices for adding models or systems.
    """
    add_menu_on = True
    while add_menu_on:
        
        show_add_menu()

        menu = get_add_menu_options()
        add_menu_user_choice = intake_user_choice(menu)
    
        if add_menu_user_choice == 1: # Add new model -> (Option to intiate with data or leave model empty)
            new_model = input("Enter new airplane model to add: ")
            print(new_model)
            if new_model == str(99):
                print("Aborted")
                add_menu()
                break

            add_new_airplane_model(new_model)

            continue_choice = input("Enter Y to update another inventory or press enter to go back to menu: ").lower()
            if continue_choice == 'y':
                add_menu()
        
        if add_menu_user_choice == 2: # Add new system to model

            show_model_options()
            model_options = get_models_options()
            model = intake_user_choice(model_options)

            if model == 99:
                print("Aborted")
                add_menu()
                break

            new_system = input("Enter new system to add: ")

            if new_system == str(99):
                print("Aborted")
                add_menu()
                break

            add_new_inventory(model, new_system)

            continue_choice = input("Enter Y to add another inventory or press enter to go back to main menu: ").lower()
            if continue_choice == 'y':
                add_menu()

        if add_menu_user_choice == 3: # Back to main menu
            add_menu_on = False
            msg = "Returning to main menu"
            print(f"\n{'-' * 30} {msg} {'-' * 30}")
