from flask import Flask, request, jsonify

app = Flask(__name__)

current_connections = 151
capacity = 150
response_time = 30
data_processing_history = []

@app.route('/process', methods=['POST'])
def process_request():
    global current_connections
    data = request.json.get('data')
    
    if current_connections < capacity:
        current_connections += 1
        data_processing_history.append(data)
        return jsonify({"status": "success", "server": 2, "current_connections": current_connections}), 200
    else:
        return jsonify({"status": "error", "message": "Server is full"}), 503

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "server": 2,
        "capacity": capacity,
        "response_time": response_time,
        "current_connections": current_connections
    }), 200

if __name__ == '__main__':
    app.run(port=5002)