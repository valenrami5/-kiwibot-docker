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

class BigQueryClient:
    def __init__(self):
        self.client = bigquery.Client()

    def get_trip_data(self):
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
        return self.client.query(query).to_dataframe()

    def get_sample_data(self):
        query = """
        SELECT *
        FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2017`
        WHERE trip_distance > 0 AND fare_amount > 0
        LIMIT 10
        """
        return self.client.query(query).to_dataframe()


class TaxiDataAnalyzer:
    def __init__(self, bigquery_client):
        self.df = bigquery_client.get_trip_data()
        self.df['trip_date'] = pd.to_datetime(self.df['trip_date'])
        self.sample_df = bigquery_client.get_sample_data()

    def basic_stats(self):
        avg_fare = self.sample_df['fare_amount'].mean()
        avg_distance = self.sample_df['trip_distance'].mean()
        total_trips = self.sample_df.shape[0]
        total_earnings = self.sample_df['fare_amount'].sum()
        total_distance = self.sample_df['trip_distance'].sum()

        print(f"Fare Amount Mean: {avg_fare}")
        print(f"Trip Distance Mean: {avg_distance}")
        print(f"Total Trips: {total_trips}")
        print(f"Total earnings: {total_earnings}")
        print(f"Total distance: {total_distance}")


class TaxiDashboard:
    def __init__(self, df):
        self.df = df
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        self.app.layout = html.Div([
            html.H2("Taxi Trips: Revenue and Number of Trips"),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=self.df['trip_date'].min(),
                max_date_allowed=self.df['trip_date'].max(),
                start_date=self.df['trip_date'].min(),
                end_date=self.df['trip_date'].max(),
                display_format='YYYY-MM-DD'
            ),
            dcc.Graph(id='revenue-trips-graph')
        ])

    def setup_callbacks(self):
        @self.app.callback(
            Output('revenue-trips-graph', 'figure'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date')
        )
        def update_graph(start_date, end_date):
            filtered_df = self.df[(self.df['trip_date'] >= start_date) & (self.df['trip_date'] <= end_date)]

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

    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    bq_client = BigQueryClient()
    analyzer = TaxiDataAnalyzer(bq_client)
    analyzer.basic_stats()

    dashboard = TaxiDashboard(analyzer.df)
    dashboard.run()