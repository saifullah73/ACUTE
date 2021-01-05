import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Output, Input

app = dash.Dash(__name__, prevent_initial_callbacks=True, meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
])

token = "pk.eyJ1IjoiYWJkdWxoYWZlZXoxNzYiLCJhIjoiY2tpeDRpdXB2MTE5YjMwbnp3ajlpNTByeiJ9.Gl6pTfZbwRyYaliXWqZQIg"

with open('map.json') as response:
    counties = json.load(response)

cases = pd.read_csv('cases_in_regions.csv')

a = len(counties['features'])

data = []
for i in range(0, a):
    s = "N/A"
    if 'id' in counties['features'][i]['properties']:
        s = counties['features'][i]['properties']['id']
        if s in cases:
            data.append([s, cases[s].max()])

data = pd.DataFrame(data, columns=['Region', 'Cases'])

for i in range(0, a):
    if 'id' in counties['features'][i]['properties']:
        counties['features'][i]['id'] = counties['features'][i]['properties']['id']

cases['Islamabad'] = cases.iloc[:, 1:].sum(axis=1)

ages_df = pd.read_csv('ages_distribution.csv')

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=data.Region, z=data.Cases,
                                    colorscale="Viridis", zmin=0, zmax=12, marker_line_width=0, showscale=False))
fig.update_layout(mapbox_style="carto-positron", mapbox_accesstoken=token,
                  mapbox_zoom=10, mapbox_center={"lat": 33.67336763636179, "lon": 73.0081844329834})
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#20254b", paper_bgcolor="#20254b")
fig.update_layout(clickmode='event+select')

line_graph = px.line(cases, x='day', y='Islamabad')
line_graph.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#f9f9f9", paper_bgcolor="#f9f9f9",
                         xaxis_title='Day', yaxis_title='Cases per day (Islamabad)', font_color='#3a9d6e')
line_graph.update_traces(line=dict(color="#3a9d6e"))
line_graph.update_xaxes(showgrid=True, gridcolor='#d6d4d4')
line_graph.update_yaxes(showgrid=True, gridcolor='#d6d4d4')
line_graph.update_xaxes(zeroline=True, zerolinecolor='#d6d4d4')
line_graph.update_yaxes(zeroline=True, zerolinecolor='#d6d4d4')

bar_chart = px.bar(ages_df, x='range', y='Islamabad')
bar_chart.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#f9f9f9", paper_bgcolor="#f9f9f9",
                        xaxis_title='Ages', yaxis_title='Number of people (Islamabad)', font_color='#3a9d6e')
bar_chart.update_traces(marker_color='#3a9d6e')
bar_chart.update_xaxes(showgrid=True, gridcolor='#d6d4d4')
bar_chart.update_yaxes(showgrid=True, gridcolor='#d6d4d4')
bar_chart.update_xaxes(zeroline=True, zerolinecolor='#d6d4d4')
bar_chart.update_yaxes(zeroline=True, zerolinecolor='#d6d4d4')

scatter_fig = go.Figure(go.Scatter(x=ages_df['range'], y=cases['Islamabad'],
                                   mode='lines+markers', line=dict(color="#3a9d6e")))
scatter_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#f9f9f9", paper_bgcolor="#f9f9f9",
                          font_color='#3a9d6e')
scatter_fig.update_xaxes(showgrid=True, gridcolor='#d6d4d4')
scatter_fig.update_yaxes(showgrid=True, gridcolor='#d6d4d4')
scatter_fig.update_xaxes(zeroline=True, zerolinecolor='#d6d4d4')
scatter_fig.update_yaxes(zeroline=True, zerolinecolor='#d6d4d4')

current_sector = "Islamabad"
current_theme = "Light"

