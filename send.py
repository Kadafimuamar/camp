import random
import string
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
import os
import json


# Load file .env
load_dotenv()

# Load ABI
with open("./abi/token.json") as f:
    ABI = json.load(f)

# Konfigurasi awal
RPC = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("WALLET_ADDRESS")
TOKEN_CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
TOKEN_DECIMALS = 18  # Sesuaikan jika berbeda
TOKEN_AMOUNT = 0.1  # Jumlah token per wallet

# Koneksi ke jaringan
w3 = Web3(Web3.HTTPProvider(RPC))
contract = w3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=ABI)

print("Connected:", w3.isConnected())

# Fungsi untuk generate wallet acak (valid checksum address)
def generate_random_wallet():
    return Account.create().address

# Kirim token ke wallet acak sebanyak 1000x
def send_to_random_wallets(count):
    nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

    for i in range(count):
        to_address = generate_random_wallet()
        amount = int(TOKEN_AMOUNT * (10 ** TOKEN_DECIMALS))
        tx = contract.functions.transfer(to_address, amount).buildTransaction({
            'chainId': w3.eth.chain_id,
            'gas': 100_000,
            'gasPrice': w3.toWei('10', 'gwei'),
            'nonce': nonce + i,
            'from': ACCOUNT_ADDRESS
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[{i+1}/1000] Sent {TOKEN_AMOUNT} token to {to_address} | tx: {tx_hash.hex()}")

# Jalankan
send_to_random_wallets(1000)
