from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from classes import Pulze, DeepGram, Labs11
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

frontend = os.environ['CRUX_Frontend_URL']
backend = os.environ['CRUX_Backend_URL']

CORS(app, origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8001/upload",
    "http://127.0.0.1:8001/parse",
    "http://127.0.0.1:8001/generate",
    frontend,
    frontend + "/upload",
    frontend + "/parse",
    frontend + "/generate",
    backend,
    backend + "/upload",
    backend + "/parse",
    backend + "/generate",
])

pulze = Pulze()
deep = DeepGram()
TARGET_FILENAME = "TARGET_AUDIO.mp3"


@app.route("/", methods=["GET"])
def root():
    return jsonify(status="Crux API Active!")


@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify(detail="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(detail="No selected file"), 400

    if not file.filename.endswith(".mp3"):
        return jsonify(detail="The file is not an .mp3"), 400

    try:
        file_contents = file.read()
        filename = secure_filename(file.filename)
        with open(TARGET_FILENAME, "wb") as buffer:
            buffer.write(file_contents)
        return jsonify(filename=filename, success=True)
    except Exception as e:
        return jsonify(detail=f"Error saving file: {e}"), 400


@app.route("/parse", methods=["GET"])
def get_info():
    audience = request.args.get('audience')
    if not audience:
        return jsonify(detail="audience parameter required!"), 400

    try:
        transcription, length = deep.transcribe(TARGET_FILENAME)
        pulze.configure_initial_prompts(audience)
        feedback, new_script = pulze.generate_feedback(transcription, length)
        pulze.reset_context()
        return jsonify(feedback=feedback, newScript=new_script)
    except Exception as e:
        return jsonify(detail=f"Error processing the audience input: {e}"), 400


@app.route("/generate", methods=["POST"])
def get_mp3():
    data = request.json
    if not data.get("username"):
        return jsonify(detail="username parameter required!"), 400
    if not data.get("script"):
        return jsonify(detail="script parameter required!"), 400

    lab = Labs11(data["username"])
    location = lab.generate_custom_response(TARGET_FILENAME, data["script"])

    with open(location, 'rb') as f:
        file_data = f.read()
    
    response = Response(file_data, mimetype="audio/mpeg")
    response.headers["Content-Disposition"] = "attachment; filename=simulation.mp3"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)