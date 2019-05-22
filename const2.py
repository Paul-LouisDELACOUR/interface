import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import numpy as np
#import pymysql as _mysql
#import _mysql
import cx_Oracle

from dash.dependencies import Input, Output, State       
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
markdown_text = '''
\n
This is an interface for queries in the database from the 
website Airbnb 
	\n In SEARCH you will be able to search a name, a date, 
a country, a city ... and get all the related information 
	\n In PREDEFINIED QUERIES you will get the result of 
predefinied queries we made
	\n In INSERT/DELETE you will be able to insert a listing, 
a review, ...
'''




#####Connecting to the database

#db=_mysql.connect(host="cs322-db.epfl.ch",user="C##DB2019_G04",
#                 passwd="DB2019_G04",db="Airbnb");
#db.query("""SELECT * FROM BED_TYPE """)
#r=db.store_result()
#r.fetch_row()

################ End of connecting to the database

######## Layout for the tabs
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='HOME', value='home'),
        dcc.Tab(label='SEARCH', value='search'),
        dcc.Tab(label='PREDEFINED QUERIES', value='predefined_queries'),
        dcc.Tab(label='INSERT', value='insert'),
        dcc.Tab(label='DELETE', value='delete'),
    ]),
    html.Div(id='tabs-content')
])

#####Here are the different layouts for the different modes

##Search
layout_search = html.Div([
    html.Div([
        html.Label('Location'),
        dcc.Input(id='loc_id', value='Location', type='text')],
        style={'marginLeft': 10, 'marginTop': 10, 'width': '49%', 'display': 'inline-block'}
    ),

    
    html.Div([
        html.Div([
            html.Label('Start date - end date')
            ]),
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=dt(2019, 8, 5),
            max_date_allowed=dt(2019, 9, 19),
            initial_visible_month=dt(2019, 8, 5),
            
            #end_date=dt(2019, 8, 25)
        )],
        style ={'marginLeft': 10, 'marginTop': 10, 'width': '100%'}
    ),
    
    html.Div([
        html.Label('Number of beds'),
        dcc.Dropdown(
            options=[
                {'label': '1 Bed', 'value': '1'},
                {'label': '2 Beds', 'value': '2'},
                {'label': '3 Beds', 'value': '3'},
                {'label': '4 Beds', 'value': '4'},
                {'label': '5 Beds', 'value': '5'},
                {'label': '6 Beds', 'value': '6'},
                {'label': '7 Beds', 'value': '7'},
                {'label': '8 Beds', 'value': '8'},
                {'label': '9 Beds', 'value': '9'},
                {'label': '10 Beds', 'value': '10'}
                ],
            value='1'
            )] , 
         style={'marginLeft': 10, 'marginTop': 10, 'width': '49%', 'display': 'inline-block'}
        ),
    
    html.Div([
        html.Label('Daily price range'),
        dcc.RangeSlider(
            id='non-linear-range-slider',
            marks={i: '{} '.format(i) for i in range(0,5001,1000)},
            min=0,
            max=5000,
            value=[50, 200]
        ) 
        ],
        style={'marginLeft': 10, 'marginTop': 10, 'width': '95%'}
    ),

    html.Div([
        html.Button('SEARCH FOR YOUR RESERVATION', id='button_reservation')
        ],
        style={'marginLeft': 400, 'marginTop': 40, 'width': '100%'}
    ),
    

    html.Div(id='output_container_search',
        style={'marginLeft': 10, 'marginTop': 50, 'width': '80%', 'display': 'inline-block'}
    )
])

app.config['suppress_callback_exceptions']=True
@app.callback(
    Output(component_id='output_container_search', component_property='children'),
    [
    Input(component_id='loc_id', component_property='value'),
    Input(component_id = 'my-date-picker-range', component_property ='start_date'),
    Input(component_id = 'my-date-picker-range', component_property = 'end_date'),
    Input(component_id = 'non-linear-range-slider', component_property = 'value')
    ]
)

def update_output(loc_id_name, start_date, end_date, price):
    string_prefix = 'The location is "{}"'.format(loc_id_name)
    
    #return string_prefix
    if start_date is not None:
        string_prefix += ' and you have selected   start : '
        string_prefix += date_to_string(start_date)
    if end_date is not None :
        string_prefix += ' and ends : '
        string_prefix += date_to_string(end_date)
    if price is not None : 
        transformed_value = [transform_value(v) for v in price]
        price_string = ' and price range is [{:0.2f}, {:0.2f}]'.format(
                transformed_value[0], 
                transformed_value[1])
        string_prefix += price_string

    return html.Div([string_prefix])
    
def transform_value(value):
    return value

