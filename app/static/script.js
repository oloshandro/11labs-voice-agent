const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const connectionStatus = document.getElementById('connectionStatus');
const agentStatus = document.getElementById('agentStatus');

startButton.addEventListener('click', async () => {
    const res = await fetch('/start', { method: 'POST' });
    if (res.ok) {
        connectionStatus.textContent = 'Connected';
        agentStatus.textContent = 'listening';
        startButton.disabled = true;
        stopButton.disabled = false;
    }
});

stopButton.addEventListener('click', async () => {
    const res = await fetch('/stop', { method: 'POST' });
    if (res.ok) {
        connectionStatus.textContent = 'Disconnected';
        agentStatus.textContent = 'stopped';
        startButton.disabled = false;
        stopButton.disabled = true;
    }
});
