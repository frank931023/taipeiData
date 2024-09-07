from flask import Flask, jsonify
import json
import subprocess
import threading

app = Flask(__name__)

def start_crawler():
    subprocess.Popen(['python', 'crawler.py'])

@app.route('/fetch', methods=['GET'])
def fetch_route():
    try:
        with open('coordinate.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

if __name__ == '__main__':
    # Start crawer in a separate thread
    threading.Thread(target=start_crawler).start()
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000)
