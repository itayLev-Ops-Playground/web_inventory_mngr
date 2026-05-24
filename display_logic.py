# Module containing logic for displaying inventory data.
# Includes functions to retrieve and display system inventories by various criteria.

from helpers import get_dummy_data as get_dummy_data
from helpers import get_systems_options as get_systems_options
from helpers import get_models_options as get_models_options


### DISPLAY MENU METHODS ###
def get_system_inventory_all(system):
    """
    Retrieves inventory data for a specific system across all airplane models.

    Args:
        system (str): The name of the system to query.

    Returns:
        list: A list of dictionaries containing model, system, and inventory data.
    """
    inventory = []
    for model in get_dummy_data():
        cur_inventory = {}
        cur_inventory['model'] = model['model']
        if system in model['systems']:
            cur_inventory['system'] = system
            available = 0
            gross = 0
            net_req = 0
            for property, status in model['systems'][system].items():
                if property == 'available':
                    available = status
                    cur_inventory[property] = status
                if property == 'gross':
                    gross = status 
                    cur_inventory[property] = status
                if property == 'net-req':
                    net_req = gross - available
                    cur_inventory[property] = net_req
        if system in model['systems']['peripheral-systems']:
            cur_inventory['system'] = system
            for property, status in model['systems']['peripheral-systems'][system].items():
                if property == 'available':
                    available = status
                    cur_inventory[property] = status
                if property == 'gross':
                    gross = status 
                    cur_inventory[property] = status
                if property == 'net-req':
                    net_req = int(gross) - int(available)
                    cur_inventory[property] = net_req
        inventory.append(cur_inventory)
    return inventory
# print(get_system_inventory_all('fuel-system'))


def display_system_inventory_all(system):
    """
    Displays inventory data for a specific system across all models.

    Args:
        system (str): The name of the system to display.
    """
    system_options = get_systems_options()
    print(get_systems_options()[system])
    inventory = get_system_inventory_all(system_options[system])
    for model in inventory:
        message = ""
        title = f"Inventory status for {model['model']} {system_options[system]}"
        print(f"\n\n{'=' * len(title)}\n{title}\n{'=' * len(title)}")
        message += f"""
AVAILABLE: {model['available']}
GROSS: {model['gross']}
NET-REQ: {model['net-req']}
"""
        alert_condition = model['gross'] / 2 < model['net-req']
        if alert_condition:
            message += f"\n\n{'!' * 45}\nALERT: Inventory is insufficient!\n{'!' * 45}"
        print(message)
    print('\n'+'-' * 45)


def get_system_inventory_by_model(model, system):
    """
    Retrieves inventory data for a specific system in a specific model.

    Args:
        model (str): The airplane model.
        system (str): The system name.

    Returns:
        dict: A dictionary with model, system, and inventory properties.
    """
    models_options = get_models_options()
    systems_options = get_systems_options()
    inventory = {}
    for cur_model in get_dummy_data():
        if cur_model['model'] == models_options[model]:
            inventory['model'] = cur_model['model']
            cur_system = systems_options[system]
            if cur_system in cur_model['systems']:
                inventory['system'] = cur_system
                for property, status in cur_model['systems'][cur_system].items():
                    inventory[property] = status
            if cur_system in cur_model['systems']['peripheral-systems']:
                inventory['system'] = cur_system
                for property, status in cur_model['systems']['peripheral-systems'][cur_system].items():
                    inventory[property] = status
    return inventory


def display_system_inventory_by_model(model, system):
    """
    Displays inventory data for a specific system in a specific model.

    Args:
        model (str): The airplane model.
        system (str): The system name.
    """
    inventory = get_system_inventory_by_model(model, system)
    message = ""
    title = f"Inventory status for {inventory['model']} {inventory['system']}"
    print(f"\n\n{'=' * len(title)}\n{title}\n{'=' * len(title)}")
    message += f"""
AVAILABLE: {inventory['available']}
GROSS: {inventory['gross']}
NET-REQ: {inventory['net-req']}"""     
    alert_condition = inventory['gross'] / 2 < inventory['net-req']
    if alert_condition:
        message += f"\n\n{'!' * 45}\nALERT: Inventory is insufficient!\n{'!' * 45}"
    print(message)
    print('\n'+'-' * 45)


def display_by_model(model):
    """
    Displays the systems list for a specific airplane model.

    Args:
        model (str): The airplane model.

    Returns:
        str: The formatted message string.
    """
    parts_msg = f"""
Airplane {model}:

{'=' * len("Main parts list:")}
Systems list:
{'=' * len("Main parts list:")}
"""
    for system in get_systems_options():
        parts_msg += f"\t- {system}\n"

    print(parts_msg)
    return parts_msg


def get_all_systems_inventory_by_model(model):
    """
    Retrieves all systems inventory data for a specific model.

    Args:
        model (str): The airplane model.

    Returns:
        dict: A dictionary with model and all systems' inventory data.
    """
    inventory = {}
    data = get_dummy_data()
    model_options = get_models_options()
    model -= 1
    for cur_model in data:
        if cur_model['model'] == model_options[model]:
            inventory['model'] = cur_model['model']
            for system, cur_inventory in cur_model['systems'].items():
                if system == 'peripheral-systems':
                    for peripheral_system, peripheral_inventory in cur_model['systems']['peripheral-systems'].items():
                        inventory[peripheral_system] = {}
                        for property, status in peripheral_inventory.items():
                            inventory[peripheral_system][property] = status
                else:                        
                    inventory[system] = {}
                    for property, status in cur_inventory.items():
                        inventory[system][property] = status
    return inventory
                    
            
def display_all_systems_inventory_by_model(model):
    """
    Displays all systems inventory for a specific model in a table format.

    Args:
        model (str): The airplane model.
    """

    data = get_all_systems_inventory_by_model(model)

    message = """
"""
    for property, info in data.items():
        if property == 'model':
            message += f"\nModel: {info}"
            table_head = f"{"SYSTEM":20}|{"AVAILABLE":10}|{"GROSS":10}|{"NET-REQ":10}"
            message += f"\n\n{table_head}"
            message += f"\n{'-' * len(table_head)}"
        else:
            message += f"\n{property:20}|{info['available']:10}|{info['gross']:10}|{info['net-req']:10}"
    print(message)
    print('\n'+'-' * 45)


def display_all_systems_inventory_for_all_airplanes():
    """
    Displays all systems inventory for all airplane models.
    """

    model_options = get_models_options()

    for i in range(len(model_options)):
        display_all_systems_inventory_by_model(i)
        i += 1        

    print('\n'+'-' * 45)
