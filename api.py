from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


# Infer
@app.route("/infer", methods=["POST"])
def infer():
    command = ["python", "main.py", "infer"] + request.json.get("args", [])
    return execute_command(command)


# Batch Infer
@app.route("/batch_infer", methods=["POST"])
def batch_infer():
    command = ["python", "main.py", "batch_infer"] + request.json.get("args", [])
    return execute_command(command)


# TTS
@app.route("/tts", methods=["POST"])
def tts():
    command = ["python", "main.py", "tts"] + request.json.get("args", [])
    return execute_command(command)


# Preprocess
@app.route("/preprocess", methods=["POST"])
def preprocess():
    command = ["python", "main.py", "preprocess"] + request.json.get("args", [])
    return execute_command(command)


# Extract
@app.route("/extract", methods=["POST"])
def extract():
    command = ["python", "main.py", "extract"] + request.json.get("args", [])
    return execute_command(command)


# Train
@app.route("/train", methods=["POST"])
def train():
    command = ["python", "main.py", "train"] + request.json.get("args", [])
    return execute_command(command)


# Index
@app.route("/index", methods=["POST"])
def index():
    command = ["python", "main.py", "index"] + request.json.get("args", [])
    return execute_command(command)


# Model Information
@app.route("/model_information", methods=["POST"])
def model_information():
    command = ["python", "main.py", "model_information"] + request.json.get("args", [])
    return execute_command(command)


# Model Fusion
@app.route("/model_fusion", methods=["POST"])
def model_fusion():
    command = ["python", "main.py", "model_fusion"] + request.json.get("args", [])
    return execute_command(command)


# Tensorboard
@app.route("/tensorboard", methods=["GET"])
def tensorboard():
    command = ["python", "main.py", "tensorboard"]
    return execute_command(command)


# Download
@app.route("/download", methods=["POST"])
def download():
    command = ["python", "main.py", "download"] + request.json.get("args", [])
    return execute_command(command)


def execute_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return jsonify({"output": result.stdout, "error": result.stderr}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
