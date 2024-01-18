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

# Unique values for 'component' and 'subcategory'
components = combined_data['component'].unique()
subcategories = combined_data['subcategory'].unique()

# Create a figure with dropdown menus
fig = go.Figure()

# Add traces for each combination of component, subcategory, and year
for comp in components:
    for subcat in subcategories:
        subcat_data = combined_data[(combined_data['component'] == comp) & (combined_data['subcategory'] == subcat)]
        for year_number in range(1, 12):  # Assuming projected_year_number ranges from 1 to 11
            filtered_data = subcat_data[subcat_data['projected_year_number'] == year_number]
            fig.add_trace(
                go.Box(
                    y=filtered_data['projection_error_pct_actual'],
                    name=f'{comp} - {subcat} Year {year_number}',
                    boxpoints='all',  # To create a beeswarm plot
                    jitter=0.5,
                    visible=(comp == components[0]) and (subcat == subcategories[0])  # Show the first component and subcategory by default
                )
            )

# Dropdown for selecting 'Component'
component_buttons = [{'label': comp, 'method': 'update', 'args': [{'visible': [trace.name.startswith(comp) for trace in fig.data]}]} for comp in components]

# Dropdown for selecting 'Subcategory'
# Note: This dropdown's functionality depends on the JavaScript callback to update based on the 'component' selection
subcategory_buttons = [{'label': subcat, 'method': 'update', 'args': [{'visible': [subcat in trace.name for trace in fig.data]}]} for subcat in subcategories]

# Update layout with the new dropdowns
fig.update_layout(
    updatemenus=[
        {'buttons': component_buttons, 'direction': 'down', 'showactive': True, 'x': 0.1, 'xanchor': 'left', 'y': 1.15, 'yanchor': 'top'},
        {'buttons': subcategory_buttons, 'direction': 'down', 'showactive': True, 'x': 0.3, 'xanchor': 'left', 'y': 1.15, 'yanchor': 'top'}
    ],
    yaxis_title='Projection Error Percentage (Actual)'
)

# Show the figure
fig.show()
