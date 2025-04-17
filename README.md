# Taxi Revenue and Trip Analysis Dashboard

This project uses data from New York Taxi trips to visualize key metrics, including average revenue per mile and the number of trips over time. The data is fetched from Google BigQuery, and the dashboard is built using Dash and Plotly.

## Table of Contents

- [Project Description](#project-description)
- [Requirements](#requirements)
- [Installation Instructions](#installation-instructions)
- [Usage](#usage)
- [Running the Application](#running-the-application)
- [Docker Setup](#docker-setup)
- [License](#license)

## Project Description

This dashboard allows users to interactively explore taxi trip data from New York. The application:

- Fetches data from Google BigQuery.
- Displays graphs showing the relationship between revenue per mile and the number of trips over time.
- Provides an interactive date range filter to customize the data displayed.

The project leverages the following technologies:
- **Dash**: A framework for building interactive web applications.
- **Plotly**: A graphing library for creating interactive charts.
- **Google BigQuery**: A cloud-based data warehouse to run SQL queries.

## Requirements

Before running the project, ensure you have the following installed:

- Python 3.7+
- Google Cloud SDK (for BigQuery authentication)
- Docker (if using Docker setup)

You will need the following Python dependencies:
- `dash`
- `plotly`
- `pandas`
- `google-cloud`
- `python-dotenv`

These dependencies are listed in the `requirements.txt` file.

## Installation Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/valenrami5/kiwibot-docker.git
   cd kiwibot-docker
2. Install the Python dependencies:

 ```bash
Copiar
Editar
pip install -r requirements.txt
 ```
3. Set up your Google Cloud credentials:

 Code Explanation
Importing Libraries and Loading Configuration
The code begins by importing several libraries necessary for data manipulation, web development, and BigQuery interaction:

dotenv: Loads environment variables from the .env file.

google.cloud.bigquery: Connects to Google BigQuery to query data.

dash: A framework for creating the web dashboard.

plotly.express and plotly.graph_objects: Used for generating interactive visualizations.

pandas: For data manipulation.

The environment variable GOOGLE_APPLICATION_CREDENTIALS is set using the .env file to authenticate with Google Cloud.

Querying Data from BigQuery
The code queries BigQuery to get taxi trip data. It aggregates the data by trip date, calculating the average revenue per mile and counting the number of trips. The query results are stored in a Pandas DataFrame (df).

Another query fetches a subset of data for basic analysis (average fare, distance, and total earnings).

Building the Dashboard
Using Dash, the code creates a web dashboard that displays:

A DatePickerRange component for users to select a date range.

A Graph component to display the data in an interactive plot.

The graph is updated based on the selected date range using a callback function. The callback takes the selected start and end dates, filters the data accordingly, and updates the graph with a line plot for average revenue per mile and a bar plot for the number of trips.

Plotly Graph Layout
The graph includes two y-axes:

Left Y-axis: Represents the average revenue per mile.

Right Y-axis: Represents the number of trips.

Running the App
Finally, the Dash app runs on the local server (127.0.0.1:8050) and displays the interactive dashboard.

Generated Image
The dashboard generates an interactive graph with the following features:

X-axis: Represents the trip dates, allowing you to view trends over time.

Y-axis (left): Displays the average revenue per mile (a line graph).

Y-axis (right): Displays the number of trips (a bar graph).

When the user selects a date range using the DatePickerRange, the graph dynamically updates to reflect the selected time period.

An example of what the graph might look like is a dual-axis chart with:

A line showing the trend of revenue per mile.

A bar graph showing the number of trips corresponding to each date.

This visualization helps identify patterns in taxi revenue and trip volume over time, which can be useful for business analytics and decision-making.


