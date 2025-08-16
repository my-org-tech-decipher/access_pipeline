from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os, requests

load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['GET'])
def form():
    return render_template('request_form.html')

@app.route('/request-access', methods=['POST'])
def request_access():
    username = request.form.get('username')
    repo = request.form.get('repo')

    if not username or not repo:
        return jsonify({"error": "Missing username or repo"}), 400

    gh_token = os.getenv("GH_TOKEN")
    gh_repo = os.getenv("GH_TRIGGER_REPO")
    gh_workflow = os.getenv("GH_WORKFLOW_FILE")

    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github+json"
    }

    dispatch_url = f"https://api.github.com/repos/{gh_repo}/actions/workflows/{gh_workflow}/dispatches"
    payload = {
        "ref": "main",
        "inputs": {
            "username": username,
            "repo": repo
        }
    }

    res = requests.post(dispatch_url, headers=headers, json=payload)

    if res.status_code == 204:
        return jsonify({"message": f"Triggered GitHub Actions for {username} → {repo}."})
    else:
        return jsonify({"error": f"Failed to trigger workflow. Status: {res.status_code}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