def date_to_string(date):
    date = date.split(' ')[0] 
    date = dt.strptime(date, '%Y-%m-%d')
    date_string = date.strftime('%B %d, %Y')
    return date_string


'''
def update_output(loc_id_name):
    string_prefix = 'The location is "{}"'.format(loc_id_name)
    
    #return string_prefix
    
    dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
    conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
    c = conn.cursor()
    c.execute('select * from BED_TYPE')
        
    #return html.Div([string_prefix + date_string])
    return html.Div([c[0]])
'''




################################### SEARCH END

##predefinied queries

def which_table(value):
    if(value == 1 ) : 
        return dash_table.DataTable(
            id = 'table-queries',
            columns = [
                {"Number of values" : 1, "id":1},
                {"age":2 , "id" :2 }
            ],
            pagination_settings={
                'current_page': 0,
                'page_size': PAGE_SIZE
            },
            pagination_mode='be',

            filtering='be',
            filtering_settings=''
        )

######################    Predefinied queries
layout_predefinied = html.Div([
	html.Div( [
        dcc.Dropdown(
            id = 'question-dropdown',
            options=[
                {'label': 'Q1', 'value': '1'},
                {'label': 'Q2', 'value': '2'},
                {'label': 'Q3', 'value': '3'},
                {'label': 'Q4', 'value': '4'},
                {'label': 'Q5', 'value': '5'},
                {'label': 'Q6', 'value': '6'},  
                {'label': 'Q7', 'value': '7'},
                {'label': 'Q8', 'value': '8'},
                {'label': 'Q9', 'value': '9'},
                {'label': 'Q10', 'value': '10'},
                {'label': 'Q11', 'value': '11'},
                {'label': 'Q12', 'value': '12'}
            ],
            value='1'
        )
        ] ,
        style={'marginLeft': 10, 'marginTop': 10, 'width': '30%', 'display': 'inline-block'}
    ), 
    html.Div(id = 'output-container' ,
        style={'marginLeft': 10, 'marginTop': 50, 'width': '80%'}
        )
])

app.config['suppress_callback_exceptions']=True
@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('question-dropdown', 'value')])

