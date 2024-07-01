from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

servers = [
    {"url": "http://localhost:5001/status"},
    {"url": "http://localhost:5002/status"},
    {"url": "http://localhost:5003/status"}
]

def get_server_status():
    server_statuses = []
    for server in servers:
        response = requests.get(server['url'])
        if response.status_code == 200:
            status = response.json()
            server_statuses.append(status)
    return server_statuses

def get_effective_response_time(server):
    if server['current_connections'] >= server['capacity']:
        return float('inf')
    return server['response_time']

@app.route('/process', methods=['POST'])
def load_balance():
    data = request.json.get('data')
    
    server_statuses = get_server_status()
    if not server_statuses:
        return jsonify({"status": "error", "message": "Unable to fetch server statuses"}), 503

    # Select server with least response time that is not at full capacity
    selected_server = min(server_statuses, key=lambda s: (get_effective_response_time(s), s['current_connections'] / s['capacity']))
    
    if selected_server['current_connections'] < selected_server['capacity']:
        process_url = f"http://localhost:500{selected_server['server']}/process"
        response = requests.post(process_url, json={"data": data})
        if response.status_code == 200:
            return jsonify(response.json()), response.status_code
        else:
            return jsonify({"status": "error", "message": "Failed to process request"}), 503
    else:
        return jsonify({"status": "error", "message": "All servers are full"}), 503

if __name__ == '__main__':
    app.run(port=5000)