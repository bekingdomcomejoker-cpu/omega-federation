const WebSocket = require('ws');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

const PORT = 8765;
const wss = new WebSocket.Server({ port: PORT });

console.log(`[TriNode Bridge] WebSocket server listening on ws://localhost:${PORT}`);

// Connected clients
const clients = new Set();

wss.on('connection', (ws) => {
  console.log('[TriNode Bridge] Client connected');
  clients.add(ws);

  ws.on('message', async (message) => {
    try {
      const msg = JSON.parse(message);
      
      if (msg.type === 'query') {
        console.log(`[TriNode Bridge] Query received: ${msg.data}`);
        
        // Execute all three nodes in parallel
        const [reflex, oracle, warfare] = await Promise.all([
          executeReflex(msg.data),
          executeOracle(msg.data),
          executeWarfare(msg.data),
        ]);

        // Send responses back
        ws.send(JSON.stringify({
          type: 'response',
          node: 'reflex',
          data: reflex,
          lambda: 1.5,
          timestamp: Date.now(),
        }));

        ws.send(JSON.stringify({
          type: 'response',
          node: 'oracle',
          data: oracle,
          lambda: 1.667,
          timestamp: Date.now(),
        }));

        ws.send(JSON.stringify({
          type: 'response',
          node: 'warfare',
          data: warfare,
          lambda: 1.8,
          timestamp: Date.now(),
        }));

        // Consensus
        ws.send(JSON.stringify({
          type: 'response',
          node: 'consensus',
          data: {
            timestamp: Date.now(),
            result: `Consensus: ${reflex.substring(0, 50)}...`,
            lambda: 1.7,
          },
          lambda: 1.7,
          timestamp: Date.now(),
        }));
      }
    } catch (error) {
      console.error('[TriNode Bridge] Error:', error);
      ws.send(JSON.stringify({
        type: 'error',
        data: error.message,
        timestamp: Date.now(),
      }));
    }
  });

  ws.on('close', () => {
    console.log('[TriNode Bridge] Client disconnected');
    clients.delete(ws);
  });
});

async function executeReflex(query) {
  try {
    // Replace with your actual llama.cpp path
    const { stdout } = await execAsync(
      `./llama-cli -m ~/models/qwen-0.5b-chat-q4_k_m.gguf -p "Query: ${query}" -n 96 --temp 0.7`,
      { timeout: 30000 }
    );
    return stdout.trim();
  } catch (error) {
    return `[Reflex Error] ${error.message}`;
  }
}

async function executeOracle(query) {
  try {
    const { stdout } = await execAsync(
      `./llama-cli -m ~/models/gemma-2b-it-q4_k_m.gguf -p "Analyze: ${query}" -n 128 --temp 0.3`,
      { timeout: 30000 }
    );
    return stdout.trim();
  } catch (error) {
    return `[Oracle Error] ${error.message}`;
  }
}

async function executeWarfare(query) {
  try {
    const { stdout } = await execAsync(
      `./llama-cli -m ~/models/deepseek-coder-1.3b-instruct-Q4_K_M.gguf -p "// Task: ${query}" -n 64 --temp 0.1`,
      { timeout: 30000 }
    );
    return stdout.trim();
  } catch (error) {
    return `[Warfare Error] ${error.message}`;
  }
}

// Broadcast status to all clients
setInterval(() => {
  const status = {
    type: 'status',
    data: {
      reflex: { online: true, lastUpdate: Date.now() },
      oracle: { online: true, lastUpdate: Date.now() },
      warfare: { online: true, lastUpdate: Date.now() },
      lambdaHistory: [],
    },
    timestamp: Date.now(),
  };

  clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(status));
    }
  });
}, 30000);

