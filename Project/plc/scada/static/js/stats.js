document.addEventListener("DOMContentLoaded", (event) => {
    FillTimeSinceLastError();
    FillUptime();
    RenderErrorChart();
    RenderPuckColorChart();
    RenderTimeChart();
});

function FillTimeSinceLastError() {
    fetch("/get_time_since_last_error/")
        .then(response => response.json())
        .then(data => {
            let error_time = data['Seconds'];
            if(error_time < 0) {
                document.getElementById('safety-time').innerHTML = "No Safety Logs Found";
                return;
            }

            let minutes = Math.round(error_time / 60);
            let seconds = error_time % 60;
            let hours = Math.round(minutes / 60);
            minutes = minutes % 60;

            let minutes_text = minutes < 10 ? `0${minutes}` : minutes;
            let seconds_text = seconds < 10 ? `0${seconds}` : seconds;
            let hours_text = hours < 10 ? `0${hours}` : hours;

            document.getElementById('safety-time').innerHTML = `${hours_text}:${minutes_text}:${seconds_text}`;
        })
        .catch(error => {
            console.error('Error in FillTimeSinceLastError:', error);
        });
}

function FillUptime() {
    fetch("/get_uptime/")
        .then(response => response.json())
        .then(data => {
            let error_time = data['Seconds'];

            let minutes = Math.round(error_time / 60);
            let seconds = error_time % 60;
            let hours = Math.round(minutes / 60);
            minutes = minutes % 60;

            let minutes_text = minutes < 10 ? `0${minutes}` : minutes;
            let seconds_text = seconds < 10 ? `0${seconds}` : seconds;
            let hours_text = hours < 10 ? `0${hours}` : hours;

            document.getElementById('uptime').innerHTML = `${hours_text}:${minutes_text}:${seconds_text}`;
        })
        .catch(error => {
            console.error('Error in FillTimeSinceLastError:', error);
        });
}

function RenderErrorChart() {
    fetch("/get_error_stats")
        .then(response => response.json())
        .then(data => {
            // Locked with 'const'
            const dataset = [data['error'], data['non_error']];

            const ctx = document.getElementById('errorChart');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Error', 'Not Error'],
                    datasets: [{
                        label: 'All Logs',
                        data: dataset,
                        backgroundColor: [
                            'rgb(255, 0, 55)',
                            'rgb(0, 153, 255)',
                        ],
                        hoverOffset: 4
                    }]
                },
            });
        })
        .catch(error => {
            console.error('Error in RenderErrorChart:', error);
            const textBox = document.getElementById('error-text');
            if (textBox) textBox.textContent = "Error fetching data";
        });
}

function RenderPuckColorChart() {
    fetch("/get_color_stats")
        .then(response => response.json())
        .then(data => {
            // Locked with 'const'
            const dataset = [data['red_count'], data['blue_count'], data['white_count']];
            const ctx = document.getElementById('colorChart');

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Red', 'Blue', 'White'],
                    datasets: [{
                        label: 'Puck Colors',
                        data: dataset,
                        backgroundColor: [
                            'rgb(255, 0, 55)',
                            'rgb(0, 153, 255)',
                            'rgb(178, 178, 178)',
                        ],
                        hoverOffset: 4
                    }]
                },
            });
        })
        .catch(error => {
            console.error('Error in RenderPuckColorChart:', error);
        });
}

function RenderTimeChart() {
    fetch("/get_prod_stats")
        .then(response => response.json())
        .then(data => { 
            // Locked with 'const'
            const timeData = data['times'];
            const time_datasets = [];

            // Used 'let i' and 'let j' for block-level scope
            for(let i = 0; i < 4; i++) {
                const cur_dataset = [];
                for(let j = 0; j < timeData.length; j++) {
                    cur_dataset.push(timeData[j][i]);
                }
                time_datasets.push(cur_dataset);
            }

            const num_entries = time_datasets[0].length;

            // Locked labels array
            const labels = [];
            for(let i = 0; i < num_entries; i++) {
                labels.push(`Puck ${i}`);
            }

            // Locked dataset arrays and config
            const datasets = [];
            const colors = ['rgb(255, 0, 55)', 'rgb(0, 153, 255)', 'rgb(255, 179, 2)', 'rgb(35, 192, 0)'];
            const sections = ["MPO Oven", "Mpo Gripper", "MPO Turntable", "SLD"];

            for(let i = 3 ; i >= 0; i--) {
                const new_data = {
                    label: sections[3 - i],
                    data: time_datasets[i],
                    backgroundColor: colors[i]
                };
                datasets.push(new_data);
            }

            const ctx = document.getElementById('timeChart');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels, // Uses the cleaned up labels array
                    datasets: datasets
                },
                options: {
                    scales: {
                        x: { stacked: true },
                        y: { stacked: true, beginAtZero: true }
                    }
                }
            });

            // Figure out the averages and show
            const avg_times = [];
            let total_avg = 0;
            
            for(let i = 0; i < 4; i++) {
                let cur_sum = 0;
                for(let j = 0; j < num_entries; j++) {
                    cur_sum += time_datasets[i][j];
                }

                let rounded_time = (cur_sum / num_entries);
                avg_times.push(rounded_time.toFixed(2));
                total_avg += Number(rounded_time.toFixed(2));
            }

            document.getElementById("avg-total").innerHTML = `Total processing time: ${total_avg.toFixed(2)} seconds`;
            document.getElementById("avg-oven").innerHTML = `MPO Oven processing time: ${avg_times[3]} seconds`;
            document.getElementById("avg-gripper").innerHTML = `MPO Gripper processing time: ${avg_times[2]} seconds`;
            document.getElementById("avg-turntable").innerHTML = `MPO Turntable processing time: ${avg_times[1]} seconds`;
            document.getElementById("avg-sld").innerHTML = `SLD processing time: ${avg_times[0]} seconds`;
        })
        .catch(error => {
            console.error('Error in RenderTimeChart:', error);
        });
}