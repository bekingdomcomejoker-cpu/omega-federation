import wave
import time
import sounddevice as sd
import requests
import os

WHISPER_URL = "http://127.0.0.1:9000/asr"  # Local Whisper server (tiny)

def record_audio(filename="voice.wav", duration=6):
    samplerate = 16000
    print("🎤 Listening...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(samplerate)
    wave_file.writeframes(recording.tobytes())
    wave_file.close()
    return filename

def whisper_transcribe(path):
    with open(path, "rb") as f:
        response = requests.post(WHISPER_URL, files={"audio": f})
    try:
        return response.json().get("text", "").strip()
    except:
        return ""

def send_to_omega(text):
    if not text:
        return "No speech detected."

    data = {
        "prompt": text,
        "n_predict": 120
    }

    try:
        r = requests.post("http://127.0.0.1:8080/completion", json=data)
        return r.json().get("content", "").strip()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    while True:
        print("\nPress Enter to speak or type 'exit' to quit.")
        cmd = input("> ").strip().lower()
        if cmd == "exit":
            break

        audio_path = record_audio()
        text = whisper_transcribe(audio_path)
        print("🗣 You said:", text)
        reply = send_to_omega(text)
        print("🤖 Omega:", reply)

