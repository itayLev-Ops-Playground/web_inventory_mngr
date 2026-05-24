# Module for rendering menu strings.
# Contains functions to generate formatted menu text for various application menus.

### MENU RENDERING METHODS ###
### MAIN MENU ### 
def get_main_menu_options():
    options_list = [
    "1. Display data",
    "2. Update data",
    "3. Add new data",
    "4. Delete data",
    "5. Commit data",
    "6. Exit program"
    ]
    
    return options_list

def generate_main_menu():
    """
    Generates the main menu as a formatted string.

    Returns:
        str: The main menu string.
    """
    title = "MAIN MENU"

    message = f"""
{'=' * len(title)}
{title}
{'=' * len(title)}

"""

    for option in get_main_menu_options():
        message += f"\n{option}"

    return message

### DISPLAY MENU ###
def get_display_menu_options():
    options_list = [
        "1. Display by  part",
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
{'=' * len(title)}

"""

    for option in get_display_menu_options():
        message += f"\n{option}"
    message += "\n\n99 to go back to menu at any stage"

    return message

### DISPLAY MENU -> DISPLAY BY PART ###
def get_display_by_part_menu_options():
    options_list = [
        "1. Display part for all models",
        "2. Display part for one model",
        "3. Back to main display menu"      
    ]

    return options_list

def generate_display_by_part_menu():
    """
    Generates the display by part menu as a formatted string.

    Returns:
        str: The display by part menu string.
    """
    title = "DISPLAY PART MENU"

    message = f"""
{'=' * len(title)}
{title}
{'=' * len(title)}

"""

    for option in get_display_by_part_menu_options():
        message += f"\n{option}"
    message += "\n\n99 to go back to menu at any stage"

    return message

### DISPLAY MENU -> DISPLAY BY MODEL ###
def get_display_by_model_menu_options():
    options_list = [
        "1. Display all parts by airplane",
        "2. Display all parts for all airplanes",
        "3. Back to main display menu"
    ]

    return options_list

def generate_display_by_model_menu():
    """
    Generates the display by model menu as a formatted string.

    Returns:
        str: The display by model menu string.
    """
    title = "DISPLAY BY AIRPLANE MENU"

    message = f"""
{'=' * len(title)}
{title}
{'=' * len(title)}

"""
    for option in get_display_by_model_menu_options():
        message += f"\n{option}"
    message += "\n\n99 to go back to menu at any stage"

    return message

### MENU METHODS PRINTING ###
def show_main_menu():
    """Prints the main menu to the console."""
    print(generate_main_menu())

def show_display_menu():
    """Prints the display menu to the console."""
    print(generate_display_menu())

def show_display_by_part_menu():
    """Prints the display by part menu to the console."""
    print(generate_display_by_part_menu())

def show_display_by_model_menu():
    """Prints the display by model menu to the console."""
    print(generate_display_by_model_menu())
