
# Module for updating inventory data.
# Contains functions to modify system inventory values for specific models.

from helpers import update_net_req as update_net_req
from helpers import show_model_options as show_model_options # Renders model options
from helpers import show_system_options as show_system_options # Renders model options
from helpers import show_inventory_options as show_inventory_options # Renders model options
from helpers import get_dummy_data as get_dummy_data # Gets current instance of dummy-data
from helpers import set_dummy_data as set_dummy_data # Sets dummy-data 
from helpers import get_models_options as get_models_options # Gets a list of models (From dummy-data instance)
from helpers import get_systems_options as get_systems_options # Gets a list of systems (From dummy-data instance)
from helpers import get_inventory_options as get_inventory_options # Gets a list of inventory properties (Hard coded)
from helpers import intake_user_choice as intake_user_choice # Takes user input and validates type and range (relative to given menu) 

### MODULE METHODS ###
def update_inventory(model, system, property):
    """
    Updates the inventory for a specific model, system, and property.

    Args:
        model (int): 0-based index of the airplane model from get_models_options().
        system (int): 0-based index of the system from get_systems_options().
        property (int): 0-based index of the property from get_inventory_options().
    """

    data = get_dummy_data()
    model_options = get_models_options()
    system_options = get_systems_options()
    property_options = get_inventory_options()

    for i in range(len(data)):
        if model_options[model] in data[i]['model']:
            cur_status = 0

            if system_options[system] in data[i]['systems']['peripheral-systems']:
                cur_status = data[i]['systems']['peripheral-systems'][system_options[system]][property_options[property]]
            else:
                cur_status = data[i]['systems'][system_options[system]][property_options[property]]

            print(f"UPDATE {model_options[model]} {system_options[system]} {property_options[property]}\nCURRENT: {cur_status}")

            new_status = int(input("Enter the new amount\n"))

            print(f"UPDATING: {model_options[model]} {system_options[system]} {property_options[property]}\nFROM {cur_status} TO {new_status}")

            continue_choice = input("Enter Y to approve or press enter to abort: ").lower()

            if continue_choice == 'y':

                if system_options[system] in data[i]['systems']['peripheral-systems']:
                    data[i]['systems']['peripheral-systems'][system_options[system]][property_options[property]] = new_status
                else:
                    data[i]['systems'][system_options[system]][property_options[property]] = new_status

            else:
                print("Action aborted going back to main menu")
                break
    set_dummy_data(data)
    update_net_req()

### MENU LOGIC ###
def update_manu():
    """
    Displays the update menu and handles user choices for updating inventory.
    """

    show_model_options()
    models_menu = get_models_options()
    user_model_choice = intake_user_choice(models_menu)
    
    if user_model_choice == 99:
        print("Aborted")
        update_manu()

    show_system_options()
    systems_menu = get_systems_options()
    user_system_choice = intake_user_choice(systems_menu)

    if user_system_choice == 99:
        print("Aborted")
        update_manu()

    show_inventory_options()
    inventory_menu = get_inventory_options()
    user_inventory_property_choice = intake_user_choice(inventory_menu)

    if user_inventory_property_choice == 99:
        print("Aborted")
        update_manu()

    update_inventory(user_model_choice-1, user_system_choice-1, user_inventory_property_choice-1)

    continue_choice = input("Enter Y to update another inventory or press enter to go back to main menu: ").lower()
    if continue_choice == 'y':
        update_manu()
        