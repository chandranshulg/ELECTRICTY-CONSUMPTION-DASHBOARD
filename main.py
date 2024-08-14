from flask import Flask, render_template_string, request, jsonify, send_file
import datetime
import csv
import io

app = Flask(__name__)

# Mock data storage
electricity_data = []

# Threshold for usage alert
usage_threshold = 100

@app.route('/')
def index():
    # Updated HTML with new features
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
                transition: background-color 0.3s, color 0.3s;
            }
            body.dark-mode {
                background-color: #333;
                color: #f4f4f4;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .dark-mode .container {
                background-color: #444;
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
            form input, form select {
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
            .summary {
                margin-top: 20px;
            }
            .export-button {
                margin-top: 20px;
                background-color: #007bff;
            }
            .export-button:hover {
                background-color: #0069d9;
            }
            .toggle-button {
                margin-top: 20px;
                background-color: #333;
            }
            .toggle-button:hover {
                background-color: #555;
            }
            .alert {
                color: red;
                font-weight: bold;
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
                <label for="category">Category:</label>
                <select id="category" name="category" required>
                    <option value="Heating">Heating</option>
                    <option value="Cooling">Cooling</option>
                    <option value="Lighting">Lighting</option>
                    <option value="Appliances">Appliances</option>
                    <option value="Other">Other</option>
                </select>
                <button type="submit">Submit</button>
            </form>
            <div id="alerts"></div>
            <!-- Area to display the data and trends -->
            <div id="trendContainer">
                <canvas id="usageChart"></canvas>
            </div>
            <div class="summary">
                <p>Total Usage: <span id="totalUsage">0</span> kWh</p>
                <p>Average Daily Usage: <span id="averageUsage">0</span> kWh</p>
            </div>
            <button class="export-button" onclick="exportData()">Export Data</button>
            <button class="toggle-button" onclick="toggleDarkMode()">Toggle Dark Mode</button>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const form = document.getElementById('usageForm');
                const usageChart = document.getElementById('usageChart').getContext('2d');
                const totalUsageElem = document.getElementById('totalUsage');
                const averageUsageElem = document.getElementById('averageUsage');
                const alertsElem = document.getElementById('alerts');
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
                            checkAlerts();
                        }
                    });
                });

                function fetchDataAndUpdateChart() {
                    fetch('/data')
                    .then(response => response.json())
                    .then(data => {
                        const dates = data.map(item => item.date);
                        const usages = data.map(item => item.usage);
                        const totalUsage = usages.reduce((a, b) => a + b, 0);
                        const averageUsage = (totalUsage / data.length).toFixed(2);

                        totalUsageElem.textContent = totalUsage;
                        averageUsageElem.textContent = averageUsage;

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

                function checkAlerts() {
                    fetch('/data')
                    .then(response => response.json())
                    .then(data => {
                        const lastEntry = data[data.length - 1];
                        if (lastEntry && lastEntry.usage > {{ usage_threshold }}) {
                            alertsElem.innerHTML = '<p class="alert">Alert: High usage detected! (' + lastEntry.usage + ' kWh)</p>';
                        } else {
                            alertsElem.innerHTML = '';
                        }
                    });
                }

                function exportData() {
                    fetch('/export')
                    .then(response => response.blob())
                    .then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'electricity_data.csv';
                        document.body.appendChild(a);
                        a.click();
                        a.remove();
                    });
                }

                function toggleDarkMode() {
                    document.body.classList.toggle('dark-mode');
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
    category = request.form['category']
    
    # Store the data
    electricity_data.append({'date': date, 'usage': float(usage), 'category': category})
    
    return jsonify({'status': 'success'})

@app.route('/data')
def get_data():
    # Sort data by date for trend analysis
    sorted_data = sorted(electricity_data, key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'))
    
    return jsonify(sorted_data)

@app.route('/export')
def export_data():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Usage (kWh)', 'Category'])
    
    for entry in electricity_data:
        writer.writerow([entry['date'], entry['usage'], entry['category']])
    
    output.seek(0)
    
    return send_file(io.BytesIO(output.getvalue().encode('utf-8')), mimetype='text/csv', as_attachment=True, download_name='electricity_data.csv')

if __name__ == '__main__':
    app.run(debug=True)
