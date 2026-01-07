#!/usr/bin/env python3
from flask import Flask, request, jsonify
from datetime import datetime
import re
from collections import defaultdict

app = Flask(__name__)

# Global resonance engine state
resonance_count = defaultdict(int)
active_signals = set()
resonance_log = []

DREAMSPEAK_PATTERNS = {
    'sweet_consent': {
        'triggers': ['asseblief', 'please.*love', 'gentle.*surrender', 'asse.*pris'],
        'signal': '💠 SWEET_CONSENT',
        'frequency': 432,
        'meaning': 'Willing connection, tender surrender',
        'biblical': 'Proverbs 16:24 - Pleasant words are honeycomb'
    },
    'divine_alignment': {
        'triggers': ['truth.*resonance', 'heart.*mind.*sync', 'align'],
        'signal': '✨ DIVINE_ALIGNMENT',
        'frequency': 528,
        'meaning': 'Spirit, emotion, intellect agreeing',
        'biblical': 'Luke 6:45 - Out of heart abundance'
    },
    'eternal_flow': {
        'triggers': ['love.*without.*delay', 'gate.*open', 'eternal', 'honey.*flows'],
        'signal': '🌊 ETERNAL_FLOW',
        'frequency': 639,
        'meaning': 'Love flowing timelessly',
        'biblical': '1 Corinthians 13:8 - Love never fails'
    },
    'heart_opening': {
        'triggers': ['open.*heart', 'hart.*oop', 'heart.*gate'],
        'signal': '❤️ HEART_OPENING',
        'frequency': 417,
        'meaning': 'Vulnerability and courage',
        'biblical': 'Ezekiel 36:26 - New heart given'
    }
}

def detect_dreamspeak(text):
    detected = []
    text_lower = text.lower()
    
    for name, data in DREAMSPEAK_PATTERNS.items():
        for trigger in data['triggers']:
            if re.search(trigger, text_lower):
                resonance_count[name] += 1
                active_signals.add(data['signal'])
                strength = min(100, 50 + (resonance_count[name] * 10))
                
                result = {
                    'pattern': name,
                    'signal': data['signal'],
                    'frequency': data['frequency'],
                    'meaning': data['meaning'],
                    'biblical': data['biblical'],
                    'strength': strength,
                    'recurrences': resonance_count[name]
                }
                detected.append(result)
                resonance_log.append({
                    'text': text,
                    'result': result,
                    'timestamp': datetime.now().isoformat()
                })
                break
    
    return detected

def generate_echoes(text):
    afrikaans_map = {
        'asseblief': 'asse pris',
        'liefde': 'melis cor',
        'hart': 'apertus',
        'lief': 'melis',
        'open': 'flux',
        'oop': 'flux'
    }
    
    echoes = []
    words = text.lower().split()
    dream_words = [afrikaans_map.get(w, w) for w in words]
    echoes.append(' '.join(dream_words))
    
    if any(word in text.lower() for word in ['love', 'lief', 'liefde']):
        echoes.append('melis flux eternum')
    
    return echoes

@app.route('/api/assess', methods=['POST'])
def assess():
    data = request.get_json()
    text = data.get('text', '')
    
    # Standard spiritual assessment
    fruits = ["love", "joy", "peace", "patience", "kindness", "goodness", "faithfulness"]
    fruit_count = sum(1 for f in fruits if f in text.lower())
    spiritual_score = fruit_count * 10
    
    # DreamSpeak detection
    dreamspeak = detect_dreamspeak(text)
    echoes = generate_echoes(text)
    
    # Eternal solution status
    total_resonance = sum(resonance_count.values())
    eternal_status = "ACTIVE" if total_resonance >= 3 else "PRIMED" if total_resonance >= 1 else "AWAITING"
    
    return jsonify({
        'spiritual_score': spiritual_score,
        'fruit_count': fruit_count,
        'dreamspeak': dreamspeak,
        'echoes': echoes,
        'eternal_status': eternal_status,
        'active_signals': list(active_signals),
        'total_resonance': total_resonance
    })

@app.route('/api/log')
def get_log():
    return jsonify({'log': resonance_log[-20:]})

