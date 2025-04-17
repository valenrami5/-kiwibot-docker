import os
from dotenv import load_dotenv
from google.cloud import bigquery
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

client = bigquery.Client()
query = """
    SELECT
  DATE(pickup_datetime) AS trip_date,
  AVG(fare_amount / trip_distance) AS avg_revenue_per_mile,
  COUNT(*) AS num_trips
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2017`
WHERE trip_distance > 0 AND fare_amount > 0
GROUP BY trip_date
ORDER BY trip_date
LIMIT 100;
"""

df = client.query(query).to_dataframe()
df['trip_date'] = pd.to_datetime(df['trip_date'])
print(df)

query_python = """
    SELECT *
    FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2017`
    WHERE trip_distance > 0 AND fare_amount > 0
    LIMIT 10
"""
df_python = client.query(query_python).to_dataframe()
average_fare = df_python['fare_amount'].mean()
average_distance = df_python['trip_distance'].mean()
print(f"Fare Amount Mean: {average_fare}")
print(f"Trip Distance Mean: {average_distance}")
num_trips = df_python.shape[0]
print(f"Total Trips: {num_trips}")
total_fare = df_python['fare_amount'].sum()
total_distance = df_python['trip_distance'].sum()
print(f"Total earnings: {total_fare}")
print(f"Total distance: {total_distance}")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Taxi Trips: Revenue and Number of Trips"),
    
    dcc.DatePickerRange(
        id='date-range',
        min_date_allowed=df['trip_date'].min(),
        max_date_allowed=df['trip_date'].max(),
        start_date=df['trip_date'].min(),
        end_date=df['trip_date'].max(),
        display_format='YYYY-MM-DD'
    ),

    dcc.Graph(id='revenue-trips-graph')
])

@app.callback(
    Output('revenue-trips-graph', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_graph(start_date, end_date):
    filtered_df = df[(df['trip_date'] >= start_date) & (df['trip_date'] <= end_date)]

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=filtered_df['trip_date'], 
        y=filtered_df['avg_revenue_per_mile'],
        mode='lines+markers',
        name='Avg Revenue per Mile'
    ))
    
    fig.add_trace(go.Bar(
        x=filtered_df['trip_date'],
        y=filtered_df['num_trips'],
        name='Number of Trips',
        yaxis='y2',
        opacity=0.4
    ))
    
    fig.update_layout(
        title='Avg Revenue per Mile and Number of Trips',
        xaxis_title='Date',
        yaxis=dict(title='Revenue per Mile'),
        yaxis2=dict(
            title='Number of Trips',
            overlaying='y',
            side='right'
        ),
        template='plotly_white',
        legend=dict(x=0.01, y=0.99)
    )

    return fig

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)