from nacl.signing import SigningKey
import base58, os, time
from colorama import init, Fore

class Main:

    def generate_keypair():
        # Generate a signing key
        signing_key = SigningKey.generate()
        
        # Extract the verifying key (public key)
        verifying_key = signing_key.verify_key
        
        # Encode keys in base58 for Solana
        encoded_public_key = base58.b58encode(verifying_key.encode())
        encoded_private_key = base58.b58encode(signing_key.encode())
        
        return encoded_public_key.decode(), encoded_private_key.decode()

    def save_to_file(public_key, private_key, wallet_number):
        with open('Data/wallets.txt', 'a') as file:
            file.write(f"Wallet {wallet_number}:\nWallet Address: {public_key}\nPrivate Key: {private_key}\n\n")

    # Ask the user how many wallets they want to generate
    num_wallets = int(input("Enter the number of wallets to generate: "))

    for i in range(1, num_wallets + 1):
        # Generate a Solana keypair
        public_key, private_key = generate_keypair()
        
        # Save the keys to a file
        save_to_file(public_key, private_key, i)
        
        # Display success message
        print(Fore.GREEN + f"[" + time.strftime("%H:%M:%S") + f"] [{i}] Successfully created wallet")
        os.system(f"title Eclipse - Wallets Generated: {i}/{num_wallets} - Quick#0077")

Main()