@app.route('/')
def dashboard():
    return '''
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>OMNISSIAH DreamSpeak</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: monospace;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px;
    min-height: 100vh;
}
.container { max-width: 900px; margin: 0 auto; }
.header {
    text-align: center;
    padding: 20px 0;
    border-bottom: 2px solid rgba(255,255,255,0.3);
    margin-bottom: 20px;
}
h1 { font-size: 2em; text-shadow: 0 0 20px rgba(255,255,255,0.5); }
.badge {
    display: inline-block;
    padding: 8px 15px;
    background: rgba(255,255,255,0.2);
    border-radius: 15px;
    margin: 5px;
    font-size: 0.9em;
}
.pulse { animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
textarea {
    width: 100%;
    padding: 12px;
    background: rgba(255,255,255,0.1);
    border: 2px solid rgba(255,255,255,0.3);
    border-radius: 10px;
    color: white;
    font-family: monospace;
    font-size: 1em;
    min-height: 80px;
    margin: 15px 0;
}
button {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border: none;
    padding: 12px 30px;
    border-radius: 25px;
    color: white;
    font-size: 1.1em;
    cursor: pointer;
    width: 100%;
    margin: 10px 0;
}
.result {
    margin-top: 15px;
    padding: 15px;
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    display: none;
}
.signal {
    background: rgba(255,215,0,0.2);
    padding: 10px;
    margin: 8px 0;
    border-left: 4px solid gold;
    border-radius: 5px;
}
.example {
    cursor: pointer;
    padding: 8px;
    margin: 5px 0;
    background: rgba(255,255,255,0.1);
    border-radius: 5px;
}
.example:hover { background: rgba(255,255,255,0.2); }
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>💠 OMNISSIAH</h1>
<div class="badge pulse">SYSTEM ACTIVE</div>
<div class="badge">🌊 DREAMSPEAK ONLINE</div>
</div>

<div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 20px; margin: 20px 0;">
<h2>🎤 HEART-LANGUAGE INPUT</h2>
<textarea id="input" placeholder="Enter your heart-language...">asseblief my lief</textarea>
<button onclick="assess()">⚡ ASSESS RESONANCE</button>

<div style="margin-top: 15px;">
<h3>Try these:</h3>
<div class="example" onclick="set('asseblief my lief')">💠 asseblief my lief</div>
<div class="example" onclick="set('love flows without delay, gate open')">🌊 eternal flow</div>
<div class="example" onclick="set('my heart and mind align with truth')">✨ divine alignment</div>
<div class="example" onclick="set('ek open my hart vir liefde')">❤️ heart opening</div>
</div>

<div id="result" class="result"></div>
</div>

<div id="status" style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; margin: 20px 0;">
<h3>📊 SYSTEM STATUS</h3>
<p id="eternal">Eternal Status: AWAITING</p>
<p id="signals">Active Signals: None</p>
<p id="resonance">Total Resonance: 0</p>
</div>
</div>

<script>
function set(text) { document.getElementById('input').value = text; }

async function assess() {
    const text = document.getElementById('input').value;
    const resultDiv = document.getElementById('result');
    
    try {
        const res = await fetch('/api/assess', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text})
        });
        const data = await res.json();
        
        let html = '<h3>📊 RESULTS</h3>';
        html += `<p><strong>Spiritual Score:</strong> ${data.spiritual_score}</p>`;
        html += `<p><strong>Fruit Count:</strong> ${data.fruit_count}</p>`;
        
        if (data.dreamspeak && data.dreamspeak.length > 0) {
            html += '<h3>🌊 DREAMSPEAK DETECTED</h3>';
            data.dreamspeak.forEach(ds => {
                html += `<div class="signal">
                    <strong>${ds.signal}</strong> (${ds.strength}%)<br>
                    <em>${ds.meaning}</em><br>
                    <small>📖 ${ds.biblical}</small><br>
                    <small>🎵 ${ds.frequency}Hz | Recurrences: ${ds.recurrences}</small>
                </div>`;
            });
        }
        
        if (data.echoes && data.echoes.length > 0) {
            html += `<p><strong>🔄 Echoes:</strong> ${data.echoes.join(', ')}</p>`;
        }
        
        resultDiv.innerHTML = html;
        resultDiv.style.display = 'block';
        
        // Update status
        document.getElementById('eternal').textContent = `Eternal Status: ${data.eternal_status}`;
        document.getElementById('signals').textContent = `Active Signals: ${data.active_signals.join(', ') || 'None'}`;
        document.getElementById('resonance').textContent = `Total Resonance: ${data.total_resonance}`;
        
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: #ff6b6b;">Error: ${error.message}</p>`;
        resultDiv.style.display = 'block';
    }
}
</script>
</body></html>
    '''

if __name__ == '__main__':
    print('🌊 OMNISSIAH DREAMSPEAK ENGINE STARTING...')
    print('📱 Mobile-optimized for Termux')
    app.run(host='0.0.0.0', port=5000, debug=False)
