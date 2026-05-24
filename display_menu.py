# Module for handling the display menu interface.
# Manages user choices for displaying inventory data by system or by model.

# from render_menu import get_display_menu_options as get_display_menu_options
# from render_menu import get_display_by_model_menu_options as get_display_by_model_menu_options
# from render_menu import get_display_by_part_menu_options as get_display_by_part_menu_options
# from render_menu import show_display_menu as show_display_menu
# from render_menu import show_display_by_part_menu as show_display_by_part_menu
# from render_menu import show_display_by_model_menu as show_display_by_model_menu

from display_logic import display_system_inventory_all as display_system_inventory_all
from display_logic import display_system_inventory_by_model as display_system_inventory_by_model
from display_logic import display_all_systems_inventory_by_model as display_all_systems_inventory_by_model
from display_logic import display_all_systems_inventory_for_all_airplanes as display_all_systems_inventory_for_all_airplanes

from helpers import intake_airplane_model as intake_airplane_model
from helpers import intake_system as intake_system
from helpers import intake_user_choice as intake_user_choice
from helpers import show_model_options as show_model_options
from helpers import show_system_options as show_system_options
from helpers import get_systems_options as get_systems_options
from helpers import get_models_options as get_models_options


### DISPLAY MENU RENDERING ###
def get_display_menu_options():
    options_list = [
        "1. Display by system",
        "2. Display by airplane",
        "3. Back to main menu"
    ]

    return options_list

def generate_display_menu():
    """
    Generates the display menu as a formatted string.

    Returns:
        str: The display menu string.
    """
    title = "DISPLAY MENU"

    message = f"""
{'=' * len(title)}
{title}
{'=' * len(title)}"""

    for option in get_display_menu_options():
        message += f"\n{option}"
    message += "\n\n99 to go back to menu at any stage"

    return message

def show_display_menu():
    """Prints the display menu to the console."""
    print(generate_display_menu())
    

### DISPLAY MENU -> DISPLAY BY PART MENU RENDERING###
def get_display_by_part_menu_options():
    options_list = [
        "1. Display system for all models",
        "2. Display system for one model",
        "3. Back to main display menu"      
    ]

    return options_list

def generate_display_by_part_menu():
    """
    Generates the display by part menu as a formatted string.

    Returns:
        str: The display by part menu string.
    """
    title = "DISPLAY BY SYSTEM MENU"

    message = f"""
{'=' * len(title)}
{title}
{'=' * len(title)}"""

    for option in get_display_by_part_menu_options():
        message += f"\n{option}"
    message += "\n\n99 to go back to menu at any stage"

    return message

def show_display_by_part_menu():
    """Prints the display by part menu to the console."""
    print(generate_display_by_part_menu())
    
    
### DISPLAY MENU -> DISPLAY BY MODEL ###
def get_display_by_model_menu_options():
    options_list = [
        "1. Display all systems by airplane",
        "2. Display all systems for all airplanes",
        "3. Back to main display menu"
    ]

    return options_list

def generate_display_by_model_menu():
    """
    Generates the display by model menu as a formatted string.

    Returns:
        str: The display by model menu string.
    """
    title = "DISPLAY BY MODEL MENU"

    message = f"""
{'=' * len(title)}
{title}
{'=' * len(title)}"""
    for option in get_display_by_model_menu_options():
        message += f"\n{option}"
    message += "\n\n99 to go back to menu at any stage"

    return message

def show_display_by_model_menu():
    """Prints the display by model menu to the console."""
    print(generate_display_by_model_menu())


### MENU LOGIC ###
def display_menu():
    """
    Displays the main display menu and handles user choices for viewing inventory data.
    """
    display_manu_on = True
    while display_manu_on:

        show_display_menu()

        menu = get_display_menu_options()
        display_menu_user_choice = intake_user_choice(menu)

        if display_menu_user_choice == 1: # DISPLAY BY SYSTEM -> 1. DISPLAY SYSTEM FOR ALL MODELS, 2. DISPLAY SYSTEM BY AIRPLANE

            by_part_menu_on = True
            while by_part_menu_on:

                show_display_by_part_menu()
                
                menu = get_display_by_part_menu_options()
                by_system_user_choice = intake_user_choice(menu)

                if by_system_user_choice == 1: #  DISPLAY SYSTEM FOR ALL MODELS -> Choose system
                    system_user_choice = intake_system()
                    if system_user_choice == 99:
                        print("\nAborted.")
                        display_menu()
                        break

                    display_system_inventory_all(system_user_choice-1)

                if by_system_user_choice == 2: # DISPLAY SYSTEM BY MODEL -> Choose system -> Choose model
                    model = intake_airplane_model()
                    if model == 99:
                        print("\nAborted.")
                        display_menu()
                        break

                    system = intake_system()
                    if system == 99:
                        print("\nAborted.")
                        display_menu()
                        break

                    display_system_inventory_by_model(model-1, system-1)

                if by_system_user_choice == 3:
                    by_part_menu_on = False
                    msg = "Returning to display menu"
                    print(f"\n{'-' * 30} {msg} {'-' * 30}")

        if display_menu_user_choice == 2: # DISPLAY BY MODEL -> 1. DISPLAY BY ALL SYSTEMS FOR MODEL, 2. DISPLAY ALL SYSTEMS FOR ALL MODELS
            by_model_menu_on = True

            while by_model_menu_on:

                show_display_by_model_menu()
                menu = get_display_by_model_menu_options()
                by_model_user_choice = intake_user_choice(menu)

                if by_model_user_choice == 99:
                    print("\nAborted.")
                    display_menu()
                    break
                if by_model_user_choice == 1: # DISPLAY BY ALL SYSTEMS FOR MODEL
                    

                    model_choice = intake_airplane_model()
                    if model_choice == 99:
                        print("\nAborted.")
                        display_menu()
                        break
                    display_all_systems_inventory_by_model(model_choice)

                if by_model_user_choice == 2: # DISPLAY ALL SYSTEMS FOR ALL MODELS
                    display_all_systems_inventory_for_all_airplanes()

                if by_model_user_choice == 3:
                    by_model_menu_on = False
                    msg = "Returning to display menu"
                    print(f"\n{'-' * 30} {msg} {'-' * 30}")

        if display_menu_user_choice == 3: # EXIT MENU
            display_manu_on = False
            msg = "Returning to main menu"
            print(f"\n{'-' * 30} {msg} {'-' * 30}")
            break
