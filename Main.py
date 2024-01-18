import inquirer,subprocess,os,json,time,requests, base64
from art import *
from colorama import init, Fore
init(autoreset=True)
clear = lambda: os.system('cls')
from pypresence import Presence
from cryptography.fernet import Fernet

class Main:
    
    def __init__(self):
        os.system("title Eclipse - Version: 0.0.1 - Test Version - Quick#0077")

        print("Connecting to Discord RPC...")

        try:
            client_id = '801310272282951731'
            RPC = Presence(client_id)
            RPC.connect()

            (RPC.update(state="Version: 0.0.1", details="Farming", large_image="logo",large_text="Eclipse", start=time.time()))
            self.rpcStatus = "Running"
        except Exception as e:
            print(Fore.RED + "Failed to connect to Discord RPC")
            self.rpcStatus = "Failed"

        print(Fore.MAGENTA + "Logging in")

        with open('Data/license.json', 'r') as f:

            if f.read() == "":
                print(Fore.RED + "License not found")
                self.license = input(Fore.RED + "Please enter your license: ")
            else:
                with open('Data/license.json', 'r') as f:
                    self.license = json.load(f)['License']
                    if self.license == "Owner":
                        print("Owner Login Bypassing Check...")
                    else:
                        pass
        
        print("Checking if owner key is set...")

        with open('Data/ownerKey.json', 'r') as f:
            if f.read() == "":
                print(Fore.RED + "No Owner Key Set - Please set it in the main menu")
                self.ownerStatus = "No"
                self.menu()
            else:
                print(Fore.GREEN + "Owner Key Has Been Set")
                self.ownerStatus = "Yes"
                self.menu()


    def menu(self):

        os.system('clear')
        clear()
        os.system(f"title Eclipse - Version: 0.0.1 - RPC: {self.rpcStatus} - License: Owner - Owner Key Set: {self.ownerStatus} - Quick#0077")

        Art=text2art("Eclipse")
        print(Fore.MAGENTA + Art)

        questions = [
            inquirer.List('Site',
                            message="Select an option",
                            choices=['NFT Owner', 'Wallet', 'Modules', 'Exit'],
                        ),
            ]
        answers = inquirer.prompt(questions)

        if answers['Site'] == 'NFT Owner':
            self.owner()
        elif answers['Site'] == 'Wallet':
            self.wallet()
        elif answers['Site'] == 'Modules':
            self.modules()
        elif answers['Site'] == 'Exit':
            clear()
            print(Fore.RED + "Exiting")
            time.sleep(1)
            exit()

    def owner(self):
        clear()
        Art=text2art("NFT Owner")
        print(Fore.MAGENTA + Art)

        with open('Data/ownerKey.json', 'r') as f:
            if f.read() == "":
                print(Fore.RED + "Owner Key not found")

                user_data = input("Enter your main wallet private key (This is encrypted and saved locally):")
                key = Fernet.generate_key()
                fernet = Fernet(key)
                enc_message = fernet.encrypt(user_data.encode())
                encoded_message = base64.b64encode(enc_message).decode()

                data_to_write = {'ownerKey': encoded_message}

                with open('Data/ownerKey.json', 'w') as file:
                    json.dump(data_to_write, file, indent=4)
            
                print(Fore.GREEN + "Saved Private Key")
                time.sleep(1)
                clear()
                self.menu()
            else:
                input("Owner Key already exists.  Would you like to change it? (Y/N): ")
                if input == "Y" or "y":
                    user_data = input("Enter your main wallet private key (This is encrypted and saved locally):")
                    key = Fernet.generate_key()
                    fernet = Fernet(key)
                    enc_message = fernet.encrypt(user_data.encode())
                    encoded_message = base64.b64encode(enc_message).decode()

                    data_to_write = {'ownerKey': encoded_message}

                    with open('Data/ownerKey.json', 'w') as file:
                        json.dump(data_to_write, file, indent=4)
                
                    print(Fore.GREEN + "Saved Private Key")
                    time.sleep(1)
                    clear()
                    self.menu()
                elif input == "N" or "n":
                    self.menu()
        

    def wallet(self):
        clear()
        Art=text2art("Wallet")
        print(Fore.MAGENTA + Art)

        file_path = 'Data/wallets.txt'

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                line_count = len(lines)
                if line_count == 0:
                    print(Fore.RED + "No wallets found - Add wallets or generate wallets from the modules section")
                    self.menu()
                else:
                    print(Fore.GREEN + f"Found {line_count} wallets")
                    input("Press enter to continue")
                    self.menu()
                    
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def modules(self):
        clear()
        Art=text2art("Modules")
        print(Fore.MAGENTA + Art)

        questions = [
            inquirer.List('Site',
                            message="Select an option",
                            choices=['Wallet Creator', 'Wallet Disperse', 'Websites', 'Wallet Sendback', 'Exit'],
                        ),
            ]
        answers = inquirer.prompt(questions)

        if answers['Site'] == 'Wallet Creator':
            self.walletCreator()
        elif answers['Site'] == 'Wallet Disperse':
            self.owner()
        elif answers['Site'] == 'Websites':
            self.sites()
        elif answers['Site'] == 'Wallet Sendback':
            self.modules()
        elif answers['Site'] == 'Exit':
            clear()
            print(Fore.RED + "Exiting")
            time.sleep(1)
            self.menu()

    def walletCreator(self):
        clear()
        Art=text2art("Wallet Creation")
        print(Fore.MAGENTA + Art)
        from Modules.walletCreator import Main as walletCreation
        walletCreation()
        input("Press enter to return back to Modules")
        self.modules()

    def sites(self):

        clear()
        Art=text2art("Sites")
        print(Fore.MAGENTA + Art)

        questions = [
            inquirer.List('Site',
                            message="Select an option",
                            choices=['Jupiter', 'Exit'],
                        ),
            ]
        answers = inquirer.prompt(questions)

        if answers['Site'] == 'Jupiter':
            self.jupSelection()
        elif answers['Site'] == 'Exit':
            clear()
            print(Fore.RED + "Exiting")
            time.sleep(1)
            self.modules()

    def jupSelection(self):
        clear()
        Art=text2art("Jupiter Farming Selection")
        print(Fore.MAGENTA + Art)

        questions = [
            inquirer.List('Site',
                            message="Select an option",
                            choices=['Swapping', 'Limit Order', 'DCA', 'Bridge', 'Perpetual', 'Exit'],
                        ),
            ]
        answers = inquirer.prompt(questions)

        if answers['Site'] == 'Swapping':
            from Modules.Jupiter.swap import Main as jupSwap
            jupSwap()
        elif answers['Site'] == 'Limit Order':
            self.modules()
        elif answers['Site'] == 'DCA':
            self.modules()
        elif answers['Site'] == 'Bridge':
            self.modules()
        elif answers['Site'] == 'Perpetual':
            self.modules()
        elif answers['Site'] == 'Exit':
            clear()
            print(Fore.RED + "Exiting")
            time.sleep(1)
            exit()



Main()
