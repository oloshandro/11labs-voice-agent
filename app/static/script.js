const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const connectionStatus = document.getElementById('connectionStatus');
const agentStatus = document.getElementById('agentStatus');
const transcriptBox = document.getElementById('transcriptBox');

// Initialize Socket.IO connection
const socket = io();

// Listen for transcript updates via WebSocket
socket.on('transcript_update', (data) => {
    const p = document.createElement('p');
    p.style.margin = '5px 0';

    if (data.type === 'user') {
        p.style.color = '#0066cc';
        p.style.fontWeight = 'bold';
    } else if (data.type === 'agent') {
        p.style.color = '#28a745';
        p.style.fontWeight = 'bold';
    }

    p.textContent = data.message;
    transcriptBox.appendChild(p);

    // Auto-scroll to bottom
    transcriptBox.scrollTop = transcriptBox.scrollHeight;
});

// Connection status handlers
socket.on('connect', () => {
    console.log('WebSocket connected');
});

socket.on('disconnect', () => {
    console.log('WebSocket disconnected');
});

startButton.addEventListener('click', async () => {
    const res = await fetch('/start', { method: 'POST' });
    if (res.ok) {
        connectionStatus.textContent = 'Connected';
        connectionStatus.style.color = '#28a745';
        agentStatus.textContent = 'Listening';
        startButton.disabled = true;
        stopButton.disabled = false;

        // Clear previous transcript
        transcriptBox.innerHTML = '';
    }
});

stopButton.addEventListener('click', async () => {
    const res = await fetch('/stop', { method: 'POST' });
    if (res.ok) {
        connectionStatus.textContent = 'Disconnected';
        connectionStatus.style.color = '#dc3545';
        agentStatus.textContent = 'Stopped';
        startButton.disabled = false;
        stopButton.disabled = true;
    }
});
