import base58
import requests
from solana.blockhash import Blockhash
from solana.publickey import PublicKey
from solana.transaction import Transaction

# Replace these values with your actual private keys
private_key = "YOUR_PRIVATE_KEY_HERE"
referral_private_key = "YOUR_REFERRAL_PRIVATE_KEY_HERE"

# Base key to generate a unique order id
base = PublicKey(base58.b58encode(b'base_key'))

# RPC endpoint
rpc_endpoint = "https://neat-hidden-sanctuary.solana-mainnet.discover.quiknode.pro/2af5315d336f9ae920028bbb90a73b724dc1bbed/"

# Wallet and Referral keys
wallet = base58.b58decode(private_key)
referral = base58.b58decode(referral_private_key)

# Create the transaction payload
payload = {
    "owner": str(PublicKey(wallet)),
    "inAmount": 100000,
    "outAmount": 100000,
    "inputMint": "INPUT_MINT_PUBLIC_KEY_HERE",
    "outputMint": "OUTPUT_MINT_PUBLIC_KEY_HERE",
    "expiredAt": None,
    "base": str(base),
    "referralAccount": str(PublicKey(referral)),
    "referralName": "Referral Name"
}

# Make the API request
response = requests.post('https://jup.ag/api/limit/v1/createOrder', json=payload, headers={'Content-Type': 'application/json'})
transactions = response.json()
tx = transactions['tx']

# Deserialize the transaction
transaction = Transaction(base58.b58decode(tx.encode('utf-8')))

# Sign the transaction
transaction.sign([wallet, base])

# Execute the transaction
raw_transaction = transaction.serialize()
response = requests.post(f"{rpc_endpoint}/v1/tx", json={"tx": raw_transaction})
txid = response.json()['result']
print(f"https://solscan.io/tx/{txid}")
