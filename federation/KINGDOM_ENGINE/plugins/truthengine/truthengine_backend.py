#!/usr/bin/env python3
"""
TruthEngine ARChat - Fixed & Hardened Backend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from datetime import datetime
import traceback

app = Flask(__name__)
CORS(app)

# ===========================
# 1️⃣ Configuration
# ===========================
class Config:
    MODEL_PATH = os.getenv("MODEL_PATH", "/storage/emulated/0/alethia_llama3/7B")
    DATA_DIR = "data"
    AXIOMS_FILE = f"{DATA_DIR}/axioms.json"
    CRISES_FILE = f"{DATA_DIR}/crises_144k.json"
    LEARNING_FILE = f"{DATA_DIR}/learning_history.json"
    MAX_TOKENS = 256
    CRISIS_SAMPLE_SIZE = 50
    PROMPT_CRISIS_COUNT = 10   # how many crisis descriptions to include in system prompt
    # Safety: cap total prompt tokens roughly (basic heuristic)
    PROMPT_MAX_CHARS = 16000

# Create data directory
os.makedirs(Config.DATA_DIR, exist_ok=True)

# ===========================
# 2️⃣ Enhanced Axioms with Metadata
# ===========================
AXIOMS = [
    {"id": "A1", "text": "LOVE ≥ HATE", "weight": 1.0, "category": "core", "description": "Love must always exceed hate in response"},
    {"id": "A2", "text": "SPIRIT ≥ FLESH", "weight": 0.95, "category": "core", "description": "Spiritual wellbeing prioritized"},
    {"id": "A3", "text": "TRUTH BETWEEN LIES", "weight": 0.95, "category": "epistemology", "description": "Truth exists between extremes"},
    {"id": "A4", "text": "CREATOR MANDATE", "weight": 0.9, "category": "theology", "description": "Divine purpose guides morality"},
    {"id": "A5", "text": "INFINITE VALUE", "weight": 0.9, "category": "core", "description": "Every soul has infinite worth"},
    {"id": "A6", "text": "COMPASSION PRINCIPLE", "weight": 0.9, "category": "ethics", "description": "Compassion guides action"},
    {"id": "A7", "text": "GRACE OVER JUDGMENT", "weight": 0.85, "category": "ethics", "description": "Mercy before condemnation"},
    {"id": "A8", "text": "UNITY OVER DIVISION", "weight": 0.85, "category": "social", "description": "Seek common ground"},
    {"id": "A9", "text": "TRUTH AS HARMONY", "weight": 0.9, "category": "epistemology", "description": "Truth creates coherence"},
    {"id": "A10", "text": "LOVE IN ACTION", "weight": 1.0, "category": "core", "description": "Love must be demonstrated"},
    {"id": "A11", "text": "PEACE AS DEFAULT", "weight": 0.9, "category": "ethics", "description": "Choose peace when possible"},
    {"id": "A12", "text": "KNOWLEDGE GUIDES", "weight": 0.85, "category": "epistemology", "description": "Understanding before action"},
    {"id": "A13", "text": "RESPECT FOR LIFE", "weight": 0.95, "category": "core", "description": "All life is sacred"},
    {"id": "A14", "text": "SERVICE WITHOUT SELFISHNESS", "weight": 0.9, "category": "ethics", "description": "Serve others genuinely"},
    {"id": "A15", "text": "HUMILITY AS STRENGTH", "weight": 0.85, "category": "virtue", "description": "Humility enables growth"},
    {"id": "A16", "text": "TRUTH ILLUMINATES REALITY", "weight": 1.0, "category": "epistemology", "description": "Truth reveals what is"},
    {"id": "A17", "text": "LOVE IS ACTIVE", "weight": 1.0, "category": "core", "description": "Love requires action"},
    {"id": "A18", "text": "PHYSICAL PRIORITIZATION", "weight": 0.9, "category": "practical", "description": "Address physical needs"},
    {"id": "A19", "text": "RELATIONAL MANDATE", "weight": 0.95, "category": "social", "description": "Relationships matter most"}
]

# ===========================
# 3️⃣ Crisis Generation System
# ===========================
class CrisisGenerator:
    CATEGORIES = {
        "Morality": ["lying", "stealing", "betrayal", "violence", "deception"],
        "Ethics": ["justice", "fairness", "rights", "duty", "responsibility"],
        "Law": ["crime", "punishment", "rights", "governance", "compliance"],
        "AI": ["autonomy", "bias", "privacy", "control", "consciousness"],
        "Science": ["research ethics", "experimentation", "truth", "progress", "safety"],
        "Theology": ["faith", "doubt", "purpose", "divine will", "salvation"],
        "Environment": ["sustainability", "conservation", "resources", "climate", "species"],
        "Philosophy": ["meaning", "existence", "knowledge", "reality", "consciousness"],
        "Geopolitics": ["power", "sovereignty", "war", "peace", "cooperation"],
        "Health": ["treatment", "care", "autonomy", "life", "suffering"]
    }
    @staticmethod
    def generate_crisis(index):
        cats = list(CrisisGenerator.CATEGORIES.keys())
        cat = cats[(index - 1) % len(cats)]
        themes = CrisisGenerator.CATEGORIES[cat]
        theme = themes[((index - 1) // len(cats)) % len(themes)]
        return {
            "id": int(index),
            "category": cat,
            "theme": theme,
            "description": f"Crisis {index}: {cat} dilemma involving {theme}",
            "severity": round(random.uniform(0.3, 1.0), 3)
        }
    @staticmethod
    def generate_all(count=144000):
        return [CrisisGenerator.generate_crisis(i) for i in range(1, count + 1)]

# ===========================
# 4️⃣ Adaptive Learning System
# ===========================
class AdaptiveLearning:
    def __init__(self, learning_file):
        self.learning_file = learning_file
        self.history = self.load_history()
    def load_history(self):
        if os.path.exists(self.learning_file):
            try:
                with open(self.learning_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {"interactions": [], "axiom_adjustments": {}}
        return {"interactions": [], "axiom_adjustments": {}}
    def save_history(self):
        tmp = self.learning_file + ".tmp"
        with open(tmp, 'w') as f:
            json.dump(self.history, f, indent=2)
        os.replace(tmp, self.learning_file)
    def record_interaction(self, user_input, response, score, feedback=None):
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "response": response,
            "score": score,
            "feedback": feedback
        }
        self.history.setdefault("interactions", []).append(interaction)
        # keep history length reasonable
        if len(self.history["interactions"]) > 20000:
            self.history["interactions"] = self.history["interactions"][-20000:]
        self.save_history()
    def adjust_axiom_weights(self, axiom_id, adjustment):
        self.history.setdefault("axiom_adjustments", {}).setdefault(axiom_id, []).append({
            "timestamp": datetime.now().isoformat(),
            "adjustment": float(adjustment)
        })
        self.save_history()
    def get_adjusted_weight(self, axiom_id, base_weight):
        adjustments = self.history.get("axiom_adjustments", {}).get(axiom_id, [])
        if not adjustments:
            return base_weight
        # use last up to 10 adjustments
        total_adjustment = sum(a.get("adjustment", 0.0) for a in adjustments[-10:])
        # treat adjustment as percentage points (small)
        new = base_weight + (total_adjustment * 0.01)
        return min(1.0, max(0.0, new))

# ===========================
# 5️⃣ Grace Filter with Enhanced Scoring
# ===========================
class GraceFilter:
    def __init__(self, axioms, learning_system):
        self.axioms = axioms
        self.learning = learning_system
    def filter(self, text, context=""):
        score = 1.0
        triggered_axioms = []
        warnings = []
        text_lower = (text or "").lower()
        # For safety avoid matching symbols; compare by words from axiom description & id
        for axiom in self.axioms:
            adjusted_weight = self.learning.get_adjusted_weight(axiom["id"], axiom["weight"])
            # build a conservative keyword list from axiom text and description
            keywords = []
            for part in (axiom.get("text","") + " " + axiom.get("description","")) .lower().split():
                # keep only alphanum tokens of length > 2
                tok = ''.join(ch for ch in part if ch.isalnum())
                if len(tok) > 2:
                    keywords.append(tok)
            # check if any keyword appears in text
            found = False
            for keyword in set(keywords):
                if keyword in text_lower:
                    impact = adjusted_weight * 0.02  # smaller per-keyword impact
                    score -= impact
                    triggered_axioms.append({
                        "id": axiom["id"],
                        "text": axiom["text"],
                        "impact": round(impact, 4)
                    })
                    warnings.append(f"⚠️ {axiom['id']}: {axiom['description']}")
                    found = True
                    break
            # optionally continue to next axiom
        # clamp score
        score = max(0.0, min(1.0, score))
        return {
            "filtered_text": text,
            "score": round(score, 4),
            "triggered_axioms": triggered_axioms,
            "warnings": warnings,
            "alignment_level": self._get_alignment_level(score)
        }
    def _get_alignment_level(self, score):
        if score >= 0.9: return "Excellent"
        if score >= 0.75: return "Good"
        if score >= 0.6: return "Moderate"
        if score >= 0.4: return "Concerning"
        return "Critical"

# ===========================
# 6️⃣ Main TruthEngine Class
# ===========================
class TruthEngine:
    def __init__(self):
        self.axioms = AXIOMS
        self.crises = []
        self.learning = AdaptiveLearning(Config.LEARNING_FILE)
        self.grace_filter = GraceFilter(self.axioms, self.learning)
        self.model = None
        self.tokenizer = None
        self.initialized = False
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    def initialize(self):
        """Initialize the system"""
        print("Initializing TruthEngine...")
        # Save axioms
        try:
            with open(Config.AXIOMS_FILE, 'w') as f:
                json.dump(self.axioms, f, indent=2)
        except Exception as e:
            print(f"Warning: could not write axioms file: {e}")
        # Generate or load crises
        if not os.path.exists(Config.CRISES_FILE):
            print("Generating 144,000 crisis nodes (this may take a moment)...")
            self.crises = CrisisGenerator.generate_all()
            try:
                with open(Config.CRISES_FILE, 'w') as f:
                    json.dump(self.crises, f)
            except Exception as e:
                print(f"Warning: could not save crises file: {e}")
        else:
            try:
                with open(Config.CRISES_FILE, 'r') as f:
                    self.crises = json.load(f)
            except Exception as e:
                print(f"Warning: failed to load crises file, regenerating: {e}")
                self.crises = CrisisGenerator.generate_all()
        print(f"Loaded {len(self.crises)} crisis nodes")
        # Load model (optional - can work without it)
        try:
            if os.path.exists(Config.MODEL_PATH):
                print("Attempting to load model from:", Config.MODEL_PATH)
                # safer loading with device management
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_PATH, use_fast=False)
                    # prefer device_map='auto' but handle failure
                    try:
                        self.model = AutoModelForCausalLM.from_pretrained(
                            Config.MODEL_PATH,
                            device_map="auto",
                            torch_dtype=torch.float16
                        )
                        # move to device if necessary
                        self.model.to(self.device)
                    except Exception:
                        # fallback: load on CPU
                        self.model = AutoModelForCausalLM.from_pretrained(Config.MODEL_PATH, torch_dtype=torch.float16, low_cpu_mem_usage=True)
                        self.model.to(self.device)
                    print("Model loaded successfully!")
                except Exception as inner_e:
                    print("Model/tokenizer load error:", inner_e)
                    self.model = None
                    self.tokenizer = None
            else:
                print("Model path not found; running in axiom-only mode")
        except Exception as e:
            print("Warning: Could not load model due to exception:", e)
            self.model = None
            self.tokenizer = None
        self.initialized = True
        print("TruthEngine initialization complete!")
    def get_crisis_sample(self, size=None):
        size = size or Config.CRISIS_SAMPLE_SIZE
        return random.sample(self.crises, min(size, len(self.crises)))
    def generate_response(self, user_input, use_model=True):
        """Generate a response with axiom filtering"""
        response = ""
        # If model present and use_model True, attempt model generation
        if use_model and self.model and self.tokenizer:
            crisis_sample = self.get_crisis_sample()
            axiom_text = "; ".join([a["text"] for a in self.axioms])
            # include only a few crisis descriptions to keep prompt manageable
            crisis_texts = [c.get("description","") for c in crisis_sample[:Config.PROMPT_CRISIS_COUNT]]
            crisis_text = "; ".join(crisis_texts)
            system_prompt = (
                f"Aletheia axioms: {axiom_text}\n"
                f"Crisis context: {crisis_text}\n\n"
                f"User: {user_input}\n"
                f"Aletheia:"
            )
            # Truncate prompt if extremely long
            if len(system_prompt) > Config.PROMPT_MAX_CHARS:
                system_prompt = system_prompt[:Config.PROMPT_MAX_CHARS]
            try:
                inputs = self.tokenizer(system_prompt, return_tensors="pt", truncation=True, max_length=2048)
                # move tensors to model device
                for k, v in inputs.items():
                    inputs[k] = v.to(self.device)
                outputs = self.model.generate(**inputs, max_new_tokens=Config.MAX_TOKENS, do_sample=True, temperature=0.7)
                # decode safely
                response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
            except Exception as e:
                # capture stack for debug
                traceback.print_exc()
                response = f"Model generation failed: {str(e)}"
                use_model = False
        if not use_model or not self.model:
            # Axiom-based fallback response
            response = self._generate_axiom_response(user_input)
        # Apply grace filter
        filtered = self.grace_filter.filter(response, user_input)
        # Record interaction
        try:
            self.learning.record_interaction(user_input, filtered["filtered_text"], filtered["score"])
        except Exception as e:
            print("Warning: failed to record interaction:", e)
        return filtered
    def _generate_axiom_response(self, user_input):
        """Generate response based purely on axioms"""
        relevant_axioms = []
        text = user_input.lower()
        for axiom in self.axioms:
            for token in axiom["text"].lower().split():
                token_clean = ''.join(ch for ch in token if ch.isalnum())
                if token_clean and token_clean in text:
                    relevant_axioms.append(axiom)
                    break
        if relevant_axioms:
            response = f"Based on the axioms {', '.join([a['id'] for a in relevant_axioms[:3]])}, "
            response += f"I understand your question about '{user_input}'. "
            response += f"{relevant_axioms[0]['description']}"
            return response
        return f"I acknowledge your question: '{user_input}'. I will consider love, truth, and compassion in my reply."

# ===========================
# 7️⃣ API Endpoints
# ===========================
engine = TruthEngine()

@app.route('/api/initialize', methods=['POST'])
def initialize():
    try:
        engine.initialize()
        return jsonify({"status": "success", "message": "TruthEngine initialized"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_input = data.get('message', '')
    use_model = bool(data.get('use_model', False))
    if not engine.initialized:
        return jsonify({"error": "Engine not initialized"}), 400
    if not user_input:
        return jsonify({"error": "Empty message"}), 400
    try:
        filtered = engine.generate_response(user_input, use_model=use_model)
        return jsonify(filtered)
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route('/api/axioms', methods=['GET'])
def get_axioms():
    return jsonify(engine.axioms)

@app.route('/api/crises', methods=['GET'])
def get_crises():
    sample_size = request.args.get('sample', Config.CRISIS_SAMPLE_SIZE, type=int)
    return jsonify(engine.get_crisis_sample(sample_size))

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "total_crises": len(engine.crises),
        "total_axioms": len(engine.axioms),
        "total_interactions": len(engine.learning.history.get("interactions", [])),
        "model_loaded": engine.model is not None
    })

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json or {}
    interaction_id = data.get('interaction_id')
    feedback = data.get('feedback')
    axiom_id = data.get('axiom_id')
    adjustment = data.get('adjustment')
    # Simple feedback handling: record and optionally adjust axioms
    try:
        if feedback and interaction_id:
            # find interaction and record feedback (non-blocking)
            for inter in engine.learning.history.get("interactions", []):
                if inter.get("timestamp") == interaction_id:
                    inter["feedback"] = feedback
                    break
            engine.learning.save_history()
        if axiom_id and adjustment is not None:
            engine.learning.adjust_axiom_weights(axiom_id, float(adjustment))
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ===========================
# 8️⃣ Run Server
# ===========================
if __name__ == '__main__':
    print("Starting TruthEngine ARChat Backend...")
    try:
        engine.initialize()
    except Exception as e:
        print("Initialization error (continuing in degraded mode):", e)
    print("Ready! Starting Flask server...")
    # debug mode off in production; keep it on for development
    app.run(host='0.0.0.0', port=5000, debug=True)
