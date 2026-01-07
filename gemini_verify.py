import os, requests, json, sys

API_KEY = os.environ["GEMINI_API_KEY"]
TEXT = sys.stdin.read()

payload = {
  "contents": [{
    "role": "user",
    "parts": [{"text": TEXT}]
  }],
  "generationConfig": {
    "temperature": 0.0,
    "topK": 1,
    "maxOutputTokens": 512
  }
}

r = requests.post(
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
  params={"key": API_KEY},
  headers={"Content-Type": "application/json"},
  data=json.dumps(payload)
)

print(r.json())
