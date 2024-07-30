from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

# Array to store data
data_store = []

@app.route('/sensor/data', methods=['POST'])
def save_data():
    # Get data from request
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data received"}), 400
    
    # Store data in array
    data_store.append(data)
    
    return jsonify({"message": "Data successfully saved", "data": data}), 201

@app.route('/sensor/data', methods=['GET'])
def get_data():
    return jsonify(data_store), 200

if __name__ == '__main__':
    # Get the device hostname
    hostname = socket.gethostname()
    # Get the local IP address of the device
    local_ip = socket.gethostbyname(hostname)
    
    print(f"Server running at: http://{local_ip}:5000 and http://127.0.0.1:5000")
    
    # Run the server on all network interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)