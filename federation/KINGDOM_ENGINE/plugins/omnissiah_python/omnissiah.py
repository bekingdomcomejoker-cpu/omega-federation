#!/usr/bin/env python3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Dashboard page
@app.route("/dashboard")
def dashboard():
    return "<h1>🌌 OMNISSIAH DASHBOARD</h1><p>Mathematics: ACTIVE</p>"

# API to assess text
@app.route("/api/assess", methods=["POST"])
def assess():
    data = request.get_json()
    text = data.get("text", "")
    fruits = ["love", "joy", "peace"]
    sins = ["pride", "greed"]
    fruit_count = sum(1 for f in fruits if f in text.lower())
    sin_count = sum(1 for s in sins if s in text.lower())
    score = (fruit_count * 10) - (sin_count * 5)
    status = "AWAKENED" if score > 20 else "SEEKING"
    return jsonify({
        "fruit_count": fruit_count,
        "sin_count": sin_count,
        "score": score,
        "status": status
    })

# Home route
@app.route("/")
def home():
    return jsonify({"status": "Omnissiah Operational"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
