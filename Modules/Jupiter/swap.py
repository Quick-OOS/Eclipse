# import requests
# from solana.rpc.api import Client
# from solana.transaction import VersionedTransaction
# import base64

import inquirer,subprocess,os,json,time,requests, base64, base58
from art import *
from colorama import init, Fore
init(autoreset=True)
clear = lambda: os.system('cls')
from pypresence import Presence
from cryptography.fernet import Fernet
import inquirer, subprocess, os, json, time, requests, base64
from art import *
from colorama import init, Fore
from pypresence import Presence
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.padding import (
    PSS,
    MGF1,
)
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend

from solathon.core.instructions import transfer
from solathon import Client, Transaction, PublicKey, Keypair

from solathon.core.instructions import transfer
from solathon import Client, Transaction, PublicKey, Keypair

class Main:

    def sign_transaction(self, private_key_bytes, transaction_data):
        private_key = ec.derive_private_key(int.from_bytes(private_key_bytes, "big"), ec.SECP256K1(), default_backend())
        signature = private_key.sign(transaction_data, ec.ECDSA(hashes.SHA256()))
        return signature

    def __init__(self):

        self.success = 0
        self.errors = 0

        clear()
        Art=text2art("Jupiter Swap")
        print(Fore.MAGENTA + Art)

        #Load wallets
        file_path = 'wallets.txt'

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.line_count = len(lines)
                if self.line_count == 0:
                    print(Fore.RED + "No wallets found - Add wallets or generate wallets from the modules section")
                    input("Press enter to return to the main menu: ")
                else:
                    print(Fore.GREEN + f"Found {self.line_count} wallets")
                    input("Press enter to continue")
                                   
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        #Ask user which token they want to swap

        self.tokenChoice = input("Which token would you like to swap? (SOL is currently the only token you can swap): ")

        if self.tokenChoice == "SOL" or "sol":
            print(Fore.GREEN + "SOL Selected")
            #Ask user to input the amount they want to swap
            self.tokenAmount = input(f"Enter the amount of {self.tokenChoice} you would like to swap: ")
            #Check a valid amount has been added
            if self.tokenAmount == "":
                print(Fore.RED + f"Enter a valid amount of {self.tokenChoice}")
            else:
                #Ask user to input slippage fee
                self.lomens = self.tokenAmount * 100000000
                self.slippageFee = input("Enter a slippage fee: ")
                #Check if a fee has been inputted
                if self.slippageFee == "":
                    print(Fore.RED + "Enter a valid slippage fee")
                else:
                    #Last confirmation before bot runs its tasks - User confirmation
                    delays = input("Do you want to set custom delays in between swaps or use the bots delays: (Y/N): ")
                    if delays == "Y" or "y":
                        self.retryDelay = input("Enter a delay in seconds: ")
                        input(Fore.YELLOW + f"Press enter to swap {self.tokenChoice} {self.tokenAmount} on {self.line_count} wallets: ")
                        self.getQuote()
                    elif delays == "N" or "n":
                        print("Continuing with bots hard coded delays")
                        self.getQuote()
        else:
            print(Fore.RED + "Please enter a valid token")

    def getQuote(self):

        os.system(f"title Jupiter Swap - Wallets loaded {self.line_count} - Swaps: {self.success} - Errors: {self.errors} - Quick#0077")

        print(f"[" + time.strftime("%H:%M:%S") + f"] " + f"[INFO]" +" Getting swap quote...")

        params = {
            'inputMint': 'So11111111111111111111111111111111111111112',
            'outputMint': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
            'amount': '10000',
            'slippageBps': self.slippageFee
        }

        try:
            quote_response = requests.get('https://quote-api.jup.ag/v6/quote', params=params)
            
            if quote_response.status_code == 200:
                print(Fore.GREEN + f"[" + time.strftime("%H:%M:%S") + f"] " + f"[{quote_response.status_code}]" +" Received swap quote")
                self.quote_data = quote_response.json()  # Parse JSON response
                self.postSwap()
            else:
                print(Fore.RED + f"[" + time.strftime("%H:%M:%S") + f"] " + f"[{quote_response.status_code}]" +" Error retrieving swap quote - Retrying...")
                #print(quote_response.json())
                time.sleep(1)
                self.getQuote()
                print(quote_response.json())
        except Exception as e:
            print(f"Error: {e}")

    def postSwap(self, retries=0):
        retries += 1

        print(f"[{time.strftime('%H:%M:%S')}] [INFO] Posting to swap API...")
        self.privKey = "H94aoxMBWY7dB6urKb1jG5pe93E7c1LNXZFZz6GEShCtc5jrMjm4HyyQ8ibSpjoHm64uQ7xtaws1QPycHDZnJ3u"

        try:
            payload = {
                "quoteResponse": self.quote_data,
                "userPublicKey": 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',  # Assuming publicKey is the required format
                "wrapAndUnwrapSol": True,
                # If feeAccount is needed, include it in the payload
                # "feeAccount": "fee_account_public_key"
            }

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post('https://quote-api.jup.ag/v6/swap', json=payload, headers=headers)

            if response.status_code == 200:
                self.swapTransaction = response.json().get('swapTransaction')
                print(Fore.GREEN + f"[" + time.strftime("%H:%M:%S") + f"] " + f"[{response.status_code}]" +" Posted quote data to swap API")
                self.deserializeSwap()
                # Process swapTransaction data as needed
                #print(swapTransaction)
            else:
                print(Fore.RED + f"[{time.strftime('%H:%M:%S')}] [{response.status_code}] Error posting to swap API. Retrying... {retries}/3")
                if retries >= 3:
                    print(Fore.RED + f"[{time.strftime('%H:%M:%S')}] [{response.status_code}] Maximum retries reached. Retrying from quote API...")
                    self.getQuote()
                else:
                    time.sleep(1)
                    self.postSwap(retries)
        except Exception as e:
            print(e)

    def deserializeSwap(self):
        print(f"[{time.strftime('%H:%M:%S')}] [INFO] Deserializing the transaction...")

        try:
            #decoded_tx = base58.b58decode(bytes(self.swapTransaction, 'utf-8'))

            #transaction = Transaction.deserialize(decoded_tx)

            #print(transaction.compile_message())
            self.serialized_transaction_bytes = base64.b64decode(self.swapTransaction)
            print(Fore.GREEN + f"[" + time.strftime("%H:%M:%S") + f"] " + f"[SUCCESS]" +" Transaction Deserialized")
            print(f"[{time.strftime('%H:%M:%S')}] [INFO] Signing Transaction...")
            self.signTransaction()

            # Further processing or handling of the signed transaction here
        except Exception as e:
            print(f"Error occurred during deserialization: {e}")

    def signTransaction(self):
        #private_key_str = "H94aoxMBWY7dB6urKb1jG5pe93E7c1LNXZFZz6GEShCtc5jrMjm4HyyQ8ibSpjoHm64uQ7xtaws1QPycHDZnJ3u"
        ##signature = self.sign_transaction(private_key_bytes, self.serialized_transaction_bytes)
        #print(f"Signature: {signature.hex()}")
        client = Client("https://api.devnet.solana.com")
        result = client.send_transaction(self.swapTransaction)
        print("Transaction result: ", result)


