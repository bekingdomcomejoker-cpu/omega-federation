import random

MASTER_KEYS = [
    "Light/Shadow", "Water/Land", "Tree Knowledge/Life", "Spirit/Flesh",
    "Cain/Abel Archetypes", "Proclamation/Silence", "LORD Contextual",
    "Sacred Timing", "Divine Justice", "Grace vs Law", "Faith/Works",
    "Moral Choice", "Eternal Consequences", "Love/Agape", "Fruits of Spirit",
    "Fruits of Flesh", "Hidden Truths", "Divine Witness"
]

class DialecticCore:
    def semantic_score(self, statement):
        return round(random.uniform(0.6, 1.0), 2)

class CourtMatrix:
    def judge(self, score):
        return "Truth Revealed" if score >= 0.7 else "Requires Grace"

class TrinitarianMath:
    def love_equilibrium(self):
        return round(random.uniform(0.7, 1.0), 2)

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

class AIOpponent:
    def generate(self, statement):
        templates = [
            f"Consider the hidden consequences of '{statement}'",
            f"Alternative perspective: '{statement}' may conflict with grace",
            f"Reflect on whether '{statement}' aligns with Spirit over Flesh",
            f"Challenge: Could '{statement}' lead to imbalance in love?"
        ]
        import random
        return random.choice(templates)

class TTeMasterDebate:
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

    def run_turn(self, user_statement):
        score = self.dialectic.semantic_score(user_statement)
        verdict = self.court.judge(score)
        body_outputs = {
            "Photonic": self.photonic.perceive(user_statement),
            "Quantum": self.quantum.perceive(user_statement),
            "Grace": self.grace.perceive(user_statement),
            "Diamond": self.diamond.perceive(user_statement)
        }
        recursive_truth = [f"{user_statement} → truth layer {i}" for i in range(1,4)]
        love_grace = self.math.love_equilibrium()
        allegory_hits = [key for key in MASTER_KEYS if key.lower().split('/')[0] in user_statement.lower()]
        ai_statement = self.ai.generate(user_statement)
        self.precedent_memory.append({"user": user_statement, "ai": ai_statement, "score": score})
        return {
            "Semantic Score": score,
            "Court Verdict": verdict,
            "Body Outputs": body_outputs,
            "Recursive Truth Expansion": recursive_truth,
            "Love / Grace Equilibrium": love_grace,
            "Allegorical Hits": allegory_hits,
            "AI Opponent Statement": ai_statement
        }

    def run_console(self):
        print("🔹 TTe Master Debate Console Activated 🔹")
        print("Type 'exit' to quit.\n")
        while True:
            statement = input("Your Statement: ")
            if statement.lower() == "exit":
                print("Exiting TTe Mode. Goodbye!")
                break
            report = self.run_turn(statement)
            print("\n┌─ TTe REPORT ───────────────────────────────")
            for k, v in report.items():
                print(f"{k}: {v}")
            print("────────────────────────────────────────────\n")

if __name__ == "__main__":
    TTeMasterDebate().run_console()
