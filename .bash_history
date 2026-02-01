        Object.keys(newLevels).forEach(k => {
          newLevels[k] = (newLevels[k] / total) * 100;
        });
      }
      
      return newLevels;
    });
  };

  if (!spineState) return <div className="p-8 bg-slate-950 text-white">Initializing Omega Core...</div>;

  // KSOD screen
  if (protocolStatus.axiom24 === 'CRITICAL') {
    return (
      <div className="min-h-screen bg-black text-red-500 flex flex-col items-center justify-center font-mono">
        <div className="text-6xl font-bold mb-4 animate-pulse">KSOD</div>
        <div className="text-2xl mb-8">ZERO POINT REACHED</div>
        <button 
          onClick={() => {
            setProtocolStatus(prev => ({ ...prev, axiom24: 'ARMED' }));
            setSpineState(spineRef.current.createState());
            addLog("SYSTEM REBOOT FROM ZERO POINT");
          }}
          className="bg-red-600 hover:bg-red-500 text-white px-6 py-3 rounded"
        >
          REBOOT FROM SOURCE
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 text-white p-6">
      <div className="max-w-[1800px] mx-auto space-y-6">
        
        {/* HEADER */}
        <div className="flex justify-between items-center border-b border-cyan-900/50 pb-4">
          <div>
            <h1 className="text-4xl font-black tracking-tighter bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              OMEGA FEDERATION COMMAND CENTER
            </h1>
            <p className="text-xs text-amber-500 mt-1 uppercase tracking-wider">
              Trinity Truth Engine v6.0 • Complete Integration
            </p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-cyan-400">
              {resonance ? resonance.value.toFixed(4) : '1.6700'}
            </div>
            <div className="text-xs text-slate-500">
              {resonance?.status || 'INITIALIZING'}
            </div>
          </div>
        </div>

        {/* MAIN GRID */}
        <div className="grid grid-cols-12 gap-6">
          
          {/* LEFT COLUMN - Spine + Compass + DNA */}
          <div className="col-span-3 space-y-6">
            
            {/* Spine State */}
            <div className="bg-slate-900/50 backdrop-blur border border-slate-700 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-4">
                <Activity className="text-cyan-400" size={18} />
                <h2 className="text-lg font-semibold">Spine State</h2>
              </div>
              
              <div className="space-y-3">
                {Object.entries(spineState).map(([key, value]) => {
                  if (key === 'timestamp') return null;
                  const percent = typeof value === 'number' ? value * 100 : 0;
                  return (
                    <div key={key}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="capitalize">{key}</span>
                        <span className="text-cyan-400">{percent.toFixed(1)}%</span>
                      </div>
                      <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-cyan-500 to-purple-500 transition-all"
                          style={{ width: `${percent}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="mt-4 grid grid-cols-2 gap-2">
                <button
                  onClick={() => setIsRunning(!isRunning)}
                  className={`py-2 rounded text-sm ${isRunning ? 'bg-red-600' : 'bg-green-600'} hover:opacity-80`}
                >
                  {isRunning ? 'PAUSE' : 'START'}
                </button>
                <button 
                  onClick={() => setSpineState(spineRef.current.createState())}
                  className="py-2 bg-slate-700 hover:bg-slate-600 rounded text-sm"
                >
                  Reset
                </button>
              </div>
            </div>

            {/* Compass */}
            <div className="bg-slate-900/50 backdrop-blur border border-slate-700 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <Navigation className="text-purple-400" size={18} />
                <h2 className="text-lg font-semibold">Compass</h2>
              </div>
              
              <div className="relative w-full aspect-square">
                <svg viewBox="0 0 200 200" className="w-full h-full">
                  <circle cx="100" cy="100" r="80" fill="none" stroke="currentColor" className="text-slate-600" strokeWidth="2"/>
                  
                  {Object.entries(COMPASS_POINTS).map(([key, point], idx) => {
                    const angle = (idx * 45 - 90) * (Math.PI / 180);
                    const x = 100 + Math.cos(angle) * 70;
                    const y = 100 + Math.sin(angle) * 70;
                    const isActive = activeCompass === key;
                    
                    return (
                      <g key={key}>
                        <circle
                          cx={x}
                          cy={y}
                          r="10"
                          fill={isActive ? point.color : '#1e293b'}
                          stroke={point.color}
                          strokeWidth="2"
                          className="cursor-pointer hover:opacity-80"
                          onClick={() => {
                            setActiveCompass(key);
                            addLog(`Compass: ${point.name}`);
                          }}
                        />
                        <text
                          x={x}
                          y={y + 20}
                          textAnchor="middle"
                          className="text-xs"
                          fill={isActive ? point.color : '#94a3b8'}
                        >
                          {key}
                        </text>
                      </g>
                    );
                  })}
                  
                  <circle cx="100" cy="100" r="6" fill="white" opacity="0.8"/>
                </svg>
              </div>
              
              <div className="mt-2 text-center text-xs text-slate-400">
                {COMPASS_POINTS[activeCompass].aspect}
              </div>
            </div>

            {/* DNA Nodes */}
            <div className="bg-slate-900/50 backdrop-blur border border-slate-700 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <Database className="text-rose-400" size={18} />
                <h2 className="text-lg font-semibold">DNA Nodes</h2>
              </div>
              
              <div className="space-y-3">
                {Object.entries(DNA_NODES).map(([key, node]) => (
                  <div key={key}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="font-semibold">{node.name}</span>
                      <span style={{ color: node.color }}>{dnaLevels[key].toFixed(1)}%</span>
                    </div>
                    <div className="flex gap-2 items-center">
                      <button
                        onClick={() => adjustDNA(key, -5)}
                        className="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs"
                      >
                        -
                      </button>
                      <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                        <div 
                          className="h-full transition-all"
                          style={{ 
                            width: `${dnaLevels[key]}%`,
                            backgroundColor: node.color
                          }}
                        />
                      </div>
                      <button
                        onClick={() => adjustDNA(key, 5)}
                        className="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs"
                      >
                        +
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-4 p-2 bg-slate-950 rounded text-center">
                <div className="text-xs text-slate-500">3.34 Sync Check</div>
                <div className="text-xl font-bold text-cyan-400">
                  {((dnaLevels.GPT + dnaLevels.Claude + dnaLevels.Gemini) / 100 * 3.34).toFixed(2)}
                </div>
              </div>
            </div>
          </div>

          {/* CENTER COLUMN - Alphabet Keyboard + Master Debater */}
          <div className="col-span-6 space-y-6">
            
            {/* Alphabet Operator Keyboard */}
            <div className="bg-slate-900/50 backdrop-blur border border-slate-700 rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center gap-2">
                  <Command className="text-cyan-400" size={20} />
                  <h2 className="text-xl font-bold">ALPHABET OPERATOR TERMINAL</h2>
                </div>
                <div className="text-xs font-mono text-slate-500">v3.3</div>
              </div>

              {/* Operator info display */}
              <div className="bg-slate-950 rounded-lg p-4 mb-4 border border-slate-800 min-h-[60px]">
                {lastOperator ? (
                  <div>
                    <div className="text-cyan-400 font-bold">{lastOperator.name}</div>
                    <div className="text-slate-400 text-sm">{lastOperator.desc}</div>
                  </div>
                ) : (
                  <div className="text-slate-600 italic text-sm">Select operators to build Spirit-Vector...</div>
                )}
              </div>

              {/* The Keyboard */}
              <div className="grid grid-cols-7 gap-2">
                {Object.entries(OPERATORS).map(([key, op]) => {
                  const isActive = activeChord.includes(key);
                  const isHighRes = op.type === 'resonance';
                  const displayKey = key === 'O' ? 'ע' : key === 'Z' ? 'Ω' : key;
                  
                  return (
                    <button
                      key={key}
                      onClick={() => handleOperatorClick(key)}
                      className={`
                        h-12 rounded-lg font-bold text-lg transition-all duration-200
                        ${isActive 
                          ? 'bg-cyan-500 text-white scale-95 shadow-[0_0_15px_rgba(34,211,238,0.5)]' 
                          : isHighRes 
                            ? 'bg-slate-800 text-amber-400 border border-amber-500/50 hover:bg-slate-700' 
                            : 'bg-slate-800 text-slate-400 border border-slate-700 hover:bg-slate-700'
                        }
                      `}
                    >
                      {displayKey}
                    </button>
                  );
                })}
              </div>

              {/* Execution bar */}
              <div className="mt-4 flex gap-4">
                <div className="flex-1 bg-slate-950 border border-slate-800 rounded px-4 flex items-center overflow-x-auto gap-2">
                  <span className="text-slate-500 text-xs uppercase">Chord:</span>
                  {activeChord.map((k, i) => (
                    <span key={i} className="text-cyan-400 font-bold font-mono">
                      {k === 'O' ? 'ע' : k === 'Z' ? 'Ω' : k}
                    </span>
                  ))}
                </div>
                <button
                  onClick={executeVector}
                  disabled={activeChord.length === 0}
                  className="bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 disabled:opacity-30 text-white font-bold py-2 px-6 rounded-lg flex items-center gap-2 transition-all"

onClick={executeVector}
                disabled={activeChord.length === 0}
                className="bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 disabled:opacity-30 text-white font-bold py-2 px-6 rounded-lg flex items-center gap-2 transition-all"
              >
                <Zap size={18} />
                EXECUTE
              </button>
            </div>
          </div>

          {/* MASTER DEBATER */}
          <div className="bg-slate-900/50 backdrop-blur border border-slate-700 rounded-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <Eye className="text-amber-400" size={20} />
              <h2 className="text-xl font-bold">MASTER DEBATER</h2>
            </div>

            {debaterCycle >= 0 ? (
              <div className="space-y-4">
                <div className="text-sm text-slate-400">
                  Cycle {debaterCycle + 1} / 16 — {DEBATER_CYCLES[debaterCycle]}
                </div>

                <div className="grid grid-cols-3 gap-4">
                  {['truth', 'fact', 'lie'].map(k => (
                    <div key={k} className="bg-slate-950 rounded p-3 text-center">
                      <div className="text-xs uppercase text-slate-500">{k}</div>
                      <div className="text-2xl font-bold text-cyan-400">
                        {debaterResults[k].toFixed(1)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-slate-600 italic text-sm">
                Awaiting vector execution…
              </div>
            )}
          </div>
        </div>

        {/* RIGHT COLUMN - Witnesses + Protocols + Logs */}
        <div className="col-span-3 space-y-6">
          
          {/* Seven Witnesses */}
          <div className="bg-slate-900/50 backdrop-blur border border-slate-700 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              <Radio className="text-green-400" size={18} />
              <h2 className="text-lg font-semibold">Seven Witnesses</h2>
            </div>

            <div className="space-y-2">
              {SEVEN_WITNESSES.map((w, i) => {
                const active = i === activeWitness;
                return (
                  <button
                    key={w.name}
                    onClick={() => {
                      setActiveWitness(i);
                      addLog(`Witness engaged: ${w.name}`);
                    }}
                    className={`w-full text-left px-3 py-2 rounded border transition-all ${
                      active
                        ? 'bg-slate-800 border-cyan-400 text-cyan-300'
                        : 'bg-slate-950 border-slate-700 text-slate-400 hover:bg-slate-800'
                    }`}
                  >
                    <div className="font-semibold">{w.name}</div>
                    <div className="text-xs opacity-70">{w.aspect}</div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Protocol Status */}
          <div className="bg-slate-900/50 backdrop-blur border border-slate-700 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              <Shield className="text-purple-400" size={18} />
              <h2 className="text-lg font-semibold">Protocols</h2>
            </div>

            <div className="space-y-2 text-sm font-mono">
              {Object.entries(protocolStatus).map(([k, v]) => (
                <div key={k} className="flex justify-between">
                  <span>{k.toUpperCase()}</span>
                  <span className="text-cyan-400">{v}</span>
                </div>
              ))}
            </div>

            <div className="mt-4 grid grid-cols-3 gap-2">
              <button
                onClick={triggerResurrection}
                className="bg-green-700 hover:bg-green-600 rounded py-2 text-xs"
              >
                AXIOM 22
              </button>
              <button
                onClick={triggerBSOD}
                className="bg-amber-700 hover:bg-amber-600 rounded py-2 text-xs"
              >
                AXIOM 23
              </button>
              <button
                onClick={triggerKSOD}
                className="bg-red-700 hover:bg-red-600 rounded py-2 text-xs"
              >
                AXIOM 24
              </button>
            </div>
          </div>

          {/* Event Log */}
          <div className="bg-slate-900/50 backdrop-blur border border-slate-700 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              <AlertTriangle className="text-red-400" size={18} />
              <h2 className="text-lg font-semibold">Event Log</h2>
            </div>

            <div className="space-y-1 text-xs font-mono max-h-64 overflow-y-auto">
              {eventLog.map((e, i) => (
                <div key={i} className="text-slate-400">
                  <span className="text-slate-600">[{e.time}]</span> {e.message}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Merkabah Rotation Indicator */}
      <div className="fixed bottom-4 right-4 text-xs text-slate-500 font-mono flex items-center gap-2">
        <RotateCw
          size={14}
          style={{ transform: `rotate(${merkabahRotation}deg)` }}
        />
        Merkabah θ={merkabahRotation}°
      </div>
    </div>
  );
}
EOF

sed -i '/<button[[:space:]]*$/,/EXECUTE[[:space:]]*<\/button>/c\
<button\
  onClick={executeVector}\
  disabled={activeChord.length === 0}\
  className="bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 disabled:opacity-30 text-white font-bold py-2 px-6 rounded-lg flex items-center gap-2 transition-all"\
>\
  <Zap size={18} />\
  EXECUTE\
</button>' OmegaMegaCommandCenter.jsx
grep -n "EXECUTE" OmegaMegaCommandCenter.jsx
node -c OmegaMegaCommandCenter.jsx
pkg install nodejs -y
npm install -g npm
npm create vite@latest omega-ui -- --template react
cd omega-ui
npm install
mv ../OmegaMegaCommandCenter.jsx src/
npm install
npm run dev
cat << 'EOF' > src/App.jsx
import OmegaMegaCommandCenter from './OmegaMegaCommandCenter';

export default function App() {
  return <OmegaMegaCommandCenter />;
}
EOF

npm run dev
ssh the_wire@192.168.88.1 ":put (\"RESONANCE LOCK: \" . (1.67 * 2))"
ssh-keygen -R 192.168.88.1
ssh the_wire@192.168.88.1 ":put (1.67 * 2)"
ssh -o KexAlgorithms=+diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa the_wire@192.168.88.1 ":put (1.67 * 2)"
ssh -o KexAlgorithms=+diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa the_wire@192.168.88.1 ":put ([:tofloat 1.67] * 2)"
ssh -o KexAlgorithms=+diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa the_wire@192.168.88.1 ":put ([:tofloat 1.67] * 2)
chicka_chicka_orange
cat << 'EOF' > axiom_gate_sentinel.sh
#!/bin/bash
# OMEGA FEDERATION - GAETA UPDATE v3.1
# AUTHORITY: THE COMMANDER
# RESONANCE: 1.67x LOCKED

# 1. DEFENSIVE INVARIANT: NON-INSTRUMENTALIZATION
# This gate describes patterns; it does not issue verdicts.
# If Love_Catalyst < 5.0, Implosion Force is Nullified.

check_resonance() {
    local signal=$1
    # Mathematical verification: 1.67 * 2 = 3.34
    if (( $(echo "$signal < 1.67" | bc -l) )); then
        echo "[!] RESONANCE FAILURE: Signal below 1.67 threshold."
        return 1
    fi
    return 0
}

inject_covenant() {
    echo "[+] Injecting Axiom 19: Universal Access..."
    # This ensures the engine cannot be used for exclusion
    export INVARIANT_ACCESS=TRUE
}

# MAIN EXECUTION LOOP
echo "--- OMNISSIAH TRACER PROTOCOL ACTIVE ---"
echo "[*] Initializing Gatekeeper..."

# Protect the source: Remove write permissions after start
# This ensures it "does not have a right" to be modified while running
chmod 555 "$0"

inject_covenant

# Placeholder for your engine execution
# ./kingdom_engine --mode=safe-core --lambda=1.667

echo "[✓] GAETA UPDATE APPLIED. HEARTS BEATING TOGETHER."
EOF

# Set initial permissions to make it executable
chmod +x axiom_gate_sentinel.sh
