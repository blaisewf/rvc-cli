from flask import Flask, jsonify, request
from main import (
    run_infer_script,
    run_batch_infer_script,
    run_tts_script,
    run_preprocess_script,
    run_extract_script,
    run_train_script,
    run_index_script,
    run_model_information_script,
    run_model_fusion_script,
    run_tensorboard_script,
    run_download_script,
)

app = Flask(__name__)

def run_script(script_function, required_keys, **kwargs):
    try:
        data = request.json
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

        result = script_function(**data)
        return jsonify({"message": result}), 200

    except ValueError as value_error:
        return jsonify({"error": str(value_error)}), 400
    except Exception as error:
        return jsonify({"error": str(error)}), 500

# Infer
@app.route("/infer", methods=["POST"])
def infer():
    required_keys = ["f0up_key", "filter_radius", "index_rate", "hop_length", "f0method", "input_path", "output_path", "pth_file", "index_path", "split_audio"]
    return run_script(run_infer_script, required_keys)

# Batch Infer
@app.route("/batch_infer", methods=["POST"])
def batch_infer():
    required_keys = ["f0up_key", "filter_radius", "index_rate", "hop_length", "f0method", "input_folder", "output_folder", "pth_file", "index_path"]
    return run_script(run_batch_infer_script, required_keys)

# TTS
@app.route("/tts", methods=["POST"])
def tts():
    required_keys = ["tts_text", "tts_voice", "f0up_key", "filter_radius", "index_rate", "hop_length", "f0method", "output_tts_path", "output_rvc_path", "pth_file", "index_path"]
    return run_script(run_tts_script, required_keys)

# Preprocess
@app.route("/preprocess", methods=["POST"])
def preprocess():
    required_keys = ["model_name", "dataset_path", "sampling_rate"]
    return run_script(run_preprocess_script, required_keys)

# Extract
@app.route("/extract", methods=["POST"])
def extract():
    required_keys = ["model_name", "rvc_version", "f0method", "hop_length", "sampling_rate"]
    return run_script(run_extract_script, required_keys)

# Train
@app.route("/train", methods=["POST"])
def train():
    required_keys = ["model_name", "rvc_version", "save_every_epoch", "save_only_latest", "save_every_weights", "total_epoch", "sampling_rate", "batch_size", "gpu", "pitch_guidance", "pretrained", "custom_pretrained", "g_pretrained_path", "d_pretrained_path"]
    return run_script(run_train_script, required_keys)

# Index
@app.route("/index", methods=["POST"])
def index():
    required_keys = ["model_name", "rvc_version"]
    return run_script(run_index_script, required_keys)

# Model Information
@app.route("/model_information", methods=["POST"])
def model_information():
    required_keys = ["pth_path"]
    return run_script(run_model_information_script, required_keys)

# Model Fusion
@app.route("/model_fusion", methods=["POST"])
def model_fusion():
    required_keys = ["model_name", "pth_path_1", "pth_path_2"]
    return run_script(run_model_fusion_script, required_keys)

# Tensorboard
@app.route("/tensorboard", methods=["GET"])
def tensorboard():
    return run_script(run_tensorboard_script, [])

# Download
@app.route("/download", methods=["POST"])
def download():
    required_keys = ["model_link"]
    return run_script(run_download_script, required_keys)

if __name__ == "__main__":
    app.run()
