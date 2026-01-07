import subprocess, sys, json, os
from pathlib import Path

MODEL = os.environ.get("LLM_MODEL")
LLAMA = os.environ.get("LLAMA_BIN")

def run_llm(prompt: str):
    if not Path(MODEL).exists():
        return {"status": "ERROR", "error": f"Model not found: {MODEL}"}
    if not Path(LLAMA).exists():
        return {"status": "ERROR", "error": f"Binary not found: {LLAMA}"}

    try:
        cmd = [
            LLAMA, "-m", MODEL,
            "-p", prompt,
            "-n", "200"
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
        return {"status": "OK", "response": output}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "FAIL", "error": "NO_PROMPT"}))
        sys.exit(1)

    prompt = sys.argv[1]
    print(json.dumps(run_llm(prompt)))
