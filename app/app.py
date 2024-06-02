from flask import Flask, request, jsonify
import subprocess
import json
import os
from fetch import fetch_contract_bytecode
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

app = Flask(__name__)

@app.route('/process_proposals', methods=['POST'])
def process_proposals():
    contract_address = request.json.get('contract_address')
    try:
        # Fetch the contract bytecode using Etherscan
        bytecode = fetch_contract_bytecode(contract_address)
        
        # Call Fluence service to summarize the bytecode
        summary_result = subprocess.run(['fluence', 'run', 'summarize_proposal', bytecode], capture_output=True, text=True)
        summary = summary_result.stdout.strip()
        
        # Store the summary on Filecoin using JavaScript script
        store_result = subprocess.run(['node', '../Storage/store.js', json.dumps([summary])], capture_output=True, text=True)
        cid = store_result.stdout.strip()

        return jsonify({"summary": summary, "cid": cid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


# This will act as the API to do the process of running Fluence service and storing the processed data on Filecoin.