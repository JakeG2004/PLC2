let sldChart = null;

document.addEventListener('DOMContentLoaded', () => {
    // Initial fetch
    fetchLogs();
    
    // Poll every second to get new data
    setInterval(fetchLogs, 1000);
});

// Primary poll function to get data then update the page
function fetchLogs() {
    const tableBody = document.getElementById('log-table-body');
    const scrollArea = document.getElementById('log-scroll-area');

    fetch('/get_logs/')
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            if (data.new_logs && data.new_logs.length > 0) {
                updateLogTable(tableBody, data.new_logs);
                
                if (scrollArea) {
                    scrollArea.scrollTop = scrollArea.scrollHeight;
                }
            }

            if (data.sld_data) {
                updateChart(data.sld_data);
            }
        })
        .catch(err => console.error("Polling error:", err));
}

// Creates and updates the table on the main page
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

    // Clear the table and insert the new data
    tableBody.innerHTML = "";
    tableBody.appendChild(fragment);
}

// Creates or updates the chart.js instance
function updateChart(sldData) {
    const canvas = document.getElementById('pollingChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    
    const sanitizedData = sldData.map(val => (val > 0 && val < 30000) ? 30000 : val);
    const labels = sanitizedData.map((_, index) => index + 1);

    const activeData = sanitizedData.filter(v => v >= 30000);
    
    let dynamicMin = activeData.length > 0 ? Math.min(...activeData) : 30000;
    let dynamicMax = activeData.length > 0 ? Math.max(...activeData) : 35000;

    const padding = (dynamicMax - dynamicMin) * 0.05;
    dynamicMax += padding;
    dynamicMin -= padding;

    if (sldChart) {
        sldChart.options.scales.y.min = dynamicMin;
        sldChart.options.scales.y.max = dynamicMax;
        
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
                        min: dynamicMin, 
                        max: dynamicMax 
                    }
                }
            }
        });
    }
}

// Gets the color of the bootstrap badge based on the log type
function getTypeClass(type) {
    const t = type.toUpperCase();
    if (t.includes('ERROR') || t.includes('SAFETY')) return 'bg-danger';
    if (t.includes('OPERATION MODE')) return 'bg-warning';
    if (t.includes('COMPLETE')) return 'bg-success';
    if (t.includes('CHECKPOINT')) return 'bg-info';
    return 'bg-primary';
}