app.layout = html.Div(children=[
    html.Div(children=[
        html.H2(children=["ACUTE Covid Simulation Dashboard"], id='header_main_heading'),
        html.Div(children=[
            html.Img(id='header_theme_icon'),
            html.H6(children=["Dark Mode"], id='header_theme_title')
        ], id='header_theme_layout', className='header_theme_layout_class')
    ], id='header'),
    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
                id="all_cases_graph",
                figure=fig,
                responsive=True,
                style={
                    'width': '100%',
                    'height': '100%',
                }
            )
        ], className='wrapper_div_1', id='wrapper_div_1'),
        html.Div(children=[

            html.Div(children=[

                html.Div(children=[

                    html.P(children=['Active Cases'], style={
                        'font-family': 'quicksand',
                        'font-size': '20px',
                        'color': '#1e88e5',
                        'margin': '8px 0px 0px 0px',
                        'flex': '1',
                        'max-height': '28px'
                    }),
                    html.P(children=["{:,}".format(cases['Islamabad'].max() * 2)], style={
                        'font-family': 'Quicksand',
                        'font-size': '40px',
                        'color': '#1e88e5',
                        'margin': '0px 0px 0px 0px',
                        'flex': '1',
                        'max-height': '48px'
                    }, id='active_cases'),
                    html.P(children=['Recoveries'], style={
                        'font-family': 'quicksand',
                        'font-size': '20px',
                        'color': '#43a047',
                        'margin': '10px 0px 0px 0px',
                        'flex': '1',
                        'max-height': '28px'
                    }),
                    html.P(children=["{:,}".format(int(cases['Islamabad'].max() / 2))], style={
                        'font-family': 'Quicksand',
                        'font-size': '40px',
                        'color': '#43a047',
                        'margin': '0px 0px 0px 0px',
                        'flex': '1',
                        'max-height': '48px'
                    }, id='recovered_cases'),
                    html.P(children=['Deaths'], style={
                        'font-family': 'quicksand',
                        'font-size': '20px',
                        'color': '#f4511e',
                        'margin': '10px 0px 0px 0px',
                        'flex': '1',
                        'max-height': '28px'
                    }),
                    html.P(children=["{:,}".format(int(cases['Islamabad'].max() / 4))], style={
                        'font-family': 'Quicksand',
                        'font-size': '40px',
                        'color': '#f4511e',
                        'margin': '0px 0px 0px 0px',
                        'flex': '1',
                        'max-height': '48px'
                    }, id='death_cases'),

                ], className='wrapper_div_2_inner_final_inner', id='wrapper_div_2_inner_final_inner_1_1'),
                html.Div(children=[

                    dcc.Graph(
                        id="sector_line_chart",
                        figure=line_graph,
                        style={
                            'width': '100%',
                            'height': '100%',
                        },
                        responsive=True
                    )

                ], className='wrapper_div_2_inner_final_inner', id='wrapper_div_2_inner_final_inner_1_2'),

            ], style={}, className='wrapper_div_2_inner'),

            html.Div(children=[

                html.Div(children=[

                    dcc.Graph(
                        id="ages_chart",
                        figure=bar_chart,
                        style={
                            'width': '100%',
                            'height': '100%',
                        },
                        responsive=True
                    )

                ], className='wrapper_div_2_inner_final_inner', id='wrapper_div_2_inner_final_inner_2_1'),
                html.Div(children=[

                    dcc.Graph(
                        id="scatter_graph",
                        figure=scatter_fig,
                        style={
                            'width': '100%',
                            'height': '100%',
                        },
                        responsive=True
                    )

                ], className='wrapper_div_2_inner_final_inner', id='wrapper_div_2_inner_final_inner_2_2'),

            ], style={}, className='wrapper_div_2_inner')

        ], className='wrapper_div_2')
    ], className='wrapper')
], style={
}, className='container', id='main_container')


