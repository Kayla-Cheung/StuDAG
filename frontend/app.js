// app_v3.js
const nodes = new vis.DataSet();
const edges = new vis.DataSet();

const container = document.getElementById('network');
const data = { nodes: nodes, edges: edges };
const options = {
    layout: { hierarchical: { enabled: true, direction: 'UD', sortMethod: 'directed' } },
    physics: { hierarchicalRepulsion: { nodeDistance: 150 } },
    nodes: {
        shape: 'box', margin: 12,
        color: { background: '#1e293b', border: '#475569', highlight: { background: '#2563eb', border: '#60a5fa' } },
        font: { color: '#f8fafc', face: 'Inter' }
    },
    edges: { color: '#64748b', arrows: 'to', smooth: { type: 'cubicBezier' } }
};
const network = new vis.Network(container, data, options);

let ws = null;
let expectedVersion = 0;
let isReconnecting = false;

function connect() {
    if (ws && (ws.readyState === WebSocket.CONNECTING || ws.readyState === WebSocket.OPEN)) return;
    
    ws = new WebSocket(`ws://127.0.0.1:8000/ws`);
    
    ws.onopen = () => {
        console.log('[SSoT Sync] Connected. Awaiting full sync...');
        isReconnecting = false;
    };
    
    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        
        if (msg.type === 'sync') {
            // Self-healing: wipe graph cleanly on a fresh sync (e.g. post-reconnection)
            nodes.clear();
            edges.clear();
            
            expectedVersion = msg.version;
            if (msg.payload.nodes?.add) nodes.add(msg.payload.nodes.add);
            if (msg.payload.edges?.add) edges.add(msg.payload.edges.add);
            console.log(`[SSoT Sync] Graph rebuilt from SSoT. State Version: ${expectedVersion}`);
        } 
        else if (msg.type === 'diff') {
            // Validate continuous state versioning
            if (msg.version !== expectedVersion + 1) {
                console.error(`[SSoT Sync] Chaos Detected! Expected v${expectedVersion+1}, got v${msg.version}. Dropping connection to self-heal.`);
                ws.close(); // Triggers onclose which reconnects
                return;
            }
            expectedVersion = msg.version;
            
            const p = msg.payload;
            if (p.nodes) {
                if (p.nodes.add) nodes.add(p.nodes.add);
                if (p.nodes.update) nodes.update(p.nodes.update);
                if (p.nodes.remove) nodes.remove(p.nodes.remove.map(n => n.id));
            }
            if (p.edges) {
                if (p.edges.add) edges.add(p.edges.add);
                if (p.edges.remove) edges.remove(p.edges.remove.map(e => e.id));
            }
        }
    };
    
    ws.onclose = () => {
        if (!isReconnecting) {
            console.warn('[SSoT Sync] Connection lost. Attempting reconnect in 1s...');
            isReconnecting = true;
            setTimeout(connect, 1000);
        }
    };
}

connect();

function requestAddNode(id, label) { ws.send(JSON.stringify({ action: 'add_node', args: { id, data: { label } } })); }
function requestAddEdge(id, from, to) { ws.send(JSON.stringify({ action: 'add_edge', args: { id, from, to } })); }
