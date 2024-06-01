from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/process_proposals', methods=['POST'])
def process_proposals():
    contract_address = request.json.get('contract_address')
    try:
        # Call Fluence service to fetch proposals
        proposals_result = subprocess.run(['fluence', 'run', 'fetch_proposals', contract_address], capture_output=True, text=True)
        proposals = json.loads(proposals_result.stdout)

        # Summarize proposals using Fluence service
        summaries = []
        for proposal in proposals:
            summary_result = subprocess.run(['fluence', 'run', 'summarize_proposal', proposal], capture_output=True, text=True)
            summary = summary_result.stdout.strip()
            summaries.append(summary)

        # Store summaries on Filecoin using Fluence service
        store_result = subprocess.run(['node', 'store_summaries.js', json.dumps(summaries)], capture_output=True, text=True)
        cid = store_result.stdout.strip()

        return jsonify({"summaries": summaries, "cid": cid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
