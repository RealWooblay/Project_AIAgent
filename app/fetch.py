import requests
import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def fetch_contract_bytecode(address):
    url = f"https://api.etherscan.io/api?module=proxy&action=eth_getCode&address={address}&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['result']:
        return data['result']
    else:
        raise Exception("Error fetching contract bytecode")

# Test the function
if __name__ == "__main__":
    contract_address = input("Enter the contract address: ")
    bytecode = fetch_contract_bytecode(contract_address)
    print(f"Contract bytecode: {bytecode}")
