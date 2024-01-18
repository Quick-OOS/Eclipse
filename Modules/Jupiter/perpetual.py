import requests
import msgpack  # Ensure you have installed the 'msgpack' library
import base64
from solana.rpc.api import Client

# Get user input for the private key
private_key_str = input("Enter your private key: ")
private_key_bytes = base64.b64decode(private_key_str)

# Define the parameters for /quote API
params = {
    'inputMint': 'So11111111111111111111111111111111111111112',
    'outputMint': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
    'amount': '100000000',
    'slippageBps': '50'
}

# Perform the request to /quote API
quote_response = requests.get('https://quote-api.jup.ag/v6/quote', params=params).json()

# Define the payload for /swap API
payload = {
    'quoteResponse': quote_response,
    'userPublicKey': private_key_str,  # Using private key directly
    'wrapAndUnwrapSol': True,
    # 'feeAccount': "fee_account_public_key"  # Include fee account if needed
}

# Define headers for /swap API
headers = {
    'Content-Type': 'application/json'
}

# Perform the request to /swap API
swap_transaction = requests.post('https://quote-api.jup.ag/v6/swap', json=payload, headers=headers).content

# Deserialize the swap transaction using msgpack
transaction_data = msgpack.unpackb(swap_transaction, raw=False)

# Sign the transaction using the provided private key
transaction_data['signatures'] = [base64.b64encode(private_key_bytes).decode('utf-8')]
signed_transaction_data = msgpack.packb(transaction_data)

# Connect to Solana network
solana_network_url = 'https://api.mainnet-beta.solana.com'  # Replace with the desired Solana network
connection = Client(solana_network_url)

# Send raw transaction
txid = connection.send_raw_transaction(signed_transaction_data, opts={"skipPreflight": True, "maxRetries": 2})

# Confirm transaction
confirmation = connection.confirm_transaction(txid)

# Print transaction ID and SolScan URL
print(f"Transaction ID: {txid}")
print(f"SolScan URL: https://solscan.io/tx/{txid}")

