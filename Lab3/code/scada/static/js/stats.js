addEventListener("DOMContentLoaded", (event) => {
    RenderErrorChart();
    RenderPuckColorChart();
    RenderTimeChart();
})

function RenderErrorChart() {
    fetch("/get_error_stats")
        .then(response => response.json())
        .then(data => {
                dataset = [data['error'], data['non_error']];

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
            console.error('Error: ', error);
            const textBox = document.getElementById('error-text');
            textBox.textContent = "Error fetching data";
        });
}

function RenderPuckColorChart() {
    fetch("/get_color_stats")
        .then(response => response.json())
        .then(data => {
            dataset = [data['red_count'], data['blue_count'], data['white_count']];
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

}

function RenderTimeChart() {
    fetch("/get_prod_stats")
    .then(response => response.json())
    .then(data => { 
        console.log(data);
        timeData = data['times'];

        time_datasets = [];

        // Populate the time datasets NEED TO MAKE THIS CORRECT. POOL BY SECTION, NOT PUCK
        for(var i = 0; i < timeData.length; i++) {
            curData = timeData[i];
            time_datasets.push([]);
            for(var j = 0; j < curData.length; j++) {
                time_datasets[i].push(curData[j]);
            }
        }

        // Populate the labels
        labels = []
        for(var i = 0; i < timeData.length; i++) {
            labels.push(`Puck ${i}`);
        }

        // Populate the actual datasets
        datasets = [];
        for(var i = 0 ; i < timeData.length; i++) {
            new_data = {};
            new_data['label'] = `Puck ${i}`;
            new_data['data'] = time_datasets[i];

        }

        const ctx = document.getElementById('timeChart');

        new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Category A', 'Category B'], // Your X-axis labels
          datasets: [
            {
              label: 'Section 1',
              data: [25, 40], // Value for the first section
              backgroundColor: 'rgb(255, 99, 132)',
            },
            {
              label: 'Section 2',
              data: [25, 20], // Piled on top of Section 1
              backgroundColor: 'rgb(54, 162, 235)',
            },
            {
              label: 'Section 3',
              data: [25, 30], // Piled on top of Section 2
              backgroundColor: 'rgb(255, 205, 86)',
            },
            {
              label: 'Section 4',
              data: [25, 10], // Piled on top of Section 3 (Total for Category A = 100)
              backgroundColor: 'rgb(75, 192, 192)',
            }
          ]
        },
        options: {
          scales: {
            x: {
              stacked: true, // This stacks the bars horizontally
            },
            y: {
              stacked: true, // This stacks the bars vertically
              beginAtZero: true,
              max: 100 // Optional: forces the chart to always show 100
            }
          }
        }
      });
    })
    .catch(error => {
        console.error('Error: ', error);
    });
}
