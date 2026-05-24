# Module containing utility functions for data handling and user interface.
# Includes functions for loading/saving data, displaying options, and getting user input.

import json

DUMMY_DATA_PATH = "./dummy_data.json"
DATA_BASE_PATH = "./data_base.json"

### Data helpers ###
def get_dummy_data():
    """
    Loads and returns the dummy data from the JSON file.

    Returns:
        list: The dummy data list.
    """
    
    with open(DUMMY_DATA_PATH, 'r') as dummy_data_file:
        dummy_data = json.load(dummy_data_file)
    return dummy_data


def get_data_base():
    """
    Loads and returns the data base from the JSON file.

    Returns:
        dict: The data base dictionary.
    """
    with open(DATA_BASE_PATH, 'r') as data_base_file:
        data_base = json.load(data_base_file)
    return data_base


def set_dummy_data(data):
    """
    Saves the provided data to the dummy data JSON file.

    Args:
        data: The data to save.
    """
    with open(DUMMY_DATA_PATH, 'w') as dummy_data_file:
        json.dump(data, dummy_data_file)
    

def set_data_base(data):
    """
    Saves the provided data to the data base JSON file.

    Args:
        data: The data to save.
    """
    with open(DATA_BASE_PATH, 'w') as data_base_file:
        json.dump(data, data_base_file)


def update_net_req():
    """
    Updates the 'net-req' for all systems in the dummy data by calculating gross - available.
    Handles both top-level systems and nested peripheral-systems.
    Saves the updated data back to dummy_data.json.
    """
    data = get_dummy_data()
    for model in data:
        for key, system in model['systems'].items():
            if key == 'peripheral-systems':
                for sub_key, sub_system in system.items():
                    sub_system['net-req'] = sub_system['gross'] - sub_system['available']
            else:
                system['net-req'] = system['gross'] - system['available']
    set_dummy_data(data)


def get_systems_options(user_input=''):
    """
    Retrieves the list of system keys based on user input.

    Args:
        user_input (str): 'peri' for peripheral systems, 'sys' for main systems, '' for all.

    Returns:
        list: The list of system keys.
    """

    data = get_dummy_data()
    cur_data = None
    all_keys_list = []
    cur_data_indx = 0
    periphral_systems_keys = []
    systems_keys = []

    # Determine the model with highest number of systems
    for i in range(len(data)):
        cur_systems_length = len(data[i-1]['systems']) + len(data[i-1]['systems']['peripheral-systems'])
        next_systems_length = len(data[i]['systems']) + len(data[i]['systems']['peripheral-systems'])
        if cur_systems_length > next_systems_length:
            cur_data_indx = i - 1
        if cur_systems_length < next_systems_length:
            cur_data_indx = i
        if cur_systems_length == next_systems_length:
            continue
        i += 1
    cur_data = data[cur_data_indx]

    # Get all systema keys for relevant model
    for key in cur_data['systems']:
        if key == 'peripheral-systems':
            periphral_systems_keys_list = cur_data['systems'][key].keys()
            for key in periphral_systems_keys_list:
                all_keys_list.append(key)
                periphral_systems_keys.append(key)
        else:
            all_keys_list.append(key)
            systems_keys.append(key)

    # Return systems devision by parameter
    if user_input == 'peri':
        return periphral_systems_keys
    elif user_input == 'sys':
        return systems_keys
    else:
        return all_keys_list


def get_models_options():
    """
    Returns the list of model names from the dummy data JSON.

    Returns:
        list[str]: Plane model identifiers, e.g. ['f-16', 'f-18'].
    """
    data = get_dummy_data()
    model_options = []
    for model in data:
        model_options.append(model['model'])

    return model_options


def get_inventory_options():
    """
    Returns the fixed inventory property options available for selection.

    Returns:
        list[str]: Inventory metric keys ['available', 'gross', 'net-req'].
    """

    inventory_options = [
        "available",
        "gross",
        "net-req"
    ]
    return inventory_options


### Menu interface helpers ###
def show_model_options():
    """
    Prints the list of available airplane models.
    """
    options_list = get_models_options()
    message = f"""
"""     
    i = 1
    for option in options_list:
        message += f"\n{i}.{option}"
        i += 1
    print(message)


def show_system_options():
    """
    Prints the list of available systems.
    """
    options_list = get_systems_options()
    message = """
"""
    i = 1
    for option in options_list:
        message += f"\n{i}.{option}"
        i += 1
    print(message)


def show_inventory_options():
    """
    Prints the inventory property options.
    """
    message = ""
    i = 1
    for option in get_inventory_options():
        message += f"\n{i}.{option}"
        i += 1
    print(message)


### Input helpers ###
def intake_user_choice(menu):
    """
    Prompt the user to enter a numeric menu choice and validate it.

    Args:
        menu (list): A list of menu options used for range validation.

    Returns:
        int: The validated choice selected by the user (1-based index).

    Behavior:
        - On invalid non-integer input, prints a custom error and reprompts.
        - On integer outside valid range, prints a range error and reprompts.
    """
    while True:
        try:
            choice = int(input("\nEnter choice then press enter: "))

            if choice == 99:
                return 99

            if choice < 1 or choice > len(menu):
                raise Exception(f"\nInvalid choice.\nPlease enter a number between 1 and {len(menu)}.")
            return choice
        
        except ValueError:
            error_msg = "\nInvalid choice.\nPlease enter a number."
            print(error_msg)
        except Exception as e:
            print(e)


def intake_airplane_model():
    """
    Display model options, prompt user input, and return selection.

    Returns:
        str: The selected airplane model.
    """
    show_model_options()
    menu = get_models_options()
    choice = intake_user_choice(menu)

    if choice == 99: return 99

    return choice


def intake_system():
    """
    Display system options, prompt user input, and return selection.

    Returns:
        str: The selected system.
    """
    show_system_options()
    menu = get_systems_options()
    choice = intake_user_choice(menu)

    if choice == 99: return 99

    return choice
        

def intake_property():
    """
    Display inventory property options, prompt user input, and return selection.

    Returns:
        str: The selected inventory property string.
    """
    show_inventory_options()
    menu = get_inventory_options()
    choice = intake_user_choice(menu)

    if choice == 99: return 99

    return choice
