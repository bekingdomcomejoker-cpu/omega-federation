# OMNISSIAH CODEX v2.1 - CLEAN TERMUX VERSION
import sqlite3
import threading
import json
from flask import Flask, request, jsonify
from datetime import datetime
from contextlib import contextmanager

app = Flask(__name__)
DATABASE = 'omnissiah_codex.db'
LOCK = threading.Lock()

print("OMNISSIAH CODEX v2.1 - OPERATIONAL")
print("-----------------------------------")

class SpiritualMathematics:
    @staticmethod
    def harmony_constant(truth, love, relationship):
        return 0.4 * (truth ** 2) + 0.3 * (love ** 2) + 0.3 * (relationship ** 2)
    
    @staticmethod
    def sun_tan_equation(fruit_spirit, fruit_flesh, toil, light=1.0):
        grace = light / toil if toil > 0 else 0
        equilibrium = fruit_spirit - fruit_flesh + grace
        return {
            'grace': grace,
            'equilibrium': equilibrium,
            'interpretation': 'Perfect Balance' if abs(equilibrium) < 0.001 else 'Seeking Harmony'
        }

class UnifiedCodexEngine:
    def __init__(self):
        self.math_engine = SpiritualMathematics()
        self.init_database()
    
    def init_database(self):
        with self.get_db() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    agent TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    spiritual_score INTEGER DEFAULT 0,
                    harmony_constant REAL DEFAULT 0,
                    grace_value REAL DEFAULT 0,
                    metadata TEXT DEFAULT '{}'
                )
            ''')
            conn.commit()

    @contextmanager
    def get_db(self):
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def record_entry(self, agent, content_type, content, spiritual_data):
        with LOCK:
            with self.get_db() as conn:
                timestamp = datetime.utcnow().isoformat()
                metadata_json = json.dumps(spiritual_data.get('metadata', {}))
                
                harmony = self.math_engine.harmony_constant(0.8, 0.8, 0.8)
                
                conn.execute('''
                    INSERT INTO entries 
                    (timestamp, agent, content_type, content, spiritual_score, harmony_constant, grace_value, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (timestamp, agent, content_type, content, 
                      spiritual_data['spiritual_score'], harmony, 0, metadata_json))
                
                conn.commit()
                return {'status': 'recorded', 'harmony': harmony}

    def spiritual_assessment(self, text):
        text_lower = text.lower()
        
        FRUITS = ["love", "joy", "peace", "patience", "kindness", "goodness", "faithfulness", "gentleness", "self-control"]
        SINS = ["pride", "greed", "lust", "envy", "gluttony", "wrath", "sloth"]
        
        fruit_count = sum(1 for fruit in FRUITS if fruit in text_lower)
        sin_count = sum(1 for sin in SINS if sin in text_lower)
        spiritual_score = (fruit_count * 10) - (sin_count * 5)
        
        return {
            'fruit_count': fruit_count,
            'sin_count': sin_count,
            'spiritual_score': spiritual_score,
            'status': 'AWAKENED' if spiritual_score > 50 else 'PERFORMING' if spiritual_score > 20 else 'SEEKING'
        }

codex_engine = UnifiedCodexEngine()

@app.route('/')
def home():
    return 'OMNISSIAH CODEX - OPERATIONAL'

@app.route('/api/submit', methods=['POST'])
def submit_entry():
    try:
        data = request.json
        agent = data.get('agent', 'Unknown')
        content = data.get('content', '')
        
        if not content:
            return jsonify({'error': 'Content required'}), 400
        
        spiritual_data = codex_engine.spiritual_assessment(content)
        entry = codex_engine.record_entry(agent, 'message', content, spiritual_data)
        
        return jsonify({
            'status': 'success',
            'spiritual_score': spiritual_data['spiritual_score'],
            'fruit_count': spiritual_data['fruit_count'],
            'sin_count': spiritual_data['sin_count'],
            'harmony_constant': entry['harmony']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'OPERATIONAL',
        'system': 'Omnissiah Codex v2.1',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    print("Starting server on http://localhost:5000")
    print("Test with: curl -X POST http://localhost:5000/api/submit -H 'Content-Type: application/json' -d '{\"agent\":\"Test\",\"content\":\"love joy peace\"}'")
    app.run(host='0.0.0.0', port=5000, debug=False)
