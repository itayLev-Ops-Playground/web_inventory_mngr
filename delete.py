# Module for deleting airplane models and systems from the inventory.
# Contains functions to render menus, display options, and perform delete operations.

from helpers import intake_user_choice as intake_user_choice
from helpers import intake_system as intake_system
from helpers import intake_airplane_model as intake_airplane_model
from helpers import show_model_options as show_model_options
from helpers import show_system_options as show_system_options
from helpers import get_models_options as get_models_options
from helpers import get_systems_options as get_systems_options
from helpers import get_dummy_data as get_dummy_data
from helpers import set_dummy_data as set_dummy_data

### MENU HANDLING ###
def get_delete_menu_options():
    """
    Return the list of delete menu options.

    Returns:
        list[str]: Three menu items for deleting models, systems, or returning to main.
    """
    options = [
        "Delete airplane model",
        "Delete system",
        "Back to main menu"        
    ]
    return options


def render_delete_menu():
    """
    Renders the delete menu options as a formatted string.

    Returns:
        str: The formatted menu string for deleting airplane models or systems.
    """
    title = "DELETE MENU"

    message = f"""
{'=' * len(title)}
{title}
{'=' * len(title)}

"""
    i = 1
    for option in get_delete_menu_options():
        message += f"\n{i}. {option}"
        i += 1
    message += "\n\n99 to go back to menu at any stage"

    return message


def show_delete_menu():
    """
    Prints the delete menu to the console.
    """
    print(render_delete_menu())


### MODULE METHODS ###
def delete_model(model):
    """
    Delete an airplane model from the dummy data.

    Args:
        model (int): 1-based menu index of the airplane model to delete.

    Prompts for confirmation before deletion.
    """
    data = get_dummy_data()
    models_options = get_models_options()
    del_indx = ''
    model -= 1

    for i in range(len(data)):
        if data[i]['model'] == models_options[model]:
            del_indx = i
        i += 1

    approve_choice = input(f"Are you sure you want to delete {models_options[model]} from dummy-data?\nEnter Yes for yes or enter to abort: ").lower()

    if approve_choice == 'yes':
        del data[del_indx]
        set_dummy_data(data)
    else:
        print("Aborted by the user")


def delete_system(model, system):
    """
    Delete a system from a specific airplane model.

    Args:
        model (int): 1-based menu index of the airplane model.
        system (int): 1-based menu index of the system to delete.

    Handles both main systems and peripheral systems.
    """
    data = get_dummy_data()
    models_options = get_models_options()
    systems_options = get_systems_options()
    is_peripheral = False
    del_indx = ''
    del_key = ''
    model -= 1
    system -= 1

    for i in range(len(data)):
        if data[i]['model'] == models_options[model]:
            for cur_system in data[i]['systems']:
                if cur_system == 'peripheral-systems':
                    for cur_system in data[i]['systems']['peripheral-systems']:
                        if cur_system == systems_options[system]:
                            is_peripheral = True
                            del_indx = i
                            del_key = cur_system
                else:
                    if cur_system == systems_options[system]:
                        is_peripheral = False
                        del_indx = i
                        del_key = cur_system

    approve_choice = input(f"Are you sure you want to delete {models_options[model]} {systems_options[system]} from dummy-data?\nEnter Yes for yes or enter to abort: ").lower()

    if approve_choice == 'yes':
        if is_peripheral:
            del data[del_indx]['systems']['peripheral-systems'][del_key]
            set_dummy_data(data)
        else:
            del data[del_indx]['systems'][del_key]
            set_dummy_data(data)
    else:
        print("Aborted by the user")

### MENU LOGIC ###
def delete_menu():
    """
    Displays the delete menu and handles user choices for deleting models or systems.
    """
    delete_menu_on = True
    while delete_menu_on:
        
        show_delete_menu()
        menu = get_delete_menu_options()
        delete_menu_user_choice = intake_user_choice(menu)
    
        if delete_menu_user_choice == 1: # Delete model
            model = intake_airplane_model()

            if model == 99:
                print("Aborted")
                delete_menu()
                break

            delete_model(model)
        
        if delete_menu_user_choice == 2: # Delete system
            model = intake_airplane_model()

            if model == 99:
                print("Aborted")
                delete_menu()
                break

            system = intake_system()

            if system == 99:
                print("Aborted")
                delete_menu()
                break

            delete_system(model, system)

        if delete_menu_user_choice == 3:
            delete_menu_on = False
            msg = "Returning to main menu"
            print(f"\n{'-' * 30} {msg} {'-' * 30}")
            