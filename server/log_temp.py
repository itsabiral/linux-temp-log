from flask import Flask, request, jsonify
import json
import os
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "temp_log.jsonl"

def read_log():
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        file_path.touch()

    with open(file_path, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def write_log(log_data):
    with open(file_path, "w") as f:
        for item in log_data:
            f.write(json.dumps(item) + "\n")

@app.route('/temperature', methods=['POST'])
def log_temperature():
    data = request.get_json(force=True) or {}
    
    for k in ("server", "temperature", "updated_at"):
        if k not in data:
            return jsonify({"error": f"Missing field!! {k}"}), 400

    log_data = read_log()

    for item in log_data:
        if item.get('server') == data['server']:
            item['temperature'] = data['temperature']
            item['updated_at'] = data['updated_at']
            break
    else:
        log_data.append({
            'server': data['server'],
            'temperature': data['temperature'],
            'updated_at': data['updated_at']
        })

    write_log(log_data)
    return jsonify({'message': 'Logged!'}), 200

@app.route('/temperature', methods=['GET'])
def get_temperature():
    server = request.args.get('server')
    log_data = read_log()

    if server:
        for item in log_data:
            if item.get('server') == server:
                return jsonify(item), 200
        return jsonify({'message': 'Server not found'}), 404

    return jsonify(log_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
