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
    
    // 1. Sanitize: 0 stays 0, everything else is at least 30,000
    const sanitizedData = sldData.map(val => (val > 0 && val < 30000) ? 30000 : val);
    const labels = sanitizedData.map((_, index) => index + 1);

    const activeData = sanitizedData.filter(v => v >= 30000);
    
    let dynamicMin = activeData.length > 0 ? Math.min(...activeData) : 30000;
    let dynamicMax = activeData.length > 0 ? Math.max(...activeData) : 35000;

    // Add a little "padding" (e.g., 5%) so the line isn't touching the very top/bottom
    const padding = (dynamicMax - dynamicMin) * 0.05;
    dynamicMax += padding;
    dynamicMin -= padding;

    if (sldChart) {
        // Update scales dynamically
        sldChart.options.scales.y.min = dynamicMin; // Always keep 0 visible for "lost connection"
        
        sldChart.data.labels = labels;
        sldChart.data.datasets[0].data = sanitizedData;
        sldChart.update('none'); 
    } else {
        sldChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'SLD Sensor Values',
                    data: sanitizedData,
                    borderColor: 'rgb(0, 153, 255)',
                    fill: true,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        // The core settings for your requirement:
                        min: dynamicMin, 
                        // setting suggestedMax allows it to grow with the data
                        max: dynamicMax 
                    }
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
    if (t.includes('CHECKPOINT')) return 'bg-info';
    return 'bg-primary';
}