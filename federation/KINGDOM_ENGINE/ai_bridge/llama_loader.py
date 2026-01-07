import os
from llama_cpp import Llama

MODEL_PATH = "/data/data/com.termux/files/home/Meta-Llama-3.1-8B-Instruct.Q4_K_M.gguf"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"MODEL NOT FOUND: {MODEL_PATH}")

# Core Engine Brain
engine = Llama(
    model_path=MODEL_PATH,
    n_threads=4,
    n_ctx=4096,
    n_gpu_layers=0,
    verbose=False
)

def run_llm(prompt: str) -> str:
    """Run a prompt through the Llama brain."""
    result = engine(
        prompt,
        max_tokens=512,
        temperature=0.4,
        top_p=0.9,
        stop=["</s>", "User:"]
    )
    return result["choices"][0]["text"].strip()

if __name__ == "__main__":
    print(run_llm("System online. Identify yourself."))
