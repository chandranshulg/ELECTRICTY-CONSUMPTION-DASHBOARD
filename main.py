from flask import Flask, render_template_string, request, jsonify
import datetime

app = Flask(__name__)

# Mock data storage
electricity_data = []

@app.route('/')
def index():
    # HTML, CSS, and JavaScript combined into a single template
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Electricity Consumption Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
            }
            form {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            form label {
                margin-right: 10px;
            }
            form input {
                margin-right: 10px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            form button {
                padding: 5px 10px;
                background-color: #28a745;
                color: #fff;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            form button:hover {
                background-color: #218838;
            }
            #trendContainer {
                margin-top: 20px;
            }
            canvas {
                max-width: 100%;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Electricity Consumption Dashboard</h1>
            <!-- Form to input electricity usage -->
            <form id="usageForm">
                <label for="date">Date:</label>
                <input type="date" id="date" name="date" required>
                <label for="usage">Usage (kWh):</label>
                <input type="number" id="usage" name="usage" required>
                <button type="submit">Submit</button>
            </form>
            <!-- Area to display the data and trends -->
            <div id="trendContainer">
                <canvas id="usageChart"></canvas>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const form = document.getElementById('usageForm');
                const usageChart = document.getElementById('usageChart').getContext('2d');
                let chart;

                form.addEventListener('submit', function(e) {
                    e.preventDefault();

                    const formData = new FormData(form);
                    fetch('/submit', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            form.reset();
                            fetchDataAndUpdateChart();
                        }
                    });
                });

                function fetchDataAndUpdateChart() {
                    fetch('/data')
                    .then(response => response.json())
                    .then(data => {
                        const dates = data.map(item => item.date);
                        const usages = data.map(item => item.usage);

                        if (chart) {
                            chart.destroy();
                        }

                        chart = new Chart(usageChart, {
                            type: 'line',
                            data: {
                                labels: dates,
                                datasets: [{
                                    label: 'Electricity Usage (kWh)',
                                    data: usages,
                                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 1
                                }]
                            },
                            options: {
                                scales: {
                                    y: {
                                        beginAtZero: true
                                    }
                                },
                                plugins: {
                                    tooltip: {
                                        callbacks: {
                                            label: function(context) {
                                                return context.parsed.y + ' kWh';
                                            }
                                        }
                                    }
                                }
                            }
                        });
                    });
                }

                fetchDataAndUpdateChart();
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/submit', methods=['POST'])
def submit_data():
    usage = request.form['usage']
    date = request.form['date']
    
    # Store the data
    electricity_data.append({'date': date, 'usage': float(usage)})
    
    return jsonify({'status': 'success'})

@app.route('/data')
def get_data():
    # Sort data by date for trend analysis
    sorted_data = sorted(electricity_data, key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'))
    
    return jsonify(sorted_data)

if __name__ == '__main__':
    app.run(debug=True)
