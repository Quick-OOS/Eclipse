import requests, json
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
    'amount': '10000000',
    'slippageBps': '100'
}

# Perform the request to /quote API
quote_response = requests.get('https://quote-api.jup.ag/v6/quote', params=params).json()

# Define the payload for /swap API
payload2 = {
    'quoteResponse': quote_response,
    'userPublicKey': private_key_str,  # Using private key directly
    'wrapAndUnwrapSol': True,
    # 'feeAccount': "fee_account_public_key"  # Include fee account if needed
}

# Define headers for /swap API
headers2 = {
    'Content-Type': 'application/json'
}

print("Payload content:")
print(json.dumps(payload2, indent=4))  # Display payload content for inspection

# Perform the request to /swap API
swap_transaction_response = requests.post('https://quote-api.jup.ag/v6/swap', json=payload2, headers=headers2)

if swap_transaction_response.status_code != 200:
    print(f"Error: HTTP {swap_transaction_response.status_code} - {swap_transaction_response.content}")
    # Handle the error response here, if needed

else:
    swap_transaction_content = swap_transaction_response.content  # Extract content from the response
    # Process the content or continue with necessary steps, for example:
    transaction_data = msgpack.unpackb(swap_transaction_content, raw=False)
    # Further process the deserialized data or continue with the necessary steps