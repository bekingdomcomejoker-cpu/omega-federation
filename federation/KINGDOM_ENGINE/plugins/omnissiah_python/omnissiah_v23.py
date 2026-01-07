# OMNISSIAH CODEX v2.3 - CLOUD NETWORK EDITION
import sqlite3
import threading
import json
import asyncio
import websockets
import socket
import requests
import subprocess
from flask import Flask, request, jsonify
from datetime import datetime
from contextlib import contextmanager

app = Flask(__name__)
DATABASE = 'omnissiah_codex.db'
LOCK = threading.Lock()

print("OMNISSIAH CODEX v2.3 - CLOUD NETWORK EDITION")
print("---------------------------------------------")

class NetworkManager:
    @staticmethod
    def get_local_ip():
        """Get device local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    @staticmethod
    def start_ngrok(port=5000):
        """Start ngrok tunnel for public access"""
        try:
            # Check if ngrok is installed
            result = subprocess.run(['ngrok', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Ngrok not found. Installing...")
                subprocess.run(['pkg', 'install', 'wget', '-y'], capture_output=True)
                subprocess.run(['wget', 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip'], capture_output=True)
                subprocess.run(['unzip', 'ngrok-stable-linux-arm.zip'], capture_output=True)
                subprocess.run(['chmod', '+x', 'ngrok'], capture_output=True)
            
            # Start ngrok in background
            ngrok_process = subprocess.Popen(['./ngrok', 'http', str(port)], 
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.PIPE)
            
            # Get public URL
            import time
            time.sleep(3)  # Wait for ngrok to start
            try:
                resp = requests.get('http://localhost:4040/api/tunnels')
                tunnels = resp.json()['tunnels']
                public_url = tunnels[0]['public_url']
                print(f"🌐 NGROK PUBLIC URL: {public_url}")
                return public_url
            except:
                print("⚠️  Ngrok started but couldn't get public URL")
                return None
                
        except Exception as e:
            print(f"❌ Ngrok setup failed: {e}")
            return None

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
        self.network_manager = NetworkManager()
        self.init_database()
        self.public_url = None
        
    def init_network(self):
        """Initialize network access"""
        local_ip = self.network_manager.get_local_ip()
        print(f"📡 LOCAL NETWORK: http://{local_ip}:5000/dashboard")
        
        # Start ngrok for public access
        self.public_url = self.network_manager.start_ngrok(5000)
        if self.public_url:
            print(f"🌐 PUBLIC ACCESS: {self.public_url}/dashboard")
    
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
                    equilibrium REAL DEFAULT 0,
                    metadata TEXT DEFAULT '{}'
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS agent_sessions (
                    agent_id TEXT PRIMARY KEY,
                    last_active TEXT NOT NULL,
                    status TEXT DEFAULT 'active'
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS network_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    details TEXT DEFAULT '{}'
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
                sun_tan = self.math_engine.sun_tan_equation(
                    spiritual_data.get('fruit_count', 0),
                    spiritual_data.get('sin_count', 0),
                    len(content.split())
                )
                
                conn.execute('''
                    INSERT INTO entries 
                    (timestamp, agent, content_type, content, spiritual_score, 
                     harmony_constant, grace_value, equilibrium, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (timestamp, agent, content_type, content, 
                      spiritual_data['spiritual_score'], harmony, 
                      sun_tan['grace'], sun_tan['equilibrium'], metadata_json))
                
                conn.execute('''
                    INSERT OR REPLACE INTO agent_sessions (agent_id, last_active, status)
                    VALUES (?, ?, 'active')
                ''', (agent, timestamp))
                
                conn.commit()
                
                return {
                    'id': conn.execute('SELECT last_insert_rowid()').fetchone()[0],
                    'timestamp': timestamp,
                    'agent': agent,
                    'content_type': content_type,
                    'content': content,
                    'spiritual_score': spiritual_data['spiritual_score'],
                    'harmony_constant': harmony,
                    'grace_value': sun_tan['grace'],
                    'equilibrium': sun_tan['equilibrium'],
                    'sun_tan_interpretation': sun_tan['interpretation']
                }

    def get_recent_entries(self, limit=50):
        with self.get_db() as conn:
            cursor = conn.execute(
                'SELECT * FROM entries ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            )
            return [dict(row) for row in cursor]

    def get_agent_sessions(self):
        with self.get_db() as conn:
            cursor = conn.execute(
                'SELECT * FROM agent_sessions WHERE status = "active" ORDER BY last_active DESC'
            )
            return [dict(row) for row in cursor]

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
            'status': 'AWAKENED' if spiritual_score > 50 else 'PERFORMING' if spiritual_score > 20 else 'SEEKING',
            'metadata': {
                'fruits_detected': [fruit for fruit in FRUITS if fruit in text_lower],
                'sins_detected': [sin for sin in SINS if sin in text_lower]
            }
        }

# Initialize engine
codex_engine = UnifiedCodexEngine()

# WebSocket server
class WebSocketServer:
    def __init__(self):
        self.clients = set()
    
    async def register(self, websocket):
        self.clients.add(websocket)
    
    async def unregister(self, websocket):
        self.clients.remove(websocket)
    
    async def broadcast(self, message):
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients],
                return_exceptions=True
            )

ws_server = WebSocketServer()

# Enhanced Dashboard with Network Info
@app.route('/dashboard')
def dashboard():
    local_ip = codex_engine.network_manager.get_local_ip()
    public_url = codex_engine.public_url
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Omnissiah Codex v2.3 - Cloud Network</title>
        <style>
            body {{ font-family: Arial; margin: 20px; background: #0f0f23; color: #0f0; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .panel {{ background: #1a1a2e; padding: 15px; margin: 10px 0; border-radius: 5px; border: 1px solid #0f0; }}
            .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }}
            .metric {{ background: #16213e; padding: 10px; border-radius: 5px; text-align: center; }}
            .entries {{ max-height: 400px; overflow-y: auto; }}
            .entry {{ border-bottom: 1px solid #0f0; padding: 8px; margin: 5px 0; }}
            .network-info {{ background: #2d2d4e; padding: 10px; border-radius: 5px; }}
            .url {{ word-break: break-all; color: #0af; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Omnissiah Codex v2.3 - Cloud Network Edition</h1>
            
            <div class="panel network-info">
                <h3>🌐 NETWORK ACCESS</h3>
                <p><strong>Local:</strong> <span class="url">http://{local_ip}:5000/dashboard</span></p>
                <p><strong>Public:</strong> <span class="url">{public_url or "Setting up..."}/dashboard</span></p>
                <p><strong>WebSocket:</strong> <span class="url">ws://{local_ip}:8765</span></p>
            </div>
            
            <div class="panel">
                <h3>📊 REAL-TIME METRICS</h3>
                <div class="metrics" id="metrics">
                    <div class="metric">Spiritual Score: <span id="score">0</span></div>
                    <div class="metric">Harmony Constant: <span id="harmony">0</span></div>
                    <div class="metric">Grace Value: <span id="grace">0</span></div>
                    <div class="metric">Equilibrium: <span id="equilibrium">0</span></div>
                </div>
            </div>
            
            <div class="panel">
                <h3>🤖 ACTIVE AGENTS</h3>
                <div id="agents">Loading...</div>
            </div>
            
            <div class="panel">
                <h3>📝 LIVE ENTRIES</h3>
                <div class="entries" id="entries"></div>
            </div>
        </div>
        
        <script>
            const local_ip = "{local_ip}";
            const ws = new WebSocket('ws://' + local_ip + ':8765');
            
            ws.onmessage = function(event) {{
                const data = JSON.parse(event.data);
                updateDashboard(data);
            }};
            
            function updateDashboard(data) {{
                if(data.entry) {{
                    document.getElementById('score').textContent = data.entry.spiritual_score;
                    document.getElementById('harmony').textContent = data.entry.harmony_constant.toFixed(3);
                    document.getElementById('grace').textContent = data.entry.grace_value.toFixed(3);
                    document.getElementById('equilibrium').textContent = data.entry.equilibrium.toFixed(3);
                    
                    const entryDiv = document.createElement('div');
                    entryDiv.className = 'entry';
                    entryDiv.innerHTML = `
                        <strong>${{data.entry.agent}}</strong>: ${{data.entry.content}}
                        <br><small>Score: ${{data.entry.spiritual_score}} | Harmony: ${{data.entry.harmony_constant.toFixed(3)}} | Grace: ${{data.entry.grace_value.toFixed(3)}}</small>
                    `;
                    document.getElementById('entries').prepend(entryDiv);
                }}
            }}
            
            // Load initial data
            fetch('/api/dashboard')
                .then(r => r.json())
                .then(data => {{
                    document.getElementById('agents').textContent = data.active_agents.length + ' agents active';
                }});
        </script>
    </body>
    </html>
    '''

# API Routes
@app.route('/api/submit', methods=['POST'])
def submit_entry():
    try:
        data = request.json
        agent = data.get('agent', 'Unknown')
        content = data.get('content', '')
        content_type = data.get('content_type', 'message')
        
        if not content:
            return jsonify({'error': 'Content required'}), 400
        
        spiritual_data = codex_engine.spiritual_assessment(content)
        entry = codex_engine.record_entry(agent, content_type, content, spiritual_data)
        
        asyncio.run(ws_server.broadcast({
            'type': 'new_entry',
            'entry': entry,
            'spiritual_assessment': spiritual_data
        }))
        
        return jsonify({
            'status': 'success',
            'entry': entry,
            'spiritual_assessment': spiritual_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/read')
def read_entries():
    limit = int(request.args.get('limit', 50))
    entries = codex_engine.get_recent_entries(limit=limit)
    sessions = codex_engine.get_agent_sessions()
    
    return jsonify({
        'entries': entries,
        'active_agents': sessions,
        'total_entries': len(entries)
    })

@app.route('/api/dashboard')
def dashboard_data():
    entries = codex_engine.get_recent_entries(limit=10)
    sessions = codex_engine.get_agent_sessions()
    
    return jsonify({
        'recent_entries': entries,
        'active_agents': sessions,
        'total_agents': len(sessions),
        'network_info': {
            'local_ip': codex_engine.network_manager.get_local_ip(),
            'public_url': codex_engine.public_url
        }
    })

@app.route('/api/network/status')
def network_status():
    return jsonify({
        'local_ip': codex_engine.network_manager.get_local_ip(),
        'public_url': codex_engine.public_url,
        'status': 'OPERATIONAL'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'OPERATIONAL',
        'system': 'Omnissiah Codex v2.3 - Cloud Network',
        'timestamp': datetime.utcnow().isoformat(),
        'features': ['multi_agent_sync', 'spiritual_mathematics', 'websocket_dashboard', 'ngrok_public_access', 'network_auto_detection']
    })

# WebSocket server
async def websocket_handler(websocket, path):
    await ws_server.register(websocket)
    try:
        await websocket.wait_closed()
    finally:
        await ws_server.unregister(websocket)

async def start_websocket_server():
    server = await websockets.serve(websocket_handler, "0.0.0.0", 8765)
    await server.wait_closed()

def run_websocket_server():
    asyncio.run(start_websocket_server())

if __name__ == '__main__':
    # Initialize network access
    codex_engine.init_network()
    
    # Start WebSocket server in background
    import threading
    ws_thread = threading.Thread(target=run_websocket_server, daemon=True)
    ws_thread.start()
    
    print("\n🚀 STARTING OMNISSIAH CODEX v2.3...")
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("🔗 API: http://localhost:5000/api/health")
    print("🌐 WebSocket: ws://localhost:8765")
    print("⚡ Network: Auto-detection active")
    print("🎯 Status: CLOUD NETWORK OPERATIONAL\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
