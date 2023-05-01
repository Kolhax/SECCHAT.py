import json
import keparmodule
import os

def clear_screen():
    """
    Clears the console screen for different operating systems.
    """
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Mac and Linux
    else:
        _ = os.system('clear')


while True:
    clear_screen()
    choices = ['Create User','Remove User','Quit']
    a = keparmodule.utils.menu(choices)
    if choices[a] == 'Create User':
        clear_screen()
        username = input('Username:  ')
        password = input('Password: ')
        with open('creds.json', 'r') as f:
            creds = json.load(f)
        creds[username] = password 
        with open('creds.json','w') as f:
            json.dump(creds, f)
        clear_screen()
        input('User Created! (press any key to continue)')            

    if choices[a] == 'Remove User':
        clear_screen()
        username = input('Username: ')
        with open('creds.json', 'r') as f:
            creds = json.load(f)
        creds.pop(username)
        with open('creds.json','w') as f:
            json.dump(creds, f)
        clear_screen()
        input('User removed! (press any key to continue)')             
    if choices[a] == 'Quit':
        exit()