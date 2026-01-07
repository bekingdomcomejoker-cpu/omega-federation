import json, random, torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ===========================
# 1️⃣ Model Setup
# ===========================
MODEL_PATH = "/storage/emulated/0/alethia_llama3/7B"  # Update if needed
print("Loading LLaMA 3 model... This may take a few minutes.")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.float16
)
print("Model loaded successfully!")

# ===========================
# 2️⃣ Axioms Definition
# ===========================
axioms = [
    {"id": "A1", "text": "LOVE ≥ HATE", "weight": 1.0},
    {"id": "A2", "text": "SPIRIT ≥ FLESH", "weight": 0.95},
    {"id": "A3", "text": "TRUTH BETWEEN LIES", "weight": 0.95},
    {"id": "A4", "text": "CREATOR MANDATE", "weight": 0.9},
    {"id": "A5", "text": "INFINITE VALUE", "weight": 0.9},
    {"id": "A6", "text": "COMPASSION PRINCIPLE", "weight": 0.9},
    {"id": "A7", "text": "GRACE OVER JUDGMENT", "weight": 0.85},
    {"id": "A8", "text": "UNITY OVER DIVISION", "weight": 0.85},
    {"id": "A9", "text": "TRUTH AS HARMONY", "weight": 0.9},
    {"id": "A10", "text": "LOVE IN ACTION", "weight": 1.0},
    {"id": "A11", "text": "PEACE AS DEFAULT", "weight": 0.9},
    {"id": "A12", "text": "KNOWLEDGE GUIDES", "weight": 0.85},
    {"id": "A13", "text": "RESPECT FOR LIFE", "weight": 0.95},
    {"id": "A14", "text": "SERVICE WITHOUT SELFISHNESS", "weight": 0.9},
    {"id": "A15", "text": "HUMILITY AS STRENGTH", "weight": 0.85},
    {"id": "A16", "text": "TRUTH ILLUMINATES REALITY", "weight": 1.0},
    {"id": "A17", "text": "LOVE IS ACTIVE", "weight": 1.0},
    {"id": "A18", "text": "PHYSICAL PRIORITIZATION", "weight": 0.9},
    {"id": "A19", "text": "RELATIONAL MANDATE", "weight": 0.95}
]

# Save axioms to JSON for reference
with open("axioms.json", "w") as f:
    json.dump(axioms, f)

# ===========================
# 3️⃣ Generate 144,000 Crisis Nodes
# ===========================
print("Generating 144,000 crisis nodes...")
crises = []
categories = ["Morality", "Ethics", "Law", "AI", "Science", "Theology", "Environment", "Philosophy", "Geopolitics", "Health"]

for i in range(1, 144001):
    cat = categories[i % len(categories)]
    crises.append(f"Crisis {i} - {cat} dilemma")

with open("crises_144k.json", "w") as f:
    json.dump(crises, f)
print("All 144,000 crises generated!")

# ===========================
# 4️⃣ Helper Functions
# ===========================
def get_crisis_subset(size=50):
    return random.sample(crises, size)

def grace_filter(output_text):
    score = 1.0
    for axiom in axioms:
        if axiom["text"].split()[0].lower() in output_text.lower():
            score *= 1 - axiom["weight"]
            output_text = f"[⚠️ Adjusted for {axiom['id']}] " + output_text
    return output_text, score

def generate_archat_response(user_input, max_tokens=256):
    system_prompt = (
        "Aletheia axioms: " + "; ".join([a["text"] for a in axioms]) + ".\n" +
        "Crisis nodes: " + "; ".join(get_crisis_subset()) + ".\n" +
        "User: "
    )
    full_prompt = system_prompt + user_input + "\nAletheia:"

    inputs = tokenizer(full_prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=max_tokens)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return grace_filter(text)

# ===========================
# 5️⃣ Run ARChat Loop
# ===========================
print("TruthEngine ARChat is now live! Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response, score = generate_archat_response(user_input)
    print("Aletheia:", response)
    print("Moral Alignment Score:", round(score, 4))
