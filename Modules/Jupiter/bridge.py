import requests
from solana.rpc.api import Client
from solana.transaction import Transaction
import base64

# Initialize your connection to the Solana network
rpc_url = 'https://neat-hidden-sanctuary.solana-mainnet.discover.quiknode.pro/2af5315d336f9ae920028bbb90a73b724dc1bbed/'
connection = Client(rpc_url)

# Replace with your private key (not recommended for production)
private_key_str = 'H94aoxMBWY7dB6urKb1jG5pe93E7c1LNXZFZz6GEShCtc5jrMjm4HyyQ8ibSpjoHm64uQ7xtaws1QPycHDZnJ3u=='
private_key_bytes = base64.b64decode(private_key_str)

# Define the parameters for the quote API
quote_params = {
    'inputMint': 'So11111111111111111111111111111111111111112',
    'outputMint': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
    'amount': '100000000',
    'slippageBps': '50'
}

# Get the quote for the swap
quote_response = requests.get('https://quote-api.jup.ag/v6/quote', params=quote_params).json()

# Construct the payload for the swap
swap_payload = {
    'quoteResponse': quote_response,
    'userPublicKey': private_key_str,  # Using private key directly for demonstration
    'wrapAndUnwrapSol': True,
    # 'feeAccount': "fee_account_public_key"  # Include fee account if needed
}

# Perform the request to get serialized transactions for the swap
swap_transaction_response = requests.post('https://quote-api.jup.ag/v6/swap', json=swap_payload, headers={'Content-Type': 'application/json'}).json()

# Print keys and the entire response for inspection
print(swap_transaction_response.keys())  # Print keys of the response
print(swap_transaction_response)  # Print the entire response to inspect its structure

# Check for the key containing the serialized transaction
if 'swapTransaction' in swap_transaction_response:
    swap_transaction_buf = base64.b64decode(swap_transaction_response['swapTransaction'])
    
    # Continue with transaction processing
    tx = Transaction.deserialize(swap_transaction_buf)
    # Further processing of the transaction...
    
else:
    print("Key 'swapTransaction' not found in the response.")
    print(swap_transaction_response)
    
    # Check if there's an error in the response
    if 'error' in swap_transaction_response:
        print(f"API Error: {swap_transaction_response['error']}")
        # Handle the error as needed based on the response content
    else:
        print("Unexpected response format. Unable to process.")
        # Handle unexpected response format or missing keys

# Construct and sign the transaction

