import os

def clear_screen():
    """
    Function to clear the screen.
    """
    os.system("cls")

def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getwch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result

def menu(items):
    """
    Function to display a menu and allow the user to choose an item using "w" to go up and "s" to go down,
    and "enter" to select an item.
    """
    selected = 0
    while True:
        clear_screen()
        for i in range(len(items)):
            if i == selected:
                print(f"> {items[i]}")
            else:
                print(f"  {items[i]}")
        key = wait_key()
        if key == "w":  # Up arrow
            selected = (selected - 1) % len(items)
        elif key == "s":  # Down arrow
            selected = (selected + 1) % len(items)
        elif key == "d":  # Enter
            return selected
        else:
            print('Pres "s" to go down,\n"w" to go up\n"d" to select the element.')
            os.system('pause')