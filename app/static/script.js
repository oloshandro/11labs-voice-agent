const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const connectionStatus = document.getElementById('connectionStatus');
const agentStatus = document.getElementById('agentStatus');
const transcriptBox = document.getElementById('transcriptBox');

let transcriptIndex = 0;
let pollingInterval = null;

// Function to fetch and display new transcript entries
async function pollTranscript() {
    try {
        const res = await fetch(`/transcript?start=${transcriptIndex}`);
        if (!res.ok) return;

        const data = await res.json();

        // Append new transcript lines
        data.transcript.forEach(line => {
            const p = document.createElement('p');
            p.style.margin = '5px 0';

            if (line.startsWith('User:')) {
                p.style.color = '#0066cc';
                p.style.fontWeight = 'bold';
            } else if (line.startsWith('Agent:')) {
                p.style.color = '#28a745';
                p.style.fontWeight = 'bold';
            }

            p.textContent = line;
            transcriptBox.appendChild(p);
        });

        // Update the index
        transcriptIndex = data.total;

        // Auto-scroll to bottom
        transcriptBox.scrollTop = transcriptBox.scrollHeight;
    } catch (error) {
        console.error('Error fetching transcript:', error);
    }
}

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
        transcriptIndex = 0;

        // Start polling every 3 seconds (longer interval to reduce load)
        pollingInterval = setInterval(pollTranscript, 3000);
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

        // Stop polling
        if (pollingInterval) {
            clearInterval(pollingInterval);
            pollingInterval = null;
        }

        // Final poll to get remaining transcript
        await pollTranscript();
    }
});
