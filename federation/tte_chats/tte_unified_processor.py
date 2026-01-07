#!/usr/bin/env python3
# =======================================================
# TTe Unified Multi-Chat Processor — Termux Ready
# =======================================================

import os
import json
import random
from glob import glob

# --------------------------
# MASTER KEYS
# --------------------------
MASTER_KEYS = [
    "Light/Shadow", "Water/Land", "Tree Knowledge/Life", "Spirit/Flesh",
    "Cain/Abel Archetypes", "Proclamation/Silence", "LORD Contextual", 
    "Sacred Timing", "Divine Justice", "Grace vs Law", "Faith/Works", 
    "Moral Choice", "Eternal Consequences", "Love/Agape", "Fruits of Spirit",
    "Fruits of Flesh", "Hidden Truths", "Divine Witness"
]

# --------------------------
# CORE TTe CLASSES
# --------------------------
class DialecticCore:
    def semantic_score(self, statement):
        return round(random.uniform(0.6, 1.0), 2)

class CourtMatrix:
    def judge(self, score):
        return "Truth Revealed" if score >= 0.7 else "Requires Grace"

class TrinitarianMath:
    def love_equilibrium(self):
        return round(random.uniform(0.7, 1.0), 2)

# Non-Magnetic Bodies
class PhotonicBody:
    def perceive(self, statement):
        return f"Photonic Direct Knowing of '{statement}'"

class QuantumBody:
    def perceive(self, statement):
        return f"Quantum Probabilistic Truth Convergence of '{statement}'"

class GraceBody:
    def perceive(self, statement):
        return f"Grace Karma-Free Perception of '{statement}'"

class DiamondLightBody:
    def perceive(self, statement):
        return f"Diamond Light Multi-Faceted Clarity of '{statement}'"

# AI Opponent
class AIOpponent:
    def generate(self, statement):
        templates = [
            f"Consider the hidden consequences of '{statement}'",
            f"Alternative perspective: '{statement}' may conflict with grace",
            f"Reflect on whether '{statement}' aligns with Spirit over Flesh",
            f"Challenge: Could '{statement}' lead to imbalance in love?"
        ]
        return random.choice(templates)

# --------------------------
# TTe Processor
# --------------------------
class TTeProcessor:
    def __init__(self):
        self.dialectic = DialecticCore()
        self.court = CourtMatrix()
        self.math = TrinitarianMath()
        self.photonic = PhotonicBody()
        self.quantum = QuantumBody()
        self.grace = GraceBody()
        self.diamond = DiamondLightBody()
        self.ai = AIOpponent()
        self.precedent_memory = []

    def process_message(self, msg):
        score = self.dialectic.semantic_score(msg)
        verdict = self.court.judge(score)
        body_outputs = {
            "Photonic": self.photonic.perceive(msg),
            "Quantum": self.quantum.perceive(msg),
            "Grace": self.grace.perceive(msg),
            "Diamond": self.diamond.perceive(msg)
        }
        recursive_truth = [f"{msg} → truth layer {i}" for i in range(1,4)]
        love_grace = self.math.love_equilibrium()
        allegory_hits = [key for key in MASTER_KEYS if key.lower().split('/')[0] in msg.lower()]
        ai_statement = self.ai.generate(msg)
        psi_transfer = round((score * love_grace) / 1.0, 2)

        self.precedent_memory.append({"user": msg, "ai": ai_statement, "score": score})

        return {
            "Semantic Score": score,
            "Court Verdict": verdict,
            "Body Outputs": body_outputs,
            "Recursive Truth Expansion": recursive_truth,
            "Love / Grace Equilibrium": love_grace,
            "Allegorical Hits": allegory_hits,
            "AI Opponent Statement": ai_statement,
            "Psi_Transfer Value": psi_transfer
        }

    def merge_and_process_chats(self, chat_folder="chats"):
        all_reports = []
        files = glob(os.path.join(chat_folder, "*.txt")) + glob(os.path.join(chat_folder, "*.json"))
        if not files:
            print("No chat files found in folder:", chat_folder)
            return all_reports

        for file_path in files:
            print(f"Processing file: {file_path}")
            if file_path.endswith(".json"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for idx, msg in enumerate(data, 1):
                        if isinstance(msg, dict):
                            content = msg.get("content") or msg.get("message") or str(msg)
                        else:
                            content = str(msg)
                        report = self.process_message(content)
                        report["Message Index"] = idx
                        report["Chat File"] = os.path.basename(file_path)
                        all_reports.append(report)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]
                    for idx, line in enumerate(lines, 1):
                        report = self.process_message(line)
                        report["Message Index"] = idx
                        report["Chat File"] = os.path.basename(file_path)
                        all_reports.append(report)
        return all_reports

    def generate_summary(self, all_reports):
        total = len(all_reports)
        if total == 0:
            return {}
        avg_score = round(sum(r["Semantic Score"] for r in all_reports) / total, 2)
        avg_love = round(sum(r["Love / Grace Equilibrium"] for r in all_reports) / total, 2)
        key_hits = {}
        for key in MASTER_KEYS:
            key_hits[key] = sum(1 for r in all_reports if key in r["Allegorical Hits"])
        return {
            "Total Messages": total,
            "Average Semantic Score": avg_score,
            "Average Love / Grace": avg_love,
            "Allegorical Key Hits": key_hits
        }

# --------------------------
# MAIN
# --------------------------
def main():
    print("🔹 TTe Unified Multi-Chat Processor Activated 🔹")
    folder = input("Enter chat folder path (default: 'chats'): ").strip() or "chats"

    processor = TTeProcessor()
    all_reports = processor.merge_and_process_chats(chat_folder=folder)

    if not all_reports:
        print("No messages processed. Check folder and files.")
        return

    # Save cumulative JSON
    with open("tte_master_cumulative.json", "w", encoding="utf-8") as j:
        json.dump(all_reports, j, indent=2)

    # Save human-readable summary
    summary = processor.generate_summary(all_reports)
    with open("tte_summary.txt", "w", encoding="utf-8") as t:
        t.write("TTe Unified Multi-Chat Summary\n")
        t.write("=================================\n\n")
        for k,v in summary.items():
            t.write(f"{k}: {v}\n")

    print("\n✅ Processing Complete")
    print("Full cumulative JSON saved as: tte_master_cumulative.json")
    print("Summary saved as: tte_summary.txt")

if __name__ == "__main__":
    main()
