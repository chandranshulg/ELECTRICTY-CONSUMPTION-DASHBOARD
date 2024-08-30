# Electricity Consumption Dashboard

This web application is designed to track and monitor electricity usage over time. It allows users to input daily electricity consumption, view trends, receive usage alerts, and export the data for further analysis.

## Overview

The Electricity Consumption Dashboard helps users monitor their electricity usage by allowing them to input daily consumption values. The application then visualizes the data using a line chart, calculates total and average usage, and alerts users if their usage exceeds a defined threshold. Additionally, users can export their electricity data as a CSV file for offline analysis.

## Features

- **Usage Input:** Users can input daily electricity usage, along with the category (e.g., Heating, Cooling, Lighting).
- **Real-Time Data Visualization:** Displays electricity usage trends over time using a line chart.
- **Usage Alerts:** Provides alerts if the daily usage exceeds a predefined threshold.
- **Dark Mode Toggle:** Allows users to switch between light and dark mode for better visibility and user comfort.
- **Data Export:** Users can export their electricity usage data as a CSV file.

## How to Use

1. Clone the repository or download the code.
2. Install Flask:
    ```bash
    pip install Flask
    ```
3. Run the application:
    ```bash
    python app.py
    ```
4. Open your web browser and go to `http://127.0.0.1:5000/` to access the dashboard.
5. Input your daily electricity usage and view trends over time.

## Technologies Used

- **Flask:** A lightweight Python web framework for building the web server.
- **HTML5 & CSS3:** For structuring and styling the dashboard interface.
- **JavaScript:** For handling form submissions, fetching data, and updating the chart.
- **Chart.js:** A JavaScript library used for creating the line chart to visualize electricity usage data.

## Future Enhancements

- **Detailed Analytics:** Add more detailed analytics, such as usage breakdown by category or peak usage times.
- **User Authentication:** Implement user authentication to save data for different users separately.
- **Interactive Charts:** Allow users to interact with the charts, such as filtering data by date or category.

## License

This project is open-source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## Author

Created by Chandranshu.