def update_output(value):
    if value == '1'  :
        return html.Div([
                html.Div(id='output_container_query_1',
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),
                html.Div( [
                    html.Label('Order'),
                    dcc.Dropdown(
                        id = 'q1p1',
                        options=[
                            {'label': 'Ascending', 'value': '1'},
                            {'label': 'Descending', 'value': '2'}
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 60, 'width': '100%', 'display': 'inline-block'}
                ) ,
                html.Div([
                    html.Button('SEARCH', id='search_1')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),
                html.Div([
                    dash_table.DataTable(
                    id='datatable-q1',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                ),
                
            ])
    elif value == '2' : 
            return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_2')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div( [
                    html.Label('City'),
                    dcc.Dropdown(
                        id = 'q2p1',
                        options=[
                            {'label': 'Madrid', 'value': '1'},
                            {'label': 'Barcelona', 'value': '2'},
                            {'label': 'Berlin', 'value': '3'},
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),
                html.Div( [
                    html.Label("Type of review_score"),
                    dcc.Dropdown(
                        id = 'q2p2',
                        options=[
                            {'label': 'Rating of the listing', 'value': '1'},
                            {'label': 'Communication with the host', 'value': '2'},
                            {'label': 'Value of the material', 'value': '3'},
                            {'label': 'Checkin', 'value': '4'},
                            {'label': 'Cleanliness of the listing', 'value': '5'},
                            {'label': 'Accuracy of the description', 'value': '6'},
                            {'label': 'Location', 'value': '7'}
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Button('SEARCH', id='search_2')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q2',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                ),

            ])
    elif value == '3' :
            return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_3')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),
                html.Div( [
                    html.Label('Extremum'),
                    dcc.Dropdown(
                        id = 'q3p1',
                        options=[
                            {'label': 'Highest', 'value': '1'},
                            {'label': 'Lowest', 'value': '2'}
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Button('SEARCH', id='search_3')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q3',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                ),

            ])
    elif value == '4' :
        #### 3 param 
            return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_4')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div( [
                    html.Label('Extremum'),
                    dcc.Dropdown(
                        id = 'q4p1',
                        options=[
                            {'label': 'Cheapest', 'value': '1'},
                            {'label': 'Highest', 'value': '2'}
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div( [
                    html.Label('Type of cancellation'),
                    dcc.Dropdown(
                        id = 'q4p2',
                        options=[
                            {'label': 'Flexible', 'value': '1'},
                            {'label': 'Moderate', 'value': '2'},
                            {'label': 'Strict -', 'value': '3'},
                            {'label': 'Strict', 'value': '4'},
                            {'label': 'Strict +', 'value': '5'},
                            {'label': 'Super strict', 'value': '6'}
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div( [
                    html.Label('Min number of beds'),
                    dcc.Dropdown(
                        id = 'q4p3',
                        options=[
                            {'label': '2', 'value': '2'},
                            {'label': '3', 'value': '3'},
                            {'label': '4', 'value': '4'},
                            {'label': '5', 'value': '5'}
                            ],
                        value='2'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Button('SEARCH', id='search_4')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q4',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                )

            ])
    elif value == '5' :
            #### 1 param
            return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_5')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div( [
                    html.Label('Order'),
                    dcc.Dropdown(
                        id = 'q5p1',
                        options=[
                            {'label': 'Ascending', 'value': '1'},
                            {'label': 'Descending', 'value': '2'}
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ) ,

                html.Div([
                    html.Button('SEARCH', id='search_5')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q5',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                )

            ])
    elif value == '6' :
            ## 0 param
            return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_6')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Button('SEARCH', id='search_6')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q6',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                )

            ])
    elif value == '7' :
            ## 2 param
            return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_7')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div( [
                    html.Label('City'),
                    dcc.Dropdown(
                        id = 'q7p1',
                        options=[
                            {'label': 'Madrid', 'value': '1'},
                            {'label': 'Barcelona', 'value': '2'},
                            {'label': 'Berlin', 'value': '3'}
                            ],
                        value='3'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),
                html.Div( [
                    html.Label('Room type'),
                    dcc.Dropdown(
                        id = 'q7p2',
                        options=[
                            {'label': 'Private room', 'value': '1'},
                            {'label': 'Entire room', 'value': '2'},
                            {'label': 'Shared room', 'value': '3'}
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Button('SEARCH', id='search_7')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q7',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                )

            ])
    elif value == '8' :
            ## 1 param
            return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_8')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div( [
                    html.Label("Type of review_score"),
                    dcc.Dropdown(
                        id = 'q8p1',
                        options=[
                            {'label': 'Rating of the listing', 'value': '1'},
                            {'label': 'Communication with the host', 'value': '2'},
                            {'label': 'Value of the material', 'value': '3'},
                            {'label': 'Checkin', 'value': '4'},
                            {'label': 'Cleanliness of the listing', 'value': '5'},
                            {'label': 'Accuracy of the description', 'value': '6'},
                            {'label': 'Location', 'value': '7'}
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Button('SEARCH', id='search_8')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q8',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                )

            ])
    elif value == '9' :
            ### 0 param
            return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_9')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Button('SEARCH', id='search_9')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q9',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                )

            ])
    elif value == '10' :
            ## 1 param
            return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_10')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div( [
                    html.Label('City'),
                    dcc.Dropdown(
                        id = 'q10p1',
                        options=[
                            {'label': 'Madrid', 'value': '1'},
                            {'label': 'Barcelona', 'value': '2'},
                            {'label': 'Berlin', 'value': '3'}
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Button('SEARCH', id='search_10')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q10',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                )

            ])
    elif value == '11' :
        return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_11')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),


                html.Div([
                    html.Button('SEARCH', id='search_11')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q11',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                )

            ])
    elif value == '12' :
        return html.Div([
                html.Div([
                    dcc.Markdown(id = 'output_container_query_12')],
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),
                html.Div( [
                    html.Label('City'),
                    dcc.Dropdown(
                        id = 'q12p1',
                        options=[
                            {'label': 'Madrid', 'value': '1'},
                            {'label': 'Barcelona', 'value': '2'},
                            {'label': 'Berlin', 'value': '3'}
                            ],
                        value='1'
                    )] ,
                    style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Button('SEARCH', id='search_12')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                ),

                html.Div([
                    dash_table.DataTable(
                    id='datatable-q12',
                    data = [],
                    columns = []
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                )

            ])


############## Q1
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_1', component_property = 'children'),
    [Input('search_1', 'n_clicks')],
    [State('q1p1', 'value')]
    )
def update_output(search ,q1p1):
    order = 'ascending'
    if(q1p1 == '1') :
        order = 'ascending'
    elif(q1p1 == '2') :
        order = 'descending'
    string_prefix = ''' 
        \n Print how many hosts in each city have declared the area of their property in square meters. Sort the
        \n output based on the city name in "{}" order
        '''.format(order)

    return html.Div([string_prefix])

app.config['suppress_callback_exceptions']=True
@app.callback(
    [Output('datatable-q1', component_property = 'data'), Output('datatable-q1', component_property = 'columns')],
    [Input('search_1', 'n_clicks')],
    [State('q1p1', 'value')]
    )
def update_output(search ,q1p1):
    order = 'ASC'
    if(q1p1 == '2') :
        order = 'DESC'

    dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
    conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
    

    string_prefix = ''' 
            SELECT CI.city_name, COUNT(*)
            FROM LISTING LI, NEIGHBORHOOD NE, CITY CI
            WHERE NOT LI.square_feet IS NULL 
            AND LI.square_feet > 0
            AND LI.neighborhood_id = NE.neighborhood_id
            AND NE.city_id = CI.city_id
            GROUP BY CI.city_name
            ORDER BY CI.city_name {}
        '''.format(order)
    
    #return string_prefix
    c = conn.cursor()
    c.execute(string_prefix)

    df = pd.DataFrame.from_records(list(c))
    columns = [
            {"id": 0, "name": "City_name"},
            {"id": 1, "name": "Count"},
            ]

        
    #return html.Div([string_prefix + date_string])
    return df.to_dict('records'), columns


#############

############## Q2
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_2', component_property ='children'),
    [Input('search_2', 'n_clicks')],
    [State('q2p1', 'value'),
    State('q2p2' , 'value')]
)
def uptdapte_output(search,q2p1,q2p2) :
    city = 'madrid'
    if(q2p1 == '1'):
        city = 'Madrid'
    elif(q2p1 == '2'):    
        city = 'Barcelona'
    elif(q2p1 == '3') :
        city ='Berlin'

    review_scores = 'review_scores_rating'
    if(q2p2 == '1') : review_scores = 'review_scores_rating'
    elif(q2p2 == '2') : review_scores = 'review_scores_communication'
    elif(q2p2 == '3') : review_scores = 'review_scores_value'
    elif(q2p2 == '4') : review_scores = 'review_scores_checkin'
    elif(q2p2 == '5') : review_scores = 'review_scores_cleanliness'
    elif(q2p2 == '6') : review_scores = 'review_scores_accuracy'
    elif(q2p2 == '7') : review_scores = 'review_scores_location'

    string_prefix_2 = '''
    \n The quality of a neighborhood is defined based on the number of listings and the review score of these
    \n listings, one way for computing that is using the median of the review scores, as medians are more
    \n robust to outliers. Find the top-5 neighborhoods using median review scores ("{}") of
    \n listings in "{}". 
    '''.format(review_scores, city)
    return string_prefix_2

app.config['suppress_callback_exceptions']=True
@app.callback(
    [Output('datatable-q2', component_property = 'data'), Output('datatable-q2', component_property = 'columns')],
    [Input('search_2', 'n_clicks')],
    [State('q2p1', 'value'), State('q2p2', 'value')]
    )
def update_output(search ,q2p1, q2p2):
    city = 'madrid'
    if(q2p1 == '1'):
        city = 'madrid'
    elif(q2p1 == '2'):    
        city = 'barcelona'
    elif(q2p1 == '3') :
        city ='berlin'

    dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
    conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)

    review_scores = 'review_scores_rating'
    if(q2p2 == '1') : review_scores = 'review_scores_rating'
    elif(q2p2 == '2') : review_scores = 'review_scores_communication'
    elif(q2p2 == '3') : review_scores = 'review_scores_value'
    elif(q2p2 == '4') : review_scores = 'review_scores_checkin'
    elif(q2p2 == '5') : review_scores = 'review_scores_cleanliness'
    elif(q2p2 == '6') : review_scores = 'review_scores_accuracy'
    elif(q2p2 == '7') : review_scores = 'review_scores_location'
    
    string_prefix = ''' 
            SELECT NC.neighborhood_id, NC.neighborhood_name, LI.{0}
            FROM (SELECT NE.neighborhood_id, NE.neighborhood_name, COUNT(*) as CO
            FROM LISTING LI, NEIGHBORHOOD NE, CITY CI
            WHERE LI.neighborhood_id = NE.neighborhood_id 
            AND NE.city_id = CI.city_id
            AND CI.city_name = \'{1}\'
            AND NOT LI.{0} IS NULL
            GROUP BY NE.neighborhood_id, NE.neighborhood_name) NC, LISTING LI
            WHERE (LI.neighborhood_id = NC.neighborhood_id AND 
            LI.listing_id = (SELECT listing_id
            FROM (SELECT LI.listing_id, row_number() over(order by li.{0}) AS row_number, LI.review_scores_rating
            FROM LISTING LI
            WHERE LI.neighborhood_id = NC.neighborhood_id AND NOT LI.{0} IS NULL
            ORDER BY LI.{0}
            FETCH FIRST NC.CO/2 ROWS ONLY)
            ORDER BY REVIEW_SCORES_RATING DESC
            FETCH FIRST 1 ROW ONLY))
            ORDER BY LI.{0} DESC
            FETCH FIRST 5 ROWS ONLY
        '''.format(review_scores, city)
    
    #return string_prefix
    c = conn.cursor()
    c.execute(string_prefix)

    df = pd.DataFrame.from_records(list(c))
    columns = [
            {"id": 0, "name": "neighborhood_id"},
            {"id": 1, "name": "neighborhood_name"},
            {"id": 2, "name": "{}".format(review_scores)}
            ]

        
    #return html.Div([string_prefix + date_string])
    return df.to_dict('records'), columns

############## Q3
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_3', component_property = 'children'),
    [Input('search_3', 'n_clicks')],
    [State('q3p1', 'value')]
    )
def update_output(search_3 ,q3p1):
    order = 'highest'
    if(q3p1 == '1') :
        order = 'highest'
    elif(q3p1 == '2') :
        order = 'lowest'
    string_prefix_3 = ''' 
        \n Find all the hosts (host_ids, host_names) with the "{}" number of listings.
        '''.format(order)

    return string_prefix_3

app.config['suppress_callback_exceptions']=True
@app.callback(
    [Output('datatable-q3', component_property = 'data'), Output('datatable-q3', component_property = 'columns')],
    [Input('search_3', 'n_clicks')],
    [State('q3p1', 'value')]
    )
def update_output(search, q3p1):

    order = 'DESC'
    if(q3p1 == '1'):
        order = 'DESC'
    elif(q3p1 == '2'):    
        order = 'ASC'

    dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
    conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
    
    string_prefix = ''' 
            SELECT host_id, host_name, count_each as count
            FROM (SELECT HO.host_id, HO.host_name, COUNT(*) as count_each, count_max
            FROM (SELECT COUNT(*) as count_max
            FROM LISTING LI
            GROUP BY LI.host_id 
            ORDER BY COUNT(*) {0} FETCH FIRST 1 ROWS ONLY), LISTING LI, HOST HO
            WHERE HO.host_id = LI.host_id
            GROUP BY HO.host_id, HO.host_name, count_max) WHERE count_each = count_max
        '''.format(order)
    
    #return string_prefix
    c = conn.cursor()
    c.execute(string_prefix)

    df = pd.DataFrame.from_records(list(c))
    columns = [
            {"id": 0, "name": "host_id"},
            {"id": 1, "name": "host_name"}
            ]

    return df.to_dict('records'), columns

############## Q4
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_4', component_property = 'children'),
    [Input('search_4', 'n_clicks')],
    [State('q4p1', 'value'),
    State('q4p2', 'value'),
    State('q4p3', 'value')]
    )
def update_output(search_4,q4p1,q4p2,q4p3):
    extremum = 'cheapest'
    if(q4p1 == '1') :
        extremum = 'cheapest'
    elif(q4p1 == '2' ) :
        extremum = 'highest'
    
    cancellation = 'flexible'
    if(q4p2 =='1') :
        cancelation = 'flexible'
    elif(q4p2 == '2') :
        cancellation = 'moderate'
    elif(q4p2 == '3') :   
        cancellation = 'strict'
    elif(q4p2 == '4') :   
        cancellation = 'strict_14_with_grace_period'
    elif(q4p2 == '5') :   
        cancellation = 'super_strict_30'
    elif(q4p2 == '6') : cancellation = 'super_strict_60'
    
    beds = '2'
    if(q4p3 == '2') :
        beds = '2'
    elif(q4p3 == '3') :
        beds = '3'
    elif(q4p3 == '4') :
        beds = '4'
    if(q4p3 == '5') :
        beds = '5'

    string_prefix_4 = '''
    \n Find the 5 most "{}" Apartments (based on average price within the available dates) in Berlin
    \n available for at least one day between 01-03-2019 and 30-04-2019 having at least "{}" beds, a location
    \n review score of at least 8, "{}" cancellation, and listed by a host with a verifiable government id.
    '''.format(extremum, beds,cancellation )

    return string_prefix_4

app.config['suppress_callback_exceptions']=True
@app.callback(
    [Output('datatable-q4', component_property = 'data'), Output('datatable-q4', component_property = 'columns')],
    [Input('search_4', 'n_clicks')],
    [State('q4p1', 'value'),
    State('q4p2', 'value'),
    State('q4p3', 'value')]
    )
def update_output(search, q4p1, q4p2, q4p3):

    extremum = 'ASC'
    if(q4p1 == '1') :
        extremum = 'ASC'
    elif(q4p1 == '2' ) :
        extremum = 'DESC'
    
    cancellation = 'flexible'
    if(q4p2 =='1') :
        cancelation = 'flexible'
    elif(q4p2 == '2') :
        cancellation = 'moderate'
    elif(q4p2 == '3') :   
        cancellation = 'strict'
    elif(q4p2 == '4') :   
        cancellation = 'strict_14_with_grace_period'
    elif(q4p2 == '5') :   
        cancellation = 'super_strict_30'
    elif(q4p2 == '6') : cancellation = 'super_strict_60'
    
    beds = '2'
    if(q4p3 == '2') :
        beds = '2'
    elif(q4p3 == '3') :
        beds = '3'
    elif(q4p3 == '4') :
        beds = '4'
    if(q4p3 == '5') :
        beds = '5'

    dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
    conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
    
    ''''To do : change this method'''
    string_prefix = ''' 
    SELECT DISTINCT LI.listing_id, LI.listing_name
    FROM (SELECT LI.*
    FROM LISTING LI, CALENDAR CA, RESERVED_ON RE
    WHERE LI.listing_id = RE.listing_id
    AND CA.calendar_id = RE.calendar_id
    AND RE.available = 't'
    AND CA.calendar_date >= date '2019-03-01' 
    AND CA.calendar_date <= date '2019-04-30') LI, CALENDAR CA, RESERVED_ON RE, CANCELLATION_POLICY CP, HOST HO, HOST_VERIFICATIONS HV, VERIFIES VE, CITY CI, NEIGHBORHOOD NE
    WHERE LI.cancellation_policy_id = CP.cancellation_policy_id 
    AND CP.cancellation_policy_name = \'{1}\'
    AND LI.neighborhood_id = NE.neighborhood_id
    AND NE.city_id = CI.city_id
    AND CI.city_name = 'berlin'
    AND LI.review_scores_value >= 8
    AND LI.beds >= {2}
    AND LI.host_id = HO.host_id
    AND VE.host_id = HO.host_id
    AND HV.host_verifications_id = VE.host_verifications_id
    AND HV.host_verifications = 'government_id'
    AND RE.listing_id = LI.listing_id
    AND CA.calendar_id = RE.calendar_id
    GROUP BY LI.listing_id, LI.listing_name
    ORDER BY AVG(RE.price) {0}
    FETCH FIRST 5 ROWS ONLY
        '''.format(extremum, cancellation, beds)
    
    #return string_prefix
    c = conn.cursor()
    c.execute(string_prefix)

    df = pd.DataFrame.from_records(list(c))
    columns = [
            {"id": 0, "name": "listing_id"},
            {"id": 1, "name": "listing_name"}
            ]

    return df.to_dict('records'), columns


############## Q5
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_5', component_property = 'children'),
    [Input('search_5', 'n_clicks')],
    [State('q5p1', 'value')]
    )
def update_output(search, q5p1):
    order = 'ascending'
    if(q5p1 == '1'):
        order = 'ascending'
    elif(q5p1 == '2') :
        order = 'descending'
    string_prefix_5 = ''' 
        \n Print how many hosts in each city have declared the area of their property in square meters. Sort the
        \n output based on the city name in "{}" order
        '''.format(order)

    return string_prefix_5

############## Q6
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_6', component_property = 'children'),
    [Input('search_6', 'n_clicks')]
    )
def update_output(search):
    string_prefix_6 = '''
    \nWhat are top three busiest listings per host? The more reviews a listing has, the busier the listing is.
    '''
    return string_prefix_6


############## Q7
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_7', component_property = 'children'),
    [Input('search_7', 'n_clicks')],
    [State('q7p1', 'value'),
    State('q7p2','value')]
    )
def update_output(search, q7p1, q7p2):
    city = 'Madrid'
    if(q7p1 == '1'):
        city = 'Madrid'
    elif(q7p1 == '2') :
        city = 'Barcelona'
    elif(q7p1 == '3') :
        city = 'Berlin'

    room_type = 'private room'
    if(q7p2 == '1'):
        room_type = 'private room'
    elif(q7p2 == '2') :
        room_type = 'entire room'
    elif(q7p2 == '3') :
        room_type = 'shared room'
    string_prefix_7 = '''
    \nWhat are the three most frequently used amenities at each neighborhood in "{}" for the listings with
    \n“{}” room type?
    '''.format(city, room_type)

    return string_prefix_7

############## Q8
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_8', component_property = 'children'),
    [Input('search_8', 'n_clicks')],
    [State('q8p1', 'value')]
    )
def update_output(search, q8p1):
    rating = 'rating of the listing'
    if(q8p1 == '1'):
        rating = 'rating of the listing'
    elif(q8p1 == '2') :
        rating = 'Communication with the host score'
    elif(q8p1 == '3') :
        rating = 'Value of the material score'
    elif(q8p1 == '4') :
        rating = 'Checkin score'
    elif(q8p1 == '5') :
        rating = 'Cleanliness of the listing'
    elif(q8p1 == '6') :
        rating = 'Accuracy of the description'
    elif(q8p1 == '7') :
        rating = 'Location score'
            
    string_prefix_8 = '''
    \n What is the difference in the average "{}" of the host who has the most
    \n diverse way of verifications and of the host who has the least diverse way of verifications. In case of a
    \n multiple number of the most or the least diverse verifying hosts, pick a host one from the most and
    \n one from the least verifying hosts.
    '''.format(rating)
    return string_prefix_8

############## Q9
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_9', component_property = 'children'),
    [Input('search_9', 'n_clicks')]
    )
def update_output(search):
    string_prefix_9 = '''
    \n What is the city who has the highest number of reviews for the room types whose average number of
    \n accommodates are greater than 3.
    '''
    return string_prefix_9

############## Q10
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_10', component_property = 'children'),
    [Input('search_10', 'n_clicks')],
    [State('q10p1', 'value' )]
    )
def update_output(search, q10p1):
    city = 'Madrid'
    if(q10p1 == '1'):
        city = 'Madrid'
    elif(q10p1 == '2'):
        city = 'Barcelona'
    elif(q10p1 == '2'):
        city = 'Berlin'
    string_prefix_10  = '''
    \n Print all the neighborhoods in {} which have at least 50 percent of their listings occupied in year
    \n 2019 and their host has joined airbnb before 01.06.2017
    '''.format(city)

    return string_prefix_10

############### Q11
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_11', component_property = 'children'),
    [Input('search_11', 'n_clicks')]
    )
def update_output(search):
    string_prefix_11  = '''
    \n Print all the countries that in 2018 had at least 20"%"" of their listings available.
    '''
    return string_prefix_11

app.config['suppress_callback_exceptions']=True
@app.callback(
    [Output('datatable-q11', component_property = 'data'), Output('datatable-q11', component_property = 'columns')],
    [Input('search_11', 'n_clicks')]
    )
def update_output(search):

    dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
    conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
    

    string_prefix = ''' 
        SELECT GOOD.country, GOOD.count1 / TOTAL.count2 as RATIO
        FROM (SELECT CO.country_code, CO.country, COUNT(DISTINCT LI.listing_id) as count1
        FROM LISTING LI, RESERVED_ON RE, NEIGHBORHOOD NE, CITY CI, COUNTRY CO, CALENDAR CA
        WHERE LI.listing_id = RE.listing_id 
        AND LI.neighborhood_id = NE.neighborhood_id
        AND NE.city_id = CI.city_id
        AND CO.country_code = CI.country_code 
        AND RE.available = 't' 
        AND CA.calendar_id = RE.calendar_id 
        AND CA.CALENDAR_DATE >= date '2018-01-01' 
        AND CA.CALENDAR_DATE <= date '2018-12-31'
        GROUP BY CO.COUNTRY_CODE, CO.COUNTRY) GOOD, 
        (SELECT CO.country_code, CO.country, COUNT(DISTINCT LI.listing_id) as count2
        FROM LISTING LI, RESERVED_ON RE, NEIGHBORHOOD NE, CITY CI, COUNTRY CO, CALENDAR CA
        WHERE LI.listing_id = RE.listing_id 
        AND LI.neighborhood_id = NE.neighborhood_id
        AND NE.city_id = CI.city_id
        AND CO.country_code = CI.country_code 
        AND CA.calendar_id = RE.calendar_id 
        AND CA.CALENDAR_DATE >= date '2018-01-01' 
        AND CA.CALENDAR_DATE <= date '2018-12-31'
        GROUP BY CO.country_code, CO.COUNTRY) TOTAL
        WHERE GOOD.country_code = TOTAL.country_code AND count1 > 0.2*count1
        '''
    
    #return string_prefix
    c = conn.cursor()
    c.execute(string_prefix)

    df = pd.DataFrame.from_records(list(c))
    columns = [
            {"id": 0, "name": "country"},
            {"id": 1, "name": "ratio"},
            ]
        
    #return html.Div([string_prefix + date_string])
    return df.to_dict('records'), columns

############### Q12
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_12', component_property = 'children'),
    [Input('search_12', 'n_clicks')],
    [State('q12p1', 'value')]
    )
def update_output(search, q12p1):
    city = 'madrid'
    if(q12p1 == '1'):
        city = 'Madrid'
    elif(q12p1 == '2'):
        city = 'Barcelona'
    elif(q12p1 == '3'):
        city = 'Berlin'
    string_prefix_12  = '''
    \n Print all the neighborhoods in "{}" where more than 5 percent of their accommodation’s
    \n cancelation policy is strict with grace period.
    '''.format(city)

    return string_prefix_12

app.config['suppress_callback_exceptions']=True
@app.callback(
    [Output('datatable-q12', component_property = 'data'), Output('datatable-q12', component_property = 'columns')],
    [Input('search_12', 'n_clicks')],
    [State('q12p1', 'value')]
    )
def update_output(search ,q12p1):
    city = 'madrid'
    if(q12p1 == '1') :
        city = 'madrid'
    elif(q12p1 == '2') :
        city = 'barcelona'
    elif(q12p1 == '3') :
        city = 'berlin'

    dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
    conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
    

    string_prefix = ''' 
        SELECT up.neighborhood_name, up.neighborhood_id, up.count1 / down.count1 as ratio
FROM (SELECT NE.neighborhood_name, NE.neighborhood_id, COUNT(DISTINCT LI.listing_id) as count1
FROM CANCELLATION_POLICY CA, LISTING LI, NEIGHBORHOOD NE, CITY CI
WHERE LI.cancellation_policy_id = CA.cancellation_policy_id AND LI.neighborhood_id = NE.neighborhood_id AND NE.city_id = CI.city_id AND CA.cancellation_policy_name = 'strict_14_with_grace_period' AND CI.city_name = \'{0}\'
GROUP BY NE.neighborhood_name, NE.neighborhood_id) up,
(SELECT NE.neighborhood_name, NE.neighborhood_id, COUNT(DISTINCT LI.listing_id) as count1
FROM LISTING LI, NEIGHBORHOOD NE, CITY CI
WHERE LI.neighborhood_id = NE.neighborhood_id AND CI.CITY_NAME = \'{0}\'
GROUP BY NE.neighborhood_name, NE.neighborhood_id) down
WHERE up.neighborhood_id = down.neighborhood_id AND up.count1 >= 0.05 * down.count1
        '''.format(city)
    
    #return string_prefix
    c = conn.cursor()
    c.execute(string_prefix)

    df = pd.DataFrame.from_records(list(c))
    columns = [
            {"id": 0, "name": "neighborhood_name"},
            {"id": 1, "name": "neighborhood_id"},
            {"id": 2, "name": "ratio"},
            ]

        
    #return html.Div([string_prefix + date_string])
    return df.to_dict('records'), columns

string_query_4 = '''
\n Find the 5 most cheapest Apartments (based on average price within the available dates) in Berlin
\n available for at least one day between 01-03-2019 and 30-04-2019 having at least 2 beds, a location
\n review score of at least 8, flexible cancellation, and listed by a host with a verifiable government id.
'''
string_query_5 = '''
\n Each property can accommodate different number of people (1 to 16). Find the top-5 rated
\n (review_score_rating) listings for each distinct category based on number of accommodated guests
\n with at least two of these facilities: Wifi, Internet, TV, and Free street parking.
'''

string_query_6 = '''
\nWhat are top three busiest listings per host? The more reviews a listing has, the busier the listing is.
'''

string_query_7 = '''
\nWhat are the three most frequently used amenities at each neighborhood in Berlin for the listings with
\n“Private Room” room type?
'''

string_query_8 = '''
\n What is the difference in the average communication review score of the host who has the most
\n diverse way of verifications and of the host who has the least diverse way of verifications. In case of a
\n multiple number of the most or the least diverse verifying hosts, pick a host one from the most and
\n one from the least verifying hosts.
'''
string_query_9 = '''
\n What is the city who has the highest number of reviews for the room types whose average number of
\n accommodates are greater than 3.
'''

string_query_10 = '''
\n Print all the neighborhoods in Madrid which have at least 50 percent of their listings occupied in year
\n 2019 and their host has joined airbnb before 01.06.2017
'''

##0 param
string_query_11 = '''
\n Print all the countries that in 2018 had at least 20"%"" of their listings available.
'''

# 1 param city
string_query_12 = '''
\n Print all the neighborhouds in Barcelona where more than 5 percent of their accommodation’s
\n cancelation policy is strict with grace period.
'''
####################### End of predefinied queries




#################### Layout insert

#####################end Layout Insert 


######################Tabs callback
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])


def render_content(tab):
    if tab == 'home':
        return html.Div([
            dcc.Markdown(children = markdown_text)],
            style={'marginLeft': 200, 'marginTop': 100, 'width': '49%', 'display': 'inline-block'}
            )
    elif tab == 'search':
        return layout_search
    elif tab == 'predefined_queries':
    	return layout_predefinied
    elif tab == 'insert':
    	return html.Div([
            html.H3('tab content insert')
        ])
    elif tab == 'delete':
    	return html.Div([
            html.H3('Tab content delete')
        ])
    

if __name__ == '__main__':
    app.run_server(debug=True)