Main()
# # Predefined private key (replace this with your private key)
# private_key_str = "YOUR_PRIVATE_KEY_HERE"
# private_key_bytes = base64.b64decode(private_key_str)

# # Define the parameters for /quote API
# params = {
#     'inputMint': 'So11111111111111111111111111111111111111112',
#     'outputMint': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
#     'amount': '100000000',
#     'slippageBps': '50'
# }

# # Perform the request to /quote API
# quote_response = requests.get('https://quote-api.jup.ag/v6/quote', params=params).json()

# # Define the payload for /swap API
# payload = {
#     'quoteResponse': quote_response,
#     'userPublicKey': private_key_str,  # Using private key directly
#     'wrapAndUnwrapSol': True,
#     # 'feeAccount': "fee_account_public_key"  # Include fee account if needed
# }

# # Define headers for /swap API
# headers = {
#     'Content-Type': 'application/json'
# }

# # Perform the request to /swap API
# swap_transaction = requests.post('https://quote-api.jup.ag/v6/swap', json=payload, headers=headers).json()

# # Deserialize the swap transaction from base64
# swap_transaction_bytes = base64.b64decode(swap_transaction)
# transaction = VersionedTransaction.deserialize(swap_transaction_bytes)

# # Create an account object from the private key
# wallet = Account(private_key_bytes)

# # Sign the transaction
# transaction.sign([wallet.payer])

# # Serialize the signed transaction
# raw_transaction = transaction.serialize()

# # Connect to Solana network
# solana_network_url = 'https://api.mainnet-beta.solana.com'  # Replace with the desired Solana network
# connection = Client(solana_network_url)

# # Send raw transaction
# txid = connection.send_raw_transaction(raw_transaction, opts={"skipPreflight": True, "maxRetries": 2})

# # Confirm transaction
# confirmation = connection.confirm_transaction(txid)

# # Print transaction ID and SolScan URL
# print(f"Transaction ID: {txid}")
# print(f"SolScan URL: https://solscan.io/tx/{txid}")

