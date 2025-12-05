# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 12:30:33 2025

@author: vrhei
"""
#I opted to complete this lab on my local machine instead of the 
#lab environment. You need spacex_launch_dash.csv in the same folder
#as this .py file and view dash at http://127.0.0.1:8050/ in browser

import pandas as pd
import dash
from dash import html #updated import for newer dash version
from dash import dcc #updated import for newer dash version
from dash.dependencies import Input, Output
import plotly.express as px


spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    

    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0',
                           2500: '2500',
                           5000: '5000',
                           7500: '7500',
                           10000: '10000'},
                    value=[min_payload, max_payload]),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    filtered_df = spacex_df[mask]
    
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {entered_site}')
        return fig

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        site_counts = filtered_df['class'].value_counts().reset_index()
        site_counts.columns = ['class', 'count']
        fig = px.pie(site_counts, values='count', 
        names='class', 
        title=f'Total Success Launches for site {entered_site}')
        return fig

if __name__ == '__main__':
    app.run(debug=True) #updated to app.run for newer version of dash