@app.callback(
    [Output('header_theme_icon', 'id'),
     Output('header_theme_title', 'id'),
     Output('header_theme_title', 'children'),
     Output('main_container', 'className'),
     Output('wrapper_div_1', 'className'),
     Output('wrapper_div_2_inner_final_inner_1_1', 'className'),
     Output('wrapper_div_2_inner_final_inner_1_2', 'className'),
     Output('wrapper_div_2_inner_final_inner_2_1', 'className'),
     Output('wrapper_div_2_inner_final_inner_2_2', 'className'),
     Output('header_main_heading', 'id'),
     Output('header_theme_layout', 'className'),
     Output('sector_line_chart', 'figure'),
     Output('ages_chart', 'figure'),
     Output('scatter_graph', 'figure'),
     Output('active_cases', 'children'),
     Output('recovered_cases', 'children'),
     Output('death_cases', 'children')
     ],
    Input('header_theme_layout', 'n_clicks'),
    Input('all_cases_graph', 'clickData')
)
def update_main_style(n_clicks, clickData):
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    global current_sector
    global current_theme
    if trigger == 'header_theme_layout':

        global line_graph
        global bar_chart
        global scatter_fig

        if n_clicks == 1 or n_clicks % 2 == 0:
            current_theme = "Dark"
            s1 = "header_theme_icon_dark"
            s2 = "header_theme_title_dark"
            s3 = "container_dark"
            s4 = "wrapper_div_1_dark"
            s5 = "wrapper_div_2_inner_final_inner_dark"
            t = "Light Mode"
            s6 = "header_main_heading_dark"
            s7 = "header_theme_layout_dark_class"

            line_graph.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#28293e",
                                     paper_bgcolor="#28293e",
                                     xaxis_title='Day', yaxis_title='Cases per day (Islamabad)', font_color='#3a9d6e')
            line_graph.update_traces(line=dict(color="#f4511e"))
            line_graph.update_xaxes(showgrid=True, gridcolor='#f9f9f9')
            line_graph.update_yaxes(showgrid=True, gridcolor='#f9f9f9')
            line_graph.update_xaxes(zeroline=True, zerolinecolor='#f9f9f9')
            line_graph.update_yaxes(zeroline=True, zerolinecolor='#f9f9f9')

            bar_chart.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#28293e",
                                    paper_bgcolor="#28293e",
                                    xaxis_title='Ages', yaxis_title='Number of people (Islamabad)',
                                    font_color='#3a9d6e')
            bar_chart.update_traces(marker_color='#f4511e')
            bar_chart.update_xaxes(showgrid=True, gridcolor='#f9f9f9')
            bar_chart.update_yaxes(showgrid=True, gridcolor='#f9f9f9')
            bar_chart.update_xaxes(zeroline=True, zerolinecolor='#f9f9f9')
            bar_chart.update_yaxes(zeroline=True, zerolinecolor='#f9f9f9')

            scatter_fig = go.Figure(go.Scatter(x=ages_df['range'], y=cases[current_sector],
                                               mode='lines+markers', line=dict(color="#f4511e")))
            scatter_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#28293e",
                                      paper_bgcolor="#28293e", font_color='#3a9d6e')
            scatter_fig.update_xaxes(showgrid=True, gridcolor='#f9f9f9')
            scatter_fig.update_yaxes(showgrid=True, gridcolor='#f9f9f9')
            scatter_fig.update_xaxes(zeroline=True, zerolinecolor='#f9f9f9')
            scatter_fig.update_yaxes(zeroline=True, zerolinecolor='#f9f9f9')
            return s1, s2, t, s3, s4, s5, s5, s5, s5, s6, s7, line_graph, bar_chart, scatter_fig, dash.no_update, dash.no_update, dash.no_update

        else:
            current_theme = "Light"
            s1 = "header_theme_icon"
            s2 = "header_theme_title"
            t = "Dark Mode"
            s3 = "container"
            s4 = "wrapper_div_1"
            s5 = "wrapper_div_2_inner_final_inner"
            s6 = "header_main_heading"
            s7 = "header_theme_layout_class"

            line_graph.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#f9f9f9",
                                     paper_bgcolor="#f9f9f9",
                                     xaxis_title='Day', yaxis_title='Cases per day (Islamabad)', font_color='#3a9d6e')
            line_graph.update_traces(line=dict(color="#3a9d6e"))
            line_graph.update_xaxes(showgrid=True, gridcolor='#d6d4d4')
            line_graph.update_yaxes(showgrid=True, gridcolor='#d6d4d4')

            bar_chart.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#f9f9f9",
                                    paper_bgcolor="#f9f9f9",
                                    xaxis_title='Ages', yaxis_title='Number of people (Islamabad)',
                                    font_color='#3a9d6e')
            bar_chart.update_traces(marker_color='#3a9d6e')
            bar_chart.update_xaxes(showgrid=True, gridcolor='#d6d4d4')
            bar_chart.update_yaxes(showgrid=True, gridcolor='#d6d4d4')
            bar_chart.update_xaxes(zeroline=True, zerolinecolor='#d6d4d4')
            bar_chart.update_yaxes(zeroline=True, zerolinecolor='#d6d4d4')

            scatter_fig = go.Figure(go.Scatter(x=ages_df['range'], y=cases[current_sector],
                                               mode='lines+markers', line=dict(color="#3a9d6e")))
            scatter_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#f9f9f9",
                                      paper_bgcolor="#f9f9f9", font_color='#3a9d6e')
            scatter_fig.update_xaxes(showgrid=True, gridcolor='#d6d4d4')
            scatter_fig.update_yaxes(showgrid=True, gridcolor='#d6d4d4')
            scatter_fig.update_xaxes(zeroline=True, zerolinecolor='#d6d4d4')
            scatter_fig.update_yaxes(zeroline=True, zerolinecolor='#d6d4d4')
            return s1, s2, t, s3, s4, s5, s5, s5, s5, s6, s7, line_graph, bar_chart, scatter_fig, dash.no_update, dash.no_update, dash.no_update

    elif trigger == 'all_cases_graph':
        current_sector = clickData['points'][0]['location']
        active, death, recovered = 0, 0, 0
        if current_sector in cases:
            active = "{:,}".format(cases[current_sector].max() * 2)
            death = "{:,}".format(int(cases[current_sector].max() / 4))
            recovered = "{:,}".format(int(cases[current_sector].max() / 2))

        line_graph = px.line(cases, x='day', y=current_sector)
        line_graph.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                 plot_bgcolor="#f9f9f9" if current_theme == "Light" else "#28293e",
                                 paper_bgcolor="#f9f9f9" if current_theme == "Light" else "#28293e",
                                 xaxis_title='Day', yaxis_title='Cases per day (Islamabad)', font_color='#3a9d6e')
        line_graph.update_traces(line=dict(color="#3a9d6e" if current_theme == "Light" else "#f4511e"))
        bar_chart.update_xaxes(showgrid=True, gridcolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")
        bar_chart.update_yaxes(showgrid=True, gridcolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")
        bar_chart.update_xaxes(zeroline=True, zerolinecolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")
        bar_chart.update_yaxes(zeroline=True, zerolinecolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")

        bar_chart = px.bar(ages_df, x='range', y=current_sector)
        bar_chart.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                plot_bgcolor="#f9f9f9" if current_theme == "Light" else "#28293e",
                                paper_bgcolor="#f9f9f9" if current_theme == "Light" else "#28293e",
                                xaxis_title='Ages', yaxis_title='Number of people (Islamabad)',
                                font_color='#3a9d6e')
        bar_chart.update_traces(marker_color="#3a9d6e" if current_theme == "Light" else "#f4511e")
        bar_chart.update_xaxes(showgrid=True, gridcolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")
        bar_chart.update_yaxes(showgrid=True, gridcolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")
        bar_chart.update_xaxes(zeroline=True, zerolinecolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")
        bar_chart.update_yaxes(zeroline=True, zerolinecolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")

        scatter_fig = go.Figure(go.Scatter(x=ages_df['range'], y=cases['Islamabad'],
                                           mode='lines+markers',
                                           line=dict(color="#3a9d6e" if current_theme == "Light" else "#f4511e")))
        scatter_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                  plot_bgcolor="#f9f9f9" if current_theme == "Light" else "#28293e",
                                  paper_bgcolor="#f9f9f9" if current_theme == "Light" else "#28293e",
                                  font_color='#3a9d6e')
        scatter_fig.update_xaxes(showgrid=True, gridcolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")
        scatter_fig.update_yaxes(showgrid=True, gridcolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")
        scatter_fig.update_xaxes(zeroline=True, zerolinecolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")
        scatter_fig.update_yaxes(zeroline=True, zerolinecolor="#d6d4d4" if current_theme == "Light" else "#f9f9f9")

        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, line_graph, bar_chart, scatter_fig, active, recovered, death

    else:
        return dash.no_update


if __name__ == '__main__':
    app.run_server(port=8070)
