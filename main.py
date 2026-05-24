
# Main application file for the inventory manager.
# This script initializes the application, loads data, and runs the main menu loop.

from helpers import intake_user_choice as intake_user_choice
from helpers import get_data_base as get_data_base
from helpers import set_data_base as set_data_base
from helpers import set_dummy_data as set_dummy_data
from helpers import get_dummy_data as get_dummy_data
from helpers import update_net_req as update_net_req

from display_menu import display_menu as display_menu
from update import update_manu as update_manu
from add import add_menu as add_menu
from delete import delete_menu as delete_menu
from report import generate_report as generate_report


### MAIN MENU RENDERING ### 
def get_main_menu_options():
    options_list = [
    "1. Display data",
    "2. Update data",
    "3. Add new data",
    "4. Delete data",
    "5. View report for all inventories",
    "6. Commit data",
    "7. Exit program"
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
{'=' * len(title)}"""

    for option in get_main_menu_options():
        message += f"\n{option}"

    return message

def show_main_menu():
    """Prints the main menu to the console."""
    main_menu = generate_main_menu()
    print(main_menu)
    

### MAIN MANU OPRETIONS ###
# Initiate dummy-data to data-base 
data_base = get_data_base()
set_dummy_data(data_base)
update_net_req()

print("\n\nWELCOME TO INVENTORY MNGR")

### STATE VARIABLES ###
is_saved = False
on = True
menu = get_main_menu_options()

### MENU LOGIC ###
while on:

    show_main_menu()

    user_choice = intake_user_choice(menu)

    if user_choice == 1: # DISPLAY -> Display menu -> 1.By system menu, 2.By model menu
        display_menu()
        
    if user_choice == 2: # UPDATE -> Choose model -> Choose system -> Choose inventory property -> Approve
        update_manu()

    if user_choice == 3: # ADD -> 
        add_menu()

    if user_choice == 4:  # DELETE
        delete_menu()
        
    if user_choice == 5: # VIEW REPORT FOR ALL INVENTORIES
        generate_report()

    if user_choice == 6: # SAVE
        dummy_data = get_dummy_data()
        continue_choice = input("Are you sure you want to commit data permanently?\nTHIS ACTION IS PERMANENT !\nEnter y for yes or press enter to abort")
        if continue_choice == 'y':
            set_data_base(dummy_data)
            is_saved = True

    if user_choice == 7: # EXIT
        if is_saved:
            message = "Thank you for using INVENTORY MNGR"
            print(f"\n\n{'=' * len(message)}\n{message}\n{'=' * len(message)}\n\n")
        else:
            try:
                dummy_data = get_dummy_data()
                exit_save_choice = input("\n* The changes you maid were not saved !\nDo you want to save the changes ?\nEnter YES to save or NO to exit INVENTORY MNGR.\n").lower()
                if exit_save_choice == 'yes':
                    set_data_base(dummy_data)
                    message = "Thank you for using INVENTORY MNGR"
                    print(f"\n\n{'=' * len(message)}\n{message}\n{'=' * len(message)}\n\n")
                    on = False
                    break
                elif exit_save_choice == 'no':
                    message = "Thank you for using INVENTORY MNGR"
                    print(f"\n\n{'=' * len(message)}\n{message}\n{'=' * len(message)}\n\n")
                    on = False
                    break
                else:
                    raise Exception (f"\nInvalid choice.\nPlease enter YES or NO.")
            except Exception as e:
                print(e)
        on = False
                
                

        
