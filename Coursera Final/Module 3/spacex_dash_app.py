# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

site_options=[{'label': 'All Sites', 'value': 'ALL'}]
for site in spacex_df["Launch Site"].unique():
    site_options.append({'label': site, 'value': site})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown', 
                                    options=site_options,
                                    value='ALL',
                                    placeholder = "Select a Launch Site",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='range-slider',
                                    min=0, max=10000, step=1000,
                                    marks={
                                        0: '0',
                                        2500: '2,500',
                                        5000:'5,000',
                                        7500:'7,500',
                                        10000:'10,000'
                                        },
                                    value=[min_payload, max_payload]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
    )
def get_pie_chart(entered_site):
    filtered_data=spacex_df.loc[spacex_df["Launch Site"]==entered_site,:]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df.loc[spacex_df['class']==1,:], 
        values='class', 
        names='Launch Site', 
        title='Total Successful Launches by Site')
        return fig
    else:
        fig = px.pie(filtered_data, 
        values=filtered_data['class'].value_counts().values, 
        names=filtered_data['class'].value_counts().index,
        title=f'Total Successful Launches for Site {entered_site}')
        return fig

@app.callback(
    Output('output-container-range-slider', 'children'),
    Input('range-slider', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(int(value[0]))

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="range-slider", component_property="value"),
    )
def get_scatter_chart(entered_site, payload_range):
    if not entered_site=="ALL":
        df = spacex_df.loc[
            (spacex_df["Launch Site"]==entered_site) &
            (spacex_df["Payload Mass (kg)"]>=int(payload_range[0])) &
            (spacex_df["Payload Mass (kg)"]<=int(payload_range[1]))
            ,:]
    else:
        df=spacex_df.loc[
            (spacex_df["Payload Mass (kg)"]>=int(payload_range[0])) &
            (spacex_df["Payload Mass (kg)"]<=int(payload_range[1]))
        ]
    fig=px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
