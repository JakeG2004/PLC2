/**
 * Global variable to store the Chart instance.
 * This prevents creating multiple charts on the same canvas during polling.
 */
let sldChart = null;

document.addEventListener('DOMContentLoaded', () => {
    // Initial fetch
    fetchLogs();
    
    // Set interval to poll every 1000ms (1 second)
    setInterval(fetchLogs, 1000);
});

/**
 * Main polling function to retrieve logs and sensor data
 */
function fetchLogs() {
    const tableBody = document.getElementById('log-table-body');
    const scrollArea = document.getElementById('log-scroll-area');

    fetch('/get_logs/')
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            // 1. Handle Log Table Updates
            if (data.new_logs && data.new_logs.length > 0) {
                updateLogTable(tableBody, data.new_logs);
                
                // Auto-scroll to the bottom of the log area
                if (scrollArea) {
                    scrollArea.scrollTop = scrollArea.scrollHeight;
                }
            }

            // 2. Handle SLD Chart Updates
            if (data.sld_data) {
                updateChart(data.sld_data);
            }
        })
        .catch(err => console.error("Polling error:", err));
}

/**
 * Parses log strings and updates the HTML table
 */
function updateLogTable(tableBody, logs) {
    if (!tableBody) return;

    const fragment = document.createDocumentFragment();

    logs.forEach(logString => {
        // Expected format: [Timestamp][Type] Message
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

    tableBody.innerHTML = ""; // Clear existing rows
    tableBody.appendChild(fragment); // Inject the new buffer
}

/**
 * Initializes or updates the Chart.js instance
 */
function updateChart(sldData) {
    const canvas = document.getElementById('pollingChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    
    // Create simple labels (1, 2, 3...) based on the data index
    const labels = sldData.map((_, index) => index + 1);

    if (sldChart) {
        // If chart already exists, update data and labels
        sldChart.data.labels = labels;
        sldChart.data.datasets[0].data = sldData;
        
        // Use 'none' mode to skip animations for better performance during fast polling
        sldChart.update('none'); 
    } else {
        // First time initialization
        sldChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'SLD Sensor Values',
                    data: sldData,
                    borderColor: 'rgb(0, 153, 255)',
                    backgroundColor: 'rgba(0, 153, 255, 0.1)',
                    borderWidth: 2,
                    tension: 0.3, // Curve the lines slightly
                    fill: true,
                    pointRadius: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false, // Disable animations for real-time feel
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Value' }
                    },
                    x: {
                        title: { display: true, text: 'Sample #' }
                    }
                },
                plugins: {
                    legend: { display: true, position: 'top' }
                }
            }
        });
    }
}

/**
 * Helper to color-code the Bootstrap badges based on log type
 */
function getTypeClass(type) {
    const t = type.toUpperCase();
    if (t.includes('ERROR') || t.includes('SAFETY')) return 'bg-danger';
    if (t.includes('OPERATION MODE')) return 'bg-warning';
    if (t.includes('COMPLETE')) return 'bg-success';
    if (t.includes('CHECKPOINT') || t.includes('PROGRESS')) return 'bg-info';
    return 'bg-primary';
}