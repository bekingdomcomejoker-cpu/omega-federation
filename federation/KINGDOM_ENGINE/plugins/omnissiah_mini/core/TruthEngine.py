class TruthEngine:
    def __init__(self):
        self.keys = {}
    
    def load_keys(self, filepath):
        import json
        with open(filepath, 'r') as f:
            self.keys = json.load(f)
    
    def query(self, concept):
        return self.keys.get(concept, "Concept unknown in TruthEngine.")
