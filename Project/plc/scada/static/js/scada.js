document.addEventListener('DOMContentLoaded', () => {
    // Initial fetch and set interval
    fetchLogs();
    setInterval(fetchLogs, 1000);
});

function fetchLogs() {
    const tableBody = document.getElementById('log-table-body');
    const scrollArea = document.getElementById('log-scroll-area');

    fetch('/scada/get_logs/')
        .then(response => response.json())
        .then(data => {
            if (data.new_logs) {
                // 1. Create a DocumentFragment (an off-screen buffer)
                // This is much faster than updating the live DOM in a loop
                const fragment = document.createDocumentFragment();

                data.new_logs.forEach(logString => {
                    const parts = logString.split(']');
                    const timestamp = parts[0] ? parts[0].replace('[', '') : "-";
                    const type = parts[1] ? parts[1].replace('[', '').trim() : "INFO";
                    const message = parts[2] ? parts[2].trim() : logString;

                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><span class="badge ${getTypeClass(type)}">${type}</span></td>
                        <td>${timestamp}</td>
                        <td>${message}</td>
                    `;
                    fragment.appendChild(row);
                });

                // 2. Replace the entire table body content with the buffer
                tableBody.innerHTML = ""; // Clear existing rows
                tableBody.appendChild(fragment); // Inject the new buffer

                // 3. Auto-scroll
                scrollArea.scrollTop = scrollArea.scrollHeight;
            }
        })
        .catch(err => console.error("Polling error:", err));
}

// Helper to color-code the "Type" column based on severity
function getTypeClass(type) {
    const t = type.toUpperCase();
    if (t.includes('ERROR')) return 'bg-danger';
    if (t.includes('WARNING') || t.includes('ESTOP')) return 'bg-warning text-dark';
    if (t.includes('INFO')) return 'bg-info';
    return 'bg-secondary';
}