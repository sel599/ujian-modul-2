import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly.graph_objects as go 
import pandas as pd 
import seaborn as sns
import dash_table 
from dash.dependencies import Input,Output, State

tsa=pd.read_csv('tsa_claims_dashboard_ujian.csv')
external_stylesheets= ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dropdown =['All',*[str(i) for i in tsa['Claim Site'].unique()]]

app = dash.Dash(__name__, external_stylesheets= external_stylesheets)
app.layout = html.Div(
    children = [

        html.H1('Ujian Modul 2 Dashboard TSA'),

        html.P('Created by: Sely'),

        dcc.Tabs(
            className = 'row', 
            value = 'tabs', 
            id = 'tabs-1', 
            children = [

                dcc.Tab(
                    label = 'Table', 
                    id = 'table', 
                    children = [

                        html.Center(html.H1('DATAFRAME TSA')),

                        html.Div(
                            className = 'col-6', 
                            children=[

                                html.P('Claim Site'),

                                dcc.Dropdown(
                                    id= 'table-dropdown', 
                                    value = 'All',
                                    options= [
                                        {'label': i, 'value': i} for i in dropdown
                                    ]
                                )
                            ]
                        ),

                        html.Div(
                            className = 'col-3', 
                            children=[

                                html.P('Max Rows:'),

                                dcc.Input(
                                    id='page-size',
                                    type='number',
                                    value=10,
                                    min=3,max=20,step=1
                                )
                            ]
                        ),

                        html.Div(
                            className = 'col-12', 
                            children = [

                                html.Button(
                                    id='Search', 
                                    n_clicks=0, 
                                    children='Search',
                                    style={
                                        'margin-top':'14px',
                                        'margin-bottom':'14px'
                                    }
                                )
                            ]
                        ),

                        html.Div(
                            id='div-table', 
                            className = 'col-12', 
                        )
                    ]
                ), 
                
                dcc.Tab(
                    label = 'Bar Chart', 
                    id = 'bar', 
                    children = [

                        html.Div(
                            className = 'col-12', 
                            children = [

                                html.Div(
                                    className = 'row', 
                                    children = [

                                        *[
                                            html.Div(
                                                className = 'col-4',
                                                children= [

                                                    html.P(f'Y{idx+1}'),

                                                    dcc.Dropdown(
                                                        id= f'axis-{idx}', 
                                                        value = col,
                                                        options= [
                                                            {'label': i, 'value': i} for i in tsa.select_dtypes('number').columns
                                                        ]
                                                    )
                                                ]
                                            ) for idx, col in enumerate(['Claim Amount', 'Close Amount'])
                                        ],

                                        html.Div(
                                            className = 'col-4',
                                            children= [

                                                html.P(f'X'),

                                                dcc.Dropdown(
                                                    id= f'axis-2', 
                                                    # input callback id, property = value
                                                    value = f'Claim Type',
                                                    options= [
                                                        {'label': i, 'value': i} for i in ['Claim Type', 'Claim Site', 'Disposition']
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),

                                html.Div(
                                    children= [
                                        dcc.Graph(
                                            id = 'contoh-graph-bar',
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
            
                dcc.Tab(
                    label = 'Scatter Chart', 
                    id = 'scatter', 
                    children = [

                        html.Div(
                            className = 'col-12', 
                            children = dcc.Graph(

                                id = 'graph-scatter',
                                figure = {
                                    'data':[go.Scatter(
                                        x= tsa[tsa['Claim Type']==i]['Claim Amount'],
                                        y= tsa[tsa['Claim Type']==i]['Close Amount'],
                                        text= tsa[tsa['Claim Type']==i]['Status'],
                                        mode='markers',
                                        name= f'{i}'    
                                    ) for i in tsa['Claim Type'].unique()],
                                    'layout':go.Layout(
                                        xaxis= {'title':'Claim Amount'},
                                        yaxis = {'title' : 'Close Amount'},
                                        hovermode = 'closest'
                                    )
                                }
                            )
                        )
                    ]
                ),

                dcc.Tab(
                    label = 'Pie Chart', 
                    id = 'tab-dua', 
                    children = [

                        html.Div(
                            className = 'col-4',
                            children= [

                                html.P('Select value'),

                                dcc.Dropdown(
                                    id= f'pie-dropdown', 
                                    value = 'Claim Amount',
                                    options= [
                                        {'label': i, 'value': i} for i in tsa.select_dtypes('number').columns
                                    ]
                                )
                            ]
                        ),

                        html.Div(
                            className = 'col-12', 
                            children = dcc.Graph(
                                id = 'pie-chart'
                            )
                        )
                    ]
                )
            ],
            content_style = {
                'fontFamily': 'Arial',
                'borderBottom': '1px solid #d6d6d6',
                'borderRight': '1px solid #d6d6d6',
                'borderLeft': '1px solid #d6d6d6',
                'padding': '44px'
            }   
        )
    ], 
    style={
        'maxwidth': '1200px', 'margin': '0 auto'
    }
)

@app.callback(
    Output(component_id= 'div-table', component_property= 'children'),
    [Input(component_id='Search', component_property='n_clicks')],
    [State(component_id=i,component_property='value') for i in ['table-dropdown','page-size']]
)

def update_tabl(n_clicks, site, size):
    if site.lower() == 'all':
        df = tsa.to_dict('records')
    else:
        df = tsa[tsa['Claim Site']==site].to_dict('records')
    return dash_table.DataTable(
                    id= 'dataTable',
                    data= df,
                    columns= [{'id': i, 'name': i} for i in tsa.columns],
                    page_action= 'native',
                    page_current= 0,
                    page_size = 10,
                    style_table={'overflowX': 'scroll'})

@app.callback(
    Output(component_id= 'contoh-graph-bar', component_property= 'figure'),
    [Input(component_id=f'axis-{i}', component_property='value') for i in range(3)]
)
def create_graph_bar(y1,y2,x):
    return {'data' : [{
        'x': tsa[x],
        'y': tsa[i],
        'type': 'bar',
        'name': i
    } for i in [y1,y2]
    ],
        'layout': {'title': 'Bar Chart'}
    }

@app.callback(
    Output(component_id= 'pie-chart', component_property= 'figure'),
    [Input(component_id=f'pie-dropdown', component_property='value')]
)
def create_pie_chart(pie):
    gb = tsa.groupby('Claim Type').mean()
    return {'data' : [go.Pie(
                labels=gb.index,
                values=list(gb[pie])
            )
            ], 'layout': {'title': 'Mean Pie Chart'}
        }

if __name__ == '__main__':
    app.run_server(debug=True)