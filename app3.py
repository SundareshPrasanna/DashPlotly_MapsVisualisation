import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import plotly.express as px
import dash_table

first_dataset = pd.read_excel("test1.xlsx", engine='openpyxl')
first_dataset['type_name'] = 'regular'
second_dataset = pd.read_excel("test2.xlsx", engine='openpyxl')
second_dataset['type_name'] = 'super'
combined_dataset = first_dataset.append(second_dataset, ignore_index=True)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(style={"marginTop": "10px", "marginBottom": "15px"}),
    dcc.RadioItems(
        id='type_of_store',
        options=[{'label': 'Both', 'value': 'both'},
                 {'label': 'Regular', 'value': 'regular'},
                 {'label': 'Super', 'value': 'super'}],
        value='both',
        labelStyle={'display': 'inline-block'},
    ),
    html.Div(style={"marginTop": "10px", "marginBottom": "15px"}),
    html.Div(className='row',
             children=[
                 html.Div(dcc.Graph(id='map_viz'), style={
                          'display': 'inline-block', 'width': '85%'}),
                 html.Div(dcc.Graph(id='indicator_viz'), style={'width': '15%',
                                                                'align-items': 'right', 'justify-content': 'right',
                                                                'vertical-align': 'top', 'display': 'inline-block', 'padding': '0px',
                                                                'margin': '0px'})]),
    html.Div(className='row',
             children=[dash_table.DataTable(
                 id='table_viz',
                 columns=[{'name': i, 'id': i}
                          for i in sorted(combined_dataset.columns)],
                 data=combined_dataset.to_dict('records'),
                 sort_mode='multi',
                 export_format="csv",
                 filter_action='native',
                 style_table={'overflowX': 'scroll',
                              'maxHeight': '400px'},
                 style_header={
                     'backgroundColor': 'rgb(188, 74, 60)', 'color': 'white', },
                 style_cell={'textAlign': 'center',  'backgroundColor': '#e5e4e2',
                             'color': '#36454F',
                             'height': 'auto', 'minWidth': '80px', 'width': '60px', 'maxWidth': '80px',
                             },
                 sort_by=[],
                 style_data={
                     'overflow': 'hidden',
                     'textOverflow': 'ellipsis',
                 })], style={
                 'width': '77.5%'})])


@app.callback(Output("map_viz", "figure"),
              [Input("type_of_store", "value"),
               Input('table_viz', "derived_viewport_data")])
def display_map(type_of_store, filter_value):
    combined_dataset = first_dataset.append(second_dataset, ignore_index=True)
    if (filter_value is not None and len(filter_value) > 0):
        filtered_rows = [x['name'] for x in filter_value]
        combined_dataset = combined_dataset[combined_dataset['name'].isin(
            filtered_rows)]
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
        zoom=9, height=500)
    fig.update_layout(mapbox_style="open-street-map",
                      title='Plotly Visualization - Upwork',
                      height=800,
                      width=1400,
                      margin={"r": 0, "t": 30, "l": 0, "b": 0}
                      )

    return fig


@app.callback([Output("table_viz", "data"), Output("indicator_viz", "figure")],
              [Input("map_viz", "selectedData"),
               Input("type_of_store", "value"),
               Input('table_viz', "derived_viewport_data")])
def callback(selection1, type_of_store, filter_value):
    combined_dataset = first_dataset.append(second_dataset, ignore_index=True)
    if (filter_value is not None and len(filter_value) > 0):
        filtered_rows = [x['name'] for x in filter_value]
        combined_dataset = combined_dataset[combined_dataset['name'].isin(
            filtered_rows)]
    if(selection1 is None):
        if type_of_store != "both":
            combined_dataset = combined_dataset[combined_dataset['type_name']
                                                == type_of_store]
            fig2 = go.Figure()

            fig2.add_trace(go.Indicator(
                mode="number",
                value=combined_dataset.type_name.value_counts()[0],
                title=combined_dataset.type_name.value_counts().index[0],
                domain={'x': [0, 0], 'y': [0, 0]}, align='center'))

        else:
            fig2 = go.Figure()
            fig2.add_trace(go.Indicator(
                mode="number",
                value=combined_dataset.type_name.value_counts()[0],
                title=combined_dataset.type_name.value_counts().index[0],
                domain={'x': [0, 0], 'y': [0, 0.5]},
                align='center'))
            fig2.add_trace(go.Indicator(
                mode="number",
                value=combined_dataset.type_name.value_counts()[1],
                title=combined_dataset.type_name.value_counts().index[1],
                domain={'x': [0, 0], 'y': [0.5, 1]},
                align='center'))
        data = combined_dataset.to_dict('records')

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
                domain={'x': [0, 0], 'y': [0, 0]},
                align='center'))
        if type_of_store == "both":
            selected_points = [x['hovertext'] for x in selection1['points']]
            combined_dataset = combined_dataset[combined_dataset['name'].isin(
                selected_points)]
            if len(selected_points) == 1:
                fig2 = go.Figure()
                fig2.add_trace(go.Indicator(
                    mode="number",
                    value=combined_dataset.type_name.value_counts()[0],
                    title=combined_dataset.type_name.value_counts().index[0],
                    domain={'x': [0, 0], 'y': [0, 0.5]},
                    align='center'))
            else:
                fig2 = go.Figure()
                fig2.add_trace(go.Indicator(
                    mode="number",
                    value=combined_dataset.type_name.value_counts()[0],
                    title=combined_dataset.type_name.value_counts(
                    ).index[0],
                    domain={'x': [0, 0], 'y': [0, 0.5]},
                    align='center'))
                fig2.add_trace(go.Indicator(
                    mode="number",
                    value=combined_dataset.type_name.value_counts()[1],
                    title=combined_dataset.type_name.value_counts().index[1],
                    domain={'x': [0, 0], 'y': [0.5, 1]},
                    align='center'))
        data = combined_dataset.to_dict('records')

    return data, fig2


app.run_server(debug=True, port=8000, host='127.0.0.1')
