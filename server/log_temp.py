from flask import Flask, request, jsonify
import json

app = Flask(__name__)

file_name = "temp_log.jsonl"

@app.route('/temperature', methods=['POST'])
def log_temperature():
    data = request.get_json()

    with open(file_name, 'r') as f:
        log_data = [json.loads(line) for line in f if line.strip()]
        
    for item in log_data:
        if item['server'] == data['server']:
            item['temperature'] = data['temperature']
            item['updated_at'] = data['updated_at']
            break
    else:
        log_data.append({'server': data['server'], 'temperature': data['temperature'], 'updated_at': data['updated_at']})
        
    with open(file_name, 'w') as f:
        for item in log_data:
            f.write(json.dumps(item) + '\n')
    return jsonify({'message': 'Logged!'}), 200

@app.route('/temperature', methods=['GET'])
def get_temperature():
    server = request.args.get('server')
    if server:
        with open(file_name, 'r') as f:
            log_data = [json.loads(line) for line in f if line.strip()]
        for item in log_data:
            if item['server'] == server:
                return jsonify(item), 200
        return jsonify({'message': 'Server not found'}), 404
    else:
        with open(file_name, 'r') as f:
            return jsonify([json.loads(line) for line in f if line.strip()]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)