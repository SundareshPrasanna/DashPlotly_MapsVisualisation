import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import plotly.express as px

first_dataset = pd.read_excel("test1.xlsx", engine='openpyxl')
first_dataset['type_name'] = 'regular'
second_dataset = pd.read_excel("test2.xlsx", engine='openpyxl')
second_dataset['type_name'] = 'super'

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.RadioItems(
        id='type_of_store',
        options=[{'label': 'Both', 'value': 'both'},
                 {'label': 'Regular', 'value': 'regular'},
                 {'label': 'Super', 'value': 'super'}],
        value='both',
        labelStyle={'display': 'inline-block'},
    ),
    html.Div(style={"margin-top": "10px", "margin-bottom": "15px"}),
    html.Div(dcc.Graph(id='map_viz'), style={'width': '100%', 'display': 'flex',
                                             'align-items': 'center', 'justify-content': 'center'}),
    html.Div(dcc.Graph(id='table_viz'), style={
             'width': '50%', 'display': 'inline-block'}),
    html.Div(dcc.Graph(id='indicator_viz'), style={
             'width': '50%', 'display': 'inline-block'})
])


@app.callback(Output("map_viz", "figure"),
              [Input("type_of_store", "value")])
def display_map(type_of_store):
    combined_dataset = first_dataset.append(second_dataset, ignore_index=True)
    if type_of_store != "both":
        combined_dataset = combined_dataset[combined_dataset['type_name']
                                            == type_of_store]
    fig = px.scatter_mapbox(
        combined_dataset,
        lon='lon',
        lat='lat',
        hover_name='name',
        color='type_name',
        hover_data=['name', 'address'],
        zoom=9, height=300)
    fig.update_layout(mapbox_style="open-street-map",
                      title='Plotly Visualization - Upwork',
                      height=600,
                      width=1200,
                      margin={"r": 0, "t": 30, "l": 0, "b": 0}
                      )

    return fig


@app.callback([Output("table_viz", "figure"), Output("indicator_viz", "figure")],
              [Input("map_viz", "selectedData"),
               Input("type_of_store", "value")])
def callback(selection1, type_of_store):
    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
    if(selection1 is None):
        combined_dataset = first_dataset.append(
            second_dataset, ignore_index=True)
        if type_of_store != "both":
            combined_dataset = combined_dataset[combined_dataset['type_name']
                                                == type_of_store]
            fig2 = go.Figure()

            fig2.add_trace(go.Indicator(
                mode="number",
                value=combined_dataset.type_name.value_counts()[0],
                title=combined_dataset.type_name.value_counts().index[0],
                domain={'x': [0, 0], 'y': [0, 0]}))
        else:
            fig2 = go.Figure()

            fig2.add_trace(go.Indicator(
                mode="number",
                value=combined_dataset.type_name.value_counts()[0],
                title=combined_dataset.type_name.value_counts().index[0],
                domain={'x': [0, 0], 'y': [0, 0.5]}))
            fig2.add_trace(go.Indicator(
                mode="number",
                value=combined_dataset.type_name.value_counts()[1],
                title=combined_dataset.type_name.value_counts().index[1],
                domain={'x': [0, 0], 'y': [0.5, 1]}))
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(combined_dataset.columns),
                        fill_color=headerColor,
                        align='left'),
            cells=dict(values=[combined_dataset.type_name,
                               combined_dataset.name, combined_dataset.address,
                               combined_dataset.lat, combined_dataset.lon],
                       line_color='darkslategray', font=dict(color='darkslategray', size=11),
                       align='left', fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor]*5],))])
    else:
        combined_dataset = first_dataset.append(
            second_dataset, ignore_index=True)
        if type_of_store != "both":
            combined_dataset = combined_dataset[combined_dataset['type_name']
                                                == type_of_store]
            selected_points = [x['hovertext'] for x in selection1['points']]
            combined_dataset = combined_dataset[combined_dataset['name'].isin(
                selected_points)]
            fig2 = go.Figure()
            fig2.add_trace(go.Indicator(
                mode="number",
                value=combined_dataset.type_name.value_counts()[0],
                title=combined_dataset.type_name.value_counts().index[0],
                domain={'x': [0, 0], 'y': [0, 0]}))
        if type_of_store == "both":
            selected_points = [x['hovertext'] for x in selection1['points']]
            combined_dataset = combined_dataset[combined_dataset['name'].isin(
                selected_points)]
            fig2 = go.Figure()
            fig2.add_trace(go.Indicator(
                mode="number",
                value=combined_dataset.type_name.value_counts()[0],
                title=combined_dataset.type_name.value_counts().index[0],
                domain={'x': [0, 0], 'y': [0, 0.5]}))
            fig2.add_trace(go.Indicator(
                mode="number",
                value=combined_dataset.type_name.value_counts()[1],
                title=combined_dataset.type_name.value_counts().index[1],
                domain={'x': [0, 0], 'y': [0.5, 1]}))
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(combined_dataset.columns),
                        fill_color=headerColor,
                        align='left'),
            cells=dict(values=[combined_dataset.type_name, combined_dataset.name, combined_dataset.address, combined_dataset.lat, combined_dataset.lon],
                       line_color='darkslategray', font=dict(color='darkslategray', size=11),
                       align='left', fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor]*5],))])

    return fig, fig2


app.run_server(debug=True, port=8000, host='127.0.0.1')
