import plotly.graph_objects as go
import pandas as pd

# Load the datasets from the URLs
url3 = 'https://raw.githubusercontent.com/US-CBO/eval-projections/main/output_data/outlay_projection_errors.csv'  # Replace with your file path
url1 = "https://raw.githubusercontent.com/US-CBO/eval-projections/main/output_data/revenue_projection_errors.csv"
url2 = "https://raw.githubusercontent.com/US-CBO/eval-projections/main/output_data/deficit_projection_errors.csv"

data_revenue = pd.read_csv(url1)
data_deficit = pd.read_csv(url2)
data_outlay = pd.read_csv(url3)

combined_data = pd.concat([data_outlay, data_revenue, data_deficit])

# Filter data for unique subcategories and components for dropdowns
components = combined_data['component'].unique()
subcategories = combined_data['subcategory'].unique()

# Create a figure with a dropdown menu
fig = go.Figure()

# Add traces (beeswarm plots) for each projected year number within each subcategory
for subcat in subcategories:
    subcat_data = combined_data[combined_data['subcategory'] == subcat]
    for year_number in range(1, 12):  # Assuming projected_year_number ranges from 1 to 11
        filtered_data = subcat_data[subcat_data['projected_year_number'] == year_number]
        fig.add_trace(
            go.Box(
                y=filtered_data['projection_error_pct_actual'],
                name=f'{subcat} Year {year_number}',
                boxpoints='all',  # To create a beeswarm plot
                jitter=0.5,
                visible=(subcat == subcategories[0])  # Show the first subcategory by default
            )
        )

# Update dropdown menus
fig.update_layout(
    updatemenus=[
        {
            'buttons': [
                {
                    'method': 'update',
                    'label': subcat,
                    'args': [{'visible': [trace.name.startswith(subcat) for trace in fig.data]}]
                } for subcat in subcategories
            ],
            'direction': 'down',
            'showactive': True,
        }
    ],
    yaxis_title='Projection Error Percentage (Actual)'
)

# Show the figure
fig.show()

# This code creates an interactive plot with a dropdown to select different subcategories.
# Each subcategory will display 11 beeswarm plots based on the 'projected_year_number' column.
