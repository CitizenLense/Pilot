import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests

# Configurations
USE_MOCK_DATA = False
API_URL = "http://127.0.0.1:5001/api/sentiment"
PROJECTS_API_URL = "http://127.0.0.1:5001/api/projects"

# Fetch project options dynamically from the API
def get_project_options():
    try:
        response = requests.get(PROJECTS_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching project options: {e}")
        return []

# Fetch and update project options dynamically
project_options = get_project_options()

def fetch_sentiment_data(project_ids=None, start_date=None, end_date=None):
    """Fetch data either from mock data or live API based on the USE_MOCK_DATA flag."""
    if USE_MOCK_DATA:
        # Placeholder mock data fetch function here
        return pd.DataFrame()  # Replace with actual mock data if needed
    else:
        try:
            params = {"project_ids": project_ids, "start_date": start_date, "end_date": end_date}
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return pd.DataFrame(data)
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return pd.DataFrame()

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Mathare Constituency CDF Projects - Sentiment Dashboard", style={'text-align': 'center', 'padding': '20px'}),

    # Filters Section
    html.Div([
        html.Div([
            html.Label("Select Project(s)"),
            dcc.Dropdown(id='project-dropdown', options=project_options, multi=True, placeholder="Select Projects"),
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label("Select Date Range"),
            dcc.DatePickerRange(id='date-picker', display_format='YYYY-MM-DD'),
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px', 'text-align': 'right'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'padding': '20px', 'backgroundColor': '#f0f2f5', 'borderRadius': '10px'}),

    # Summary Metrics in Card Format
    html.Div(id='summary-metrics', style={'padding': '20px', 'display': 'flex', 'justify-content': 'center'}),

    # Graphs Section with Tooltips
    html.Div([
        html.H3("Sentiment Trend Over Time", style={'text-align': 'center'}),
        html.Div("Showing daily sentiment counts with a 7-day moving average", style={'text-align': 'center', 'fontSize': '12px', 'color': 'gray'}),
        dcc.Graph(id='sentiment-trend-graph'),

        html.H3("Project-Specific Sentiment Breakdown", style={'text-align': 'center', 'margin-top': '40px'}),
        html.Div("Comparison of positive and negative feedback for each project", style={'text-align': 'center', 'fontSize': '12px', 'color': 'gray'}),
        dcc.Graph(id='project-sentiment-bar-graph'),
    ], style={'padding': '20px'}),
])

@app.callback(
    [Output('sentiment-trend-graph', 'figure'),
     Output('project-sentiment-bar-graph', 'figure'),
     Output('summary-metrics', 'children')],
    [Input('project-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_visualizations(selected_projects, start_date, end_date):
    """Update sentiment trend, project-specific bar graph, and summary metrics."""
    df = fetch_sentiment_data(selected_projects, start_date, end_date)
    
    if df.empty:
        return {}, {}, html.Div("No data available", style={'font-size': '18px', 'color': 'gray', 'text-align': 'center'})

    # *Sentiment Trend Over Time*
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_sentiment = df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
    daily_sentiment = daily_sentiment.rolling(window=7, min_periods=1).mean()

    trend_fig = px.line(
        daily_sentiment,
        x=daily_sentiment.index,
        y=['positive', 'negative'],
        title="Sentiment Trend Over Time (7-day Moving Average)",
        labels={'value': 'Sentiment Count', 'date': 'Date'}
    )
    trend_fig.update_layout(legend_title_text="Sentiment Type", xaxis_title="Date", yaxis_title="Count")

    # *Project-Specific Sentiment Breakdown*
    project_sentiments = df.groupby(['project_name', 'sentiment']).size().unstack(fill_value=0)
    sentiment_bar_fig = px.bar(
        project_sentiments,
        x=project_sentiments.index,
        y=['positive', 'negative'],
        title="Project-Specific Sentiment Breakdown",
        labels={'value': 'Feedback Count', 'x': 'Project Name'},
        barmode='stack'
    )
    sentiment_bar_fig.update_layout(legend_title_text="Sentiment Type", xaxis_title="Project", yaxis_title="Count")

    # *Summary Metrics in Card Format*
    pos_count = df[df['sentiment'] == 'positive'].shape[0]
    neg_count = df[df['sentiment'] == 'negative'].shape[0]
    total = len(df)
    pos_percentage = (pos_count / total * 100) if total > 0 else 0
    neg_percentage = (neg_count / total * 100) if total > 0 else 0

    summary_cards = html.Div([
        html.Div([
            html.H4("Total Feedback"),
            html.P(f"{total}", style={'font-size': '22px', 'margin': '0'}),
        ], className='card'),
        
        html.Div([
            html.H4("Positive Feedback"),
            html.P(f"{pos_count} ({pos_percentage:.1f}%)", style={'font-size': '22px', 'margin': '0'}),
        ], className='card'),
        
        html.Div([
            html.H4("Negative Feedback"),
            html.P(f"{neg_count} ({neg_percentage:.1f}%)", style={'font-size': '22px', 'margin': '0'}),
        ], className='card'),
    ], style={'display': 'flex', 'gap': '20px', 'justify-content': 'center'})

    return trend_fig, sentiment_bar_fig, summary_cards

if __name__ == '__main__':
    app.run_server(debug=True)
