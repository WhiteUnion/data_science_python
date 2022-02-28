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
sites=spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': sites[0], 'value': sites[0]},
                                                    {'label': sites[1], 'value': sites[1]},
                                                    {'label': sites[2], 'value': sites[2]},
                                                    {'label': sites[3], 'value': sites[3]},
                                                ],
                                                value='ALL',
                                                placeholder="Choose Site Here",
                                                searchable=True
                                                ),


                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',2000: '2000Kg',4000: '4000Kg',6000: '6000Kg',8000: '8000Kg',
                                    10000: '10000Kg'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Br(),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title=entered_site)
        return fig
    else:
        else_df= filtered_df[filtered_df['Launch Site']==entered_site]
        fig = px.pie(else_df, 
        names='class', 
        title=entered_site)
        return fig


# TASK 4:

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),Input(component_id="payload-slider", component_property="value")]
)

def get_scatter_plot(entered_site,entered_payload):
    low,high = entered_payload
    filtered_df = spacex_df

    if entered_site == 'ALL':
            mask = (filtered_df['Payload Mass (kg)'] > low)&(filtered_df['Payload Mass (kg)'] < high)
            fig = px.scatter(
            filtered_df[mask], x="Payload Mass (kg)", y="class", 
            color="Booster Version Category",
            title= 'Payload vs sucsess rate for ' + entered_site,
            hover_data=['Launch Site'])
    else:
            mask = (filtered_df['Payload Mass (kg)'] > low)&(filtered_df['Payload Mass (kg)'] < high)&(filtered_df['Launch Site'] == entered_site) 
            fig = px.scatter(
            filtered_df[mask], x="Payload Mass (kg)", y="class", 
            color="Booster Version Category",
            title= 'Payload vs sucsess rate for ' + entered_site,
            hover_data=['Payload Mass (kg)'])
    
    return fig



# Run the appVAFB SLC-4E
if __name__ == '__main__':
    app.run_server()
