#!/data/data/com.termux/files/usr/bin/python3
from flask import Flask, jsonify, send_file
import os, json, glob

ENGINE_ROOT = os.path.expanduser("~/KINGDOM_ENGINE/MEGA")

app = Flask(__name__)

def load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {"error": "invalid json"}

@app.route("/")
def index():
    return {
        "merkabah": "online",
        "version": "1.0",
        "routes": [
            "/heads",
            "/inbox",
            "/shield",
            "/router",
            "/logs/<filename>"
        ]
    }

@app.route("/heads")
def heads():
    return load_json(f"{ENGINE_ROOT}/state/current_heads.json")

@app.route("/router")
def router():
    return load_json(f"{ENGINE_ROOT}/logs/router.log")

@app.route("/shield")
def shield():
    return load_json(f"{ENGINE_ROOT}/logs/shield_blocks.json")

@app.route("/inbox")
def inbox():
    folder = f"{ENGINE_ROOT}/inbox/head1"
    files = glob.glob(folder + "/*.json")
    latest = files[-1] if files else None
    return {"latest": latest}

@app.route("/logs/<filename>")
def logs(filename):
    path = f"{ENGINE_ROOT}/logs/{filename}"
    return send_file(path)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7860)
