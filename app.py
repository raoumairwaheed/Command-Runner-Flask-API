from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import time
import os

app = Flask(__name__)
CORS(app)

# Directory to store JSON files
OUTPUT_DIR = 'output_files'

# Ensure the output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/run_command', methods=['POST'])
def run_command():
    try:
        data = request.get_json()
        command = data.get('command', '')

        if not command:
            return jsonify({'error': 'Command not provided'}), 400

        # Generate a timestamp for the current command execution
        timestamp = int(time.time())

        # Create a unique filename based on the timestamp
        filename = os.path.join(OUTPUT_DIR, f'output_{timestamp}.json')

        # Run the command and capture the output
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = []
        while True:
            line = process.stdout.readline()
            if not line:
                break
            output.append(line.strip())

        # Store the command data in a JSON file
        with open(filename, 'w') as json_file:
            json.dump({
                'command': command,
                'output': output,
                'returncode': process.returncode
            }, json_file)

        response = {
            'output': output,
            'returncode': process.returncode,
            'filename': filename
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
