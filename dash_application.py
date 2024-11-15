import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Sample data for the DataFrame based on the description
data = {
    'Date': pd.date_range(start='1980-01-01', periods=480, freq='ME'),
    'Recession': [1 if year in [1980, 1981, 1982, 1991, 2000, 2001, 2007, 2008, 2009, 2020] and month in [1, 2, 3, 4] else 0 
                  for year in range(1980, 2020) for month in range(1, 13)][:480],
    'Automobile_Sales': np.random.randint(1000, 10000, size=480),
    'GDP': np.random.uniform(10000, 60000, size=480),
    'Unemployment_Rate': np.random.uniform(3, 10, size=480),
    'Consumer_Confidence': np.random.uniform(50, 120, size=480),
    'Seasonality_Weight': np.random.uniform(0.5, 1.5, size=480),
    'Price': np.random.uniform(20000, 50000, size=480),
    'Advertising_Expenditure': np.random.uniform(1000, 5000, size=480),
    'Vehicle_Type': np.random.choice(['Supperminicar', 'Smallfamilycar', 'Mediumfamilycar', 'Executivecar', 'Sports'], size=480),
    'Competition': np.random.uniform(1, 10, size=480),
    'Month': pd.date_range(start='1980-01-01', periods=480, freq='ME').month,
    'Year': pd.date_range(start='1980-01-01', periods=480, freq='ME').year
}

# Create a DataFrame
df = pd.DataFrame(data)

# Ensure 'Year' is of type int
df['Year'] = df['Year'].astype(int)

# Initialize the Dash app
app = dash.Dash(__name__)

# Set up the app layout
app.layout = html.Div([
    html.H1("Automobile Sales Recession and Yearly Report Dashboard"),  # Meaningful title

    # Dropdown for vehicle type
    html.Div([
        html.Label("Select Vehicle Type"),
        dcc.Dropdown(
            id='vehicle-type-dropdown',
            options=[
                {'label': 'Supperminicar', 'value': 'Supperminicar'},
                {'label': 'Smallfamilycar', 'value': 'Smallfamilycar'},
                {'label': 'Mediumfamilycar', 'value': 'Mediumfamilycar'},
                {'label': 'Executivecar', 'value': 'Executivecar'},
                {'label': 'Sports', 'value': 'Sports'}
            ],
            value='Supperminicar',  # Default value
            clearable=False
        ),
    ]),

    # Dropdown for year
    html.Div([
        html.Label("Select Year"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in range(1980, 2021)],
            value=2020,  # Default year
            clearable=False
        )
    ]),

    # Output container for selected options
    html.Div(id='output-container', className='output-display'),

    # Graph for Recession Report Statistics
    dcc.Graph(id='recession-report-graph'),  # Recession statistics graph

    # Graph for Yearly Report Statistics
    dcc.Graph(id='yearly-report-graph')  # Yearly statistics graph
])

# Callback to update the output container with selected vehicle type and year
@app.callback(
    Output('output-container', 'children'),
    Input('vehicle-type-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_output(vehicle_type, year):
    return f'You have selected {vehicle_type} for the year {year}.'

# Callback to update the Recession Report Statistics graph
@app.callback(
    Output('recession-report-graph', 'figure'),
    Input('vehicle-type-dropdown', 'value')
)
def update_recession_report_graph(vehicle_type):
    filtered_df = df[(df['Recession'] == 1) & (df['Vehicle_Type'] == vehicle_type)]
    
    # Handle the case where the filtered DataFrame is empty
    if filtered_df.empty:
        return {
            "layout": {
                "title": f'No data available for {vehicle_type} during recession periods.'
            }
        }

    fig = px.line(filtered_df, x='Year', y='Automobile_Sales', title=f'Recession Sales for {vehicle_type}')
    return fig

# Callback to update the Yearly Report Statistics graph
@app.callback(
    Output('yearly-report-graph', 'figure'),
    Input('vehicle-type-dropdown', 'value')
)
def update_yearly_report_graph(vehicle_type):
    filtered_df = df[df['Vehicle_Type'] == vehicle_type]
    
    # Handle the case where the filtered DataFrame is empty
    if filtered_df.empty:
        return {
            "layout": {
                "title": f'No data available for {vehicle_type} for yearly sales.'
            }
        }

    fig = px.line(filtered_df, x='Year', y='Automobile_Sales', title=f'Yearly Sales for {vehicle_type}')
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
