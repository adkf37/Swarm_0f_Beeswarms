# Import necessary libraries
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Load the datasets
url1 = "https://raw.githubusercontent.com/US-CBO/eval-projections/main/output_data/revenue_projection_errors.csv"
url2 = "https://raw.githubusercontent.com/US-CBO/eval-projections/main/output_data/deficit_projection_errors.csv"
url3 = 'https://raw.githubusercontent.com/US-CBO/eval-projections/main/output_data/outlay_projection_errors.csv'

data_revenue = pd.read_csv(url1)
data_deficit = pd.read_csv(url2)
data_outlay = pd.read_csv(url3)

# Combine the datasets
combined_data = pd.concat([data_outlay, data_revenue, data_deficit])

# Initialize the Dash application
app = dash.Dash(__name__)

# Unique values for 'component' and 'subcategory'
components = combined_data['component'].unique()
subcategories = combined_data['subcategory'].unique()

# Define the layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='component-dropdown',
        options=[{'label': comp, 'value': comp} for comp in components],
        value=components[0]  # Set default value to the first component
    ),
    dcc.Dropdown(
        id='subcategory-dropdown',
        # options will be set by callback
    ),
    dcc.Graph(id='projection-graph')
])

# Callback to update subcategory dropdown based on component selection
@app.callback(
    Output('subcategory-dropdown', 'options'),
    Input('component-dropdown', 'value')
)
def set_subcategories_options(selected_component):
    filtered_data = combined_data[combined_data['component'] == selected_component]
    return [{'label': subcat, 'value': subcat} for subcat in filtered_data['subcategory'].unique()]

# Callback to update graph based on dropdowns
@app.callback(
    Output('projection-graph', 'figure'),
    [Input('component-dropdown', 'value'),
     Input('subcategory-dropdown', 'value')]
)
def update_graph(selected_component, selected_subcategory):
    fig = go.Figure()


    # Define color mapping for components
    color_map = {
        'revenue': 'green',
        'outlay':'blue',
        'deficit': 'purple'
        # Add other components and their colors here
        # 'component_name': 'color',
    }

    # Filter data based on selected component and subcategory
    filtered_data = combined_data[(combined_data['component'] == selected_component) & 
                                  (combined_data['subcategory'] == selected_subcategory)]

    # Add traces for the selected component and subcategory
    for year_number in range(1, 12):  # Assuming projected_year_number ranges from 1 to 11
        year_data = filtered_data[filtered_data['projected_year_number'] == year_number]
        fig.add_trace(
            go.Box(
                x=[year_number] * len(year_data),  # Set x-axis values
                y=year_data['projection_error_pct_actual'],
                name=f'{selected_component} - {selected_subcategory} Year {year_number}',
                boxpoints='all',  # To create a beeswarm plot
                jitter=0.5,
                marker_color=color_map.get(selected_component, 'default_color')  # Use the color based on the component
            )
        )
   # Define the range of years for the x-axis
    year_range = list(range(1, 12))  # Adjust this if your year range is different

     # Check if subcategory is None and adjust the title accordingly
    if selected_subcategory is None:
        title = f'{selected_component}'
    else:
        title = f'{selected_component}, {selected_subcategory} Errors, by Projection Year'

    # Update layout for x-axis and title, and remove the legend
    fig.update_layout(
        title=title,
        height=800,
        showlegend=False,  # This removes the legend
        xaxis=dict(
            tickmode='array',
            tickvals=year_range,
            ticktext=[str(year) for year in year_range]
        ),)


    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
