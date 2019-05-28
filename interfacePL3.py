import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import numpy as np
import dash_daq as daq
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

'''
html.Div([
        html.Label('Location'),
        dcc.Input(id='loc_id', value='Location', type='text')],
        style={'marginLeft': 10, 'marginTop': 10, 'width': '49%', 'display': 'inline-block'}
    ),
'''


                    

##Search
layout_search = html.Div([

    html.Div( [
        html.Label('Location'),
        dcc.Dropdown(
            id = 'loc_id',
            options=[
                {'label': 'Madrid', 'value': '1'},
                {'label': 'Barcelona', 'value': '2'},
                {'label': 'Berlin', 'value': '3'}
                ],
            value='1'
        )
    ] ,
    style={'marginLeft': 10, 'marginTop': 5, 'width': '50%', 'display': 'inline-block'}
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
        daq.NumericInput(
          id='beds_number',
          max=10,
          value=5,
          min=0
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
    ),

    html.Div([
                dash_table.DataTable(
                    id='datatable-search',
                    data = [],
                    columns = [],
                    pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be',
                    )],
                    style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
                ),
    html.Div([
        dash_table.DataTable(
                    id='d_1_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} )


])

app.config['suppress_callback_exceptions']=True
@app.callback(
    Output(component_id='output_container_search', component_property='children'),
    [
    Input(component_id='loc_id', component_property='value'),
    Input(component_id = 'my-date-picker-range', component_property ='start_date'),
    Input(component_id = 'my-date-picker-range', component_property = 'end_date'),
    Input(component_id = 'beds_number', component_property = 'value'),
    Input(component_id = 'non-linear-range-slider', component_property = 'value')
    ]
)

def update_output(loc_id_name, start_date, end_date, beds,price):
    string_prefix = 'The location is "{}"'.format(get_name_loc(loc_id_name))
    
    #return string_prefix
    if start_date is not None:
        string_prefix += ' and you have selected   start : '
        string_prefix += date_to_string(start_date)
    if end_date is not None :
        string_prefix += ' and ends : '
        string_prefix += date_to_string(end_date)
    if beds is not None :
        string_prefix += ' for a number of "{}" beds '.format(beds)
    if price is not None : 
        transformed_value = [transform_value(v) for v in price]
        price_string = ' and price range is [{:0.2f}, {:0.2f}]'.format(
                transformed_value[0], 
                transformed_value[1])
        string_prefix += price_string

    return html.Div([string_prefix])

def get_name_loc(val) : 
    if(val == '1') :
        return 'Madrid'
    elif(val == '2') : 
        return 'Barcelona'
    else :
        return 'Berlin'
    
def transform_value(value):
    return value

def date_to_string(date):
    date = date.split(' ')[0] 
    date = dt.strptime(date, '%Y-%m-%d')
    date_string = date.strftime('%B %d, %Y')
    return date_string

@app.callback(
    [Output(component_id='d_1_precompute', component_property='data'), Output(component_id='d_1_precompute', component_property='columns')],
    [Input('button_reservation', component_property = 'n_clicks')],
    [State(component_id='loc_id', component_property='value'),
    State(component_id = 'my-date-picker-range', component_property ='start_date'),
    State(component_id = 'my-date-picker-range', component_property = 'end_date'),
    State(component_id = 'beds_number', component_property = 'value'),
    State(component_id = 'non-linear-range-slider', component_property = 'value')]
)

def update_output(search, loc_id_name, start_date, end_date, beds,price):

    if start_date == None or end_date == None : return [], []

    start_date = start_date.split(' ')[0] 
    end_date = end_date.split(' ')[0]
    prices = [transform_value(v) for v in price]
    start_price = prices[0]
    end_price = prices[1]


    if loc_id_name == '3': city = 'berlin'
    elif loc_id_name == '2' : city = 'barcelona'
    else : loc_id_name = 'madrid'

    dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
    conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
    c = conn.cursor()
    c.execute('''SELECT LI.*
    FROM (SELECT LI.listing_id
    FROM LISTING LI, RESERVED_ON RE, CALENDAR CA
    WHERE LI.listing_id = RE.listing_id 
    AND RE.calendar_id = CA.calendar_id
    AND CA.calendar_date >= date \'{0}\'
    AND CA.calendar_date <= date \'{1}\'
    AND LI.beds > {2}
    AND LI.daily_price >= {3}
    AND LI.daily_price <= {4}
    AND RE.available = 't'
    GROUP BY LI.listing_id
    HAVING COUNT(*) = 
    (SELECT COUNT(*) from CALENDAR CA
    WHERE CA.calendar_date >= date \'{0}\'
    AND CA.calendar_date <= date \'{1}\')) ids, LISTING LI
    where ids.listing_id = LI.listing_id'''.format(start_date, end_date, beds, start_price, end_price))


    column_names = [row[0] for row in c.description]
    columns = [{"id" : k, "name" : column_names[k]} for k in range(len(column_names))]

    df = pd.DataFrame.from_records(list(c))
    #return html.Div([string_prefix + date_string])
    return df.to_dict('records'), columns

@app.callback(
    [Output(component_id='datatable-search', component_property='data'), Output(component_id='datatable-search', component_property='columns')],
    [Input('datatable-search', 'pagination_settings'), Input('d_1_precompute', component_property = 'data'), Input(component_id='d_1_precompute', component_property='columns')]
)

def update_output(pagination_settings, data, columns):
    
    return pd.DataFrame(data).iloc[
            pagination_settings['current_page']*pagination_settings['page_size']:
            (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
        ].to_dict('records'), columns


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

####################### End of predefinied queries




#################### Layout insert
layout_insert = html.Div([
     

    html.Div([
        #html.Label('Type of insertion'),
        html.H6('Type of insertion', className = "gs-header gs-text-header padded"),
        html.Div(
            [dcc.Dropdown(
            id='dropdown_insert',
            options=[
            {'label': 'Listing', 'value': '1'},
            {'label': 'Host', 'value': '2'},
            {'label': 'Review', 'value': '3'}
            ],
            value='NYC',
            #size = '400',
            )]
        )],   
        style={'marginLeft': 10, 'marginTop': 5, 'width': '50%', 'display': 'inline-block'}
    ),

    html.Div(id='output_container_insert',
        style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
    ) 

])

app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_insert', 'children'),
    [Input('dropdown_insert', 'value')],
    ##[State('checklist','values')]
    )

def update_output(value):
    if value == '1'  :
        return html.Div([
            
            ### Name
            html.Div([
                html.Label("Listing name"),
                dcc.Input(
                id = 'search_insert',
                placeholder='',
                type='text',
                value='',
                size = '50'
                )],
            style={'marginLeft': 10, 'marginTop': 10, 'width': '100%', 'display': 'inline-block'}
            ),

            ### Price
            html.Div([
                html.Div([
                    html.Label("Daily price"),
                    html.Div([
                        daq.Slider(
                        id = 'daily_slider',
                        min=0,
                        max=500,
                        value=50,
                        handleLabel={"showCurrentValue": True,"label": "VALUE"},
                        step=10
                        )
                    ] ,
                    style={'marginTop': 40, 'width': '100%'}
                    )
                ], 
                className="six columns"
                ),
                html.Div([
                    html.Label("Weekly price"),
                    html.Div([
                        daq.Slider(
                        id = 'weekly_slider',
                        min=0,
                        max=2000,
                        value=50,
                        handleLabel={"showCurrentValue": True,"label": "VALUE"},
                        step=10,
                        #height = 12
                        )
                    ] ,
                    style={'marginTop': 40, 'width': '100%'}
                    )
                ],
                className="six columns"
                ),
            ],
            style={'marginLeft': 10, 'marginTop': 10, 'width': '100%'}
            ),
            
            ### Availability and number of beds 
            html.Div([
                ### Availability
                html.Div([
                    html.Div([
                        html.Label('Availability')
                    ]),
                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=dt(2019, 8, 5),
                        max_date_allowed=dt(2019, 9, 19),
                        initial_visible_month=dt(2019, 8, 5),
                    )],
                className="six columns",
                style ={'marginLeft': 10, 'marginTop': 10, 'width': '100%'}
                ),

                ###beds
                html.Div([
                    html.Label('Number of beds'),
                    daq.NumericInput(
                    id='beds_number_insert',
                    max=10,
                    value=5,
                    min=0
                )] , 
                className="six columns",
                style={'marginLeft': 10, 'marginTop': 10, 'width': '49%', 'display': 'inline-block'}
                ),
            ],
            style={'marginLeft': 10, 'marginTop': 10, 'width': '100%'}
            ),

            html.Div([
                html.Label("Accommodates"),

                dcc.Checklist(
                id = 'accommodates' ,
                options=[
                    {'label': 'TV', 'value': '71'},
                    {'label': 'Sound system', 'value': '8'},
                    {'label': 'Printer', 'value': '9'},
                    {'label': 'Oven', 'value': '52'},
                    {'label': 'Microwave', 'value': '15'},
                    {'label': 'Pool cover', 'value': '150'},
                    {'label': 'Pool', 'value': '37'},
                    {'label': 'DVD player', 'value': '16'},
                    {'label': 'Gym', 'value': '21'},
                    {'label': 'netflix', 'value': '24'},
                    {'label': 'Full kitchen', 'value': '27'},
                    {'label': 'Hair dryer', 'value': '30'},
                    {'label': 'Washer', 'value': '35'},
                    {'label': 'Outdoor parking', 'value': '45'},
                    {'label': 'Internet', 'value': '55'},
                    {'label': 'Terrace', 'value': '137'},
                ],
                values=['host', 'listing' , 'neighborhood', 'amenity', 'bed_type',
                    'calendar', 'cancellation', 'city', 'country', 'host_verifications',
                    'is_equiped_with', 'property_type', 'reserved_on' , 'response_time',
                    'reviewer', 'reviews', 'room_type', 'verifies'],
                labelStyle={'display': 'inline-block'}
                )],
                style={'marginLeft': 10, 'marginTop': 10, 'width': '100%', 'display': 'inline-block'}
            ),

            ### Property_type and description
            html.Div([
                html.Div( [
                html.Label("Property_type"),
                dcc.Dropdown(
                    id = 'property_type_dropdown',
                    options=[
                        {'label': 'Apartment', 'value': '1'},
                        {'label': 'Hostel', 'value': '2'},
                        {'label': 'Loft', 'value': '3'},
                        {'label': 'Guest suite', 'value': '4'},
                        {'label': 'House', 'value': '5'},
                        {'label': 'Serviced apartment', 'value': '6'},
                        {'label': 'Other', 'value': '7'},
                        {'label': 'Condominium', 'value': '8'},
                        {'label': 'Townhouse', 'value': '9'},
                        {'label': 'Bed and breakfast', 'value': '10'},
                        {'label': 'Guesthouse', 'value': '11'},
                        {'label': 'Chalet', 'value': '12'},
                        {'label': 'Aparthotel', 'value': '13'},
                        {'label': 'Casa particularDome house', 'value': '14'},
                        {'label': 'Dome House', 'value': '15'},
                        {'label': 'Boutique hotel', 'value': '16'},
                        {'label': 'Hotel', 'value': '17'},
                        {'label': 'Camper/rv', 'value': '18'},
                        {'label': 'Hut', 'value': '19'},
                        {'label': 'Tiny House', 'value': '20'},
                        {'label': 'Villa', 'value': '21'},
                        {'label': 'Dorm', 'value': '22'},
                        {'label': 'Earth House', 'value': '23'},
                        {'label': 'Pension (South Korea)', 'value': '24'},
                        {'label': 'Cottage', 'value': '25'},
                        {'label': 'Bungalow', 'value': '26'},
                        {'label': 'Cabin', 'value': '27'},
                        {'label': 'Castle', 'value': '28'},
                        {'label': 'Boat', 'value': '29'},
                        {'label': 'Houseboat', 'value': '30'},
                        {'label': 'Tipi', 'value': '31'},
                        {'label': 'Resort', 'value': '32'},
                        {'label': 'Train', 'value': '33'},
                        {'label': 'In-Law', 'value': '34'},
                        {'label': 'Cave', 'value': '35'},
                        {'label': 'Barn', 'value': '36'},
                        {'label': 'Farm stay', 'value': '37'},

                    ],
                    value='1'
                    )
                ] ,
                className="six columns",
                style={'marginLeft': 10, 'marginTop': 10, 'width': '30%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Label("description"),
                    dcc.Textarea(
                        placeholder='Enter a value...',
                        value='Describe in a few words...',
                        style={'width': '100%'}
                    )  
                ] ,
                className="six columns",
                style={'marginLeft': 10, 'marginTop': 10, 'marginBotom' : 20, 'width': '30%', 'display': 'inline-block'}
                ),

                html.Div([
                    html.Button('INSERT', id='button_insert')
                ],
                className="six columns",
                style={'marginLeft': 10, 'marginTop': 10, 'marginBotom' : 20, 'width': '50%', 'display': 'inline-block'}
                )     
            ],
            style={'marginLeft': 10, 'marginTop': 10, 'width': '100%'}
            )
        ])

    elif value == '2' :
        return html.Div([
            html.Div([
                html.Label("Host name"),
                dcc.Input(
                    id = 'host_insert',
                    placeholder='',
                    type='text',
                    value=''
                )
            ]),
            html.Div([
                html.Label("Host about"),
                dcc.Textarea(
                    placeholder='Enter a description...',
                    value='Describe in a few words...',
                    style={'width': '100%'}
                )  
            ] ,
             style={'marginLeft': 0, 'marginTop': 10, 'marginBotom' : 20, 'width': '30%', 'display': 'inline-block'}
            ),

            html.Div( [
                html.Label('Location / neighborhood'),
                dcc.Dropdown(
                    id = 'loc_id',
                    options=[
                      {'label': 'Madrid', 'value': '1'},
                       {'label': 'Barcelona', 'value': '2'},
                       {'label': 'Berlin', 'value': '3'}
                    ],
                    value='1'
                )
            ] ,

            style={'marginLeft': 10, 'marginTop': 5, 'width': '50%', 'display': 'inline-block'}
            ),

            html.Div([
                html.Label("Response Time"),
                dcc.Dropdown(
                    id = 'response_time',
                    options=[
                        {'label': 'Within an hour', 'value': '1'},
                        {'label': 'Within a few hours', 'value': '2'},
                        {'label': 'Within a day', 'value': '3'},
                        {'label': 'A few days or more', 'value': '4'},
                        {'label': 'Not specified', 'value': '5'}
                    ],
                    value = '5'
                )

            ],
            style={'marginLeft': 0, 'marginTop': 5, 'width': '40%', 'display': 'inline-block'}
            ),

            html.Div([
                html.Button('ENROLL', id='button_enroll')
            ],
            style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
            ),
        ],
        style={'marginLeft': 10, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
        )

    elif value == '3' :
        return html.Div([
            html.Div([
                html.Div([
                    html.Label('Listing ID'),
                    dcc.Input(
                        id = 'l_id',
                        placeholder='',
                        type='text',
                        value=''
                    ),
                ],
                 className="six columns",
                ),
                html.Div([
                    html.Label('Reviewer ID'),
                    dcc.Input(
                        id = 'r_id',
                        placeholder='',
                        type='text',
                        value=''
                    ),
                ],
                 className="six columns",
                ),
            ],
            style={'marginLeft': 10, 'marginTop': 20, 'marginBotom' : 10, 'width': '100%', 'display': 'inline-block'}
            ),
            
            
            html.Div([
                    #html.Label("Review for lisiting :  by Reviewer: "),
                    html.Div(
                        id='output_container_review_listing',
                        style={'marginLeft': 10, 'marginTop': 50, 'width': '80%', 'display': 'inline-block'}
                    ),
                    dcc.Textarea(
                        placeholder='Enter a value...',
                        value='',
                        style={'width': '100%'}
                    )  
            ] ,
            #className="six columns",
            style={'marginLeft': 10, 'marginTop': 10, 'marginBotom' : 10, 'width': '80%', 'display': 'inline-block'}
            ),

            html.Div([
                html.Button('INSERT THE REVIEW', id='button_insert')
            ],
            style={'marginLeft': 50, 'marginTop': 10, 'marginBotom' : 10, 'width': '80%', 'display': 'inline-block'}
            )
        ],
        #style={'marginLeft': 10, 'marginTop': 5, 'width': '100%', 'display': 'inline-block'}
        )

@app.callback(Output('output_container_review_listing', 'children'),
              [Input('l_id', 'value'),
              Input('r_id', 'value')]) 
def render_content(l_id,r_id) :
    string = 'Review for the listing : {} \n by reviewer {}'.format(l_id,r_id)
    return string


#####################end Layout Insert 

###################### Layout DELETE
layout_delete = html.Div([
    html.Div([
        html.H3('Tab content delete')
    ])
])

#################### End layout DELETE

######################Tabs callback
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])


def render_content(tab):
    if tab == 'home':
        return home_layout
    elif tab == 'search':
        return layout_search
    elif tab == 'predefined_queries':
    	return layout_predefinied
    elif tab == 'insert':
    	return layout_insert
    elif tab == 'delete':
    	return layout_delete

home_layout = html.Div([
            html.Div([
                dcc.Markdown(children = markdown_text)
                ],
                style={'marginLeft': 20, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Checklist(
                id = 'checklist' ,
                options=[
                    {'label': 'Host', 'value': 'host'},
                    {'label': 'Listing', 'value': 'listing'},
                    {'label': 'Neighborhood', 'value': 'neighborhood'},
                    {'label': 'Amenity equipment', 'value': 'amenity'},
                    {'label': 'Bed type', 'value': 'bed_type'},
                    {'label': 'Calendar', 'value': 'calendar'},
                    {'label': 'Cancellation policy', 'value': 'cancellation'},
                    {'label': 'City', 'value': 'city'},
                    {'label': 'Country', 'value': 'country'},
                    {'label': 'Host Verifications', 'value': 'host_verifications'},
                    {'label': 'Equipement', 'value': 'is_equiped_with'},
                    {'label': 'Property type', 'value': 'property_type'},
                    {'label': 'Reservation', 'value': 'reserved_on'},
                    {'label': 'Response Time', 'value': 'response_time'},
                    {'label': 'Reviewer', 'value': 'reviewer'},
                    {'label': 'Reviews', 'value': 'reviews'},
                    {'label': 'Room type', 'value': 'room_type'},
                    {'label': 'Verifies', 'value': 'verifies'},
                ],
                values=['host', 'listing', 'reviews'],
                labelStyle={'display': 'inline-block'}
                )],
                style={'marginLeft': 10, 'marginTop': 10, 'width': '100%', 'display': 'inline-block'}
            ),
            html.Div([
                html.Div([
                    html.Label('Search in the website'),
                ],
                style = {'marginLeft' : 20}
                ),
                dcc.Input(id='research_input', value='', type='text'),
                html.Div([
                    html.Button('Enter', id='search_home')],
                    style={'marginLeft': 40, 'marginTop': 10, 'width': '100%', 'display': 'inline-block'}
                ),
            ],
                style={'marginLeft': 300, 'marginTop': 50, 'width': '100%', 'display': 'inline-block'}
            ),
            html.Div([
            dash_table.DataTable(
            id='datatable-search-host',
            data = [],
            columns = [],
            pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be',
                    ),
            ],
            style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-listing',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-neighborhood',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-amenity_equipment',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-bedtype',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-calendar',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-cancellation_policy',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-city',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-country',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-host_verifications',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-is_equiped_with',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-property_type',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-reservation',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-response_time',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-reviewer',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-reviews',
                data = [],
                columns = [],
                 pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-room_type',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),
            html.Div([
                dash_table.DataTable(
                id='datatable-search-verifies',
                data = [],
                columns = [],
                pagination_settings={
                        'current_page': 0,
                        'page_size': 5
                    },
                    pagination_mode='be'
                ),],
                style={'marginLeft': 10, 'marginTop': 50, 'width': '90%', 'display': 'inline-block'}
            ),


            html.Div([
        dash_table.DataTable(
                    id='d_a_precompute',
                    data = [],
                    columns = []

                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_2_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_3_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_4_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_5_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_6_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_7_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_8_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_9_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_10_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_11_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_12_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_13_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_14_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_15_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_16_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_17_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} ),
            html.Div([
        dash_table.DataTable(
                    id='d_18_precompute',
                    data = [],
                    columns = [],
                    )  ], style = {'visibility' : 'hidden'} )
        ])

@app.callback(
    [Output('d_a_precompute' , component_property ='data'), Output('d_a_precompute' , component_property ='columns'),
    Output('d_2_precompute' , component_property ='data'), Output('d_2_precompute' , component_property ='columns'),
    Output('d_3_precompute' , component_property ='data'), Output('d_3_precompute' , component_property ='columns'),
    Output('d_4_precompute' , component_property ='data'), Output('d_4_precompute' , component_property ='columns'),
    Output('d_5_precompute' , component_property ='data'), Output('d_5_precompute' , component_property ='columns'),
    Output('d_6_precompute' , component_property ='data'), Output('d_6_precompute' , component_property ='columns'),
    Output('d_7_precompute' , component_property ='data'), Output('d_7_precompute' , component_property ='columns'),
    Output('d_8_precompute' , component_property ='data'), Output('d_8_precompute' , component_property ='columns'),
    Output('d_9_precompute' , component_property ='data'), Output('d_9_precompute' , component_property ='columns'),
    Output('d_10_precompute' , component_property ='data'), Output('d_10_precompute' , component_property ='columns'),
    Output('d_11_precompute' , component_property ='data'), Output('d_11_precompute' , component_property ='columns'),
    Output('d_12_precompute' , component_property ='data'), Output('d_12_precompute' , component_property ='columns'),
    Output('d_13_precompute' , component_property ='data'), Output('d_13_precompute' , component_property ='columns'),
    Output('d_14_precompute' , component_property ='data'), Output('d_14_precompute' , component_property ='columns'),
    Output('d_15_precompute' , component_property ='data'), Output('d_15_precompute' , component_property ='columns'),
    Output('d_16_precompute' , component_property ='data'), Output('d_16_precompute' , component_property ='columns'),
    Output('d_17_precompute' , component_property ='data'), Output('d_17_precompute' , component_property ='columns'),
    Output('d_18_precompute' , component_property ='data'), Output('d_18_precompute' , component_property ='columns')],
    [Input('search_home','n_clicks')],
    [State('checklist','values'),
    State('research_input', 'value')]
    )
        
def render_target_insert(n_clicks,checklist, value) : 
    table_set = ['host', 'listing', 'neighborhood', 'amenity_equipment', 'bed_type',
            'calendar', 'cancellation_policy', 'city', 'country', 'host_verifications',
            'is_equiped_with', 'property_type', 'reserved_on' , 'response_time',
            'reviewer', 'reviews', 'room_type', 'verifies']
    selected_tables = checklist

    dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
    conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
            
    columns_list = []
    for i in table_set:
        cmd = 'SELECT * FROM ' + i + ' WHERE 1 = 2'
        c = conn.cursor()
        c.execute(cmd)
        columns = [row[0] for row in c.description]
        columns_list.append(columns)

    string_prefices = []
    for i in range(len(table_set)):
        if table_set[i] in checklist :
            string_where = ' WHERE '
            for j in range(len(columns_list[i])):
                string_where += ' REGEXP_LIKE(' + str(columns_list[i][j]) + ', \'' + str(value) + '\', \'im\')'  
                if j < (len(columns_list[i]) - 1):
                    string_where += ' OR '
            string_prefix = 'SELECT * FROM '+ table_set[i] + string_where + 'FETCH FIRST 100 ROWS ONLY'
            string_prefices.append(string_prefix)
        else : string_prefices.append([])

    results = []

    for i in range(len(table_set)):
        if table_set[i] in checklist :
            string_prefix = string_prefices[i]
            c = conn.cursor()
            c.execute(string_prefix)
            l = list(c)
            if table_set[i] == 'host' :
                for j in range(len(l)):
                    tu = list(l[j])
                    tu.pop(4)
                    l[j] = tuple(tu)
            if table_set[i] == 'reviews' :
                for j in range(len(l)):
                    tu = list(l[j])
                    tu.pop(3)
                    l[j] = tuple(tu)
            df = pd.DataFrame.from_records(l)
            column_names = [row[0] for row in c.description if (row[0] != 'HOST_ABOUT' and row[0] != 'COMMENTS')]
            columns = [{"id" : k, "name" : column_names[k]} for k in range(len(column_names))]
            results.append(df.to_dict('records'))
            results.append(columns)
        else : 
            results.append([])
            results.append([])
    
    return results

@app.callback(
    [Output('datatable-search-host' , component_property ='data'), Output('datatable-search-host' , component_property ='columns'),
    Output('datatable-search-listing' , component_property ='data'), Output('datatable-search-listing' , component_property ='columns'),
    Output('datatable-search-neighborhood' , component_property ='data'), Output('datatable-search-neighborhood' , component_property ='columns'),
    Output('datatable-search-amenity_equipment' , component_property ='data'), Output('datatable-search-amenity_equipment' , component_property ='columns'),
    Output('datatable-search-bedtype' , component_property ='data'), Output('datatable-search-bedtype' , component_property ='columns'),
    Output('datatable-search-calendar' , component_property ='data'), Output('datatable-search-calendar' , component_property ='columns'),
    Output('datatable-search-cancellation_policy' , component_property ='data'), Output('datatable-search-cancellation_policy' , component_property ='columns'),
    Output('datatable-search-city' , component_property ='data'), Output('datatable-search-city' , component_property ='columns'),
    Output('datatable-search-country' , component_property ='data'), Output('datatable-search-country' , component_property ='columns'),
    Output('datatable-search-host_verifications' , component_property ='data'), Output('datatable-search-host_verifications' , component_property ='columns'),
    Output('datatable-search-is_equiped_with' , component_property ='data'), Output('datatable-search-is_equiped_with' , component_property ='columns'),
    Output('datatable-search-property_type' , component_property ='data'), Output('datatable-search-property_type' , component_property ='columns'),
    Output('datatable-search-reservation' , component_property ='data'), Output('datatable-search-reservation' , component_property ='columns'),
    Output('datatable-search-response_time' , component_property ='data'), Output('datatable-search-response_time' , component_property ='columns'),
    Output('datatable-search-reviewer' , component_property ='data'), Output('datatable-search-reviewer' , component_property ='columns'),
    Output('datatable-search-reviews' , component_property ='data'), Output('datatable-search-reviews' , component_property ='columns'),
    Output('datatable-search-room_type' , component_property ='data'), Output('datatable-search-room_type' , component_property ='columns'),
    Output('datatable-search-verifies' , component_property ='data'), Output('datatable-search-verifies' , component_property ='columns')],
    [Input('d_a_precompute' , component_property ='data'), Input('d_a_precompute' , component_property ='columns'), Input('datatable-search-host', 'pagination_settings'),
    Input('d_2_precompute' , component_property ='data'), Input('d_2_precompute' , component_property ='columns'), Input('datatable-search-listing', 'pagination_settings'),
    Input('d_3_precompute' , component_property ='data'), Input('d_3_precompute' , component_property ='columns'), Input('datatable-search-neighborhood', 'pagination_settings'),
    Input('d_4_precompute' , component_property ='data'), Input('d_4_precompute' , component_property ='columns'), Input('datatable-search-amenity_equipment', 'pagination_settings'),
    Input('d_5_precompute' , component_property ='data'), Input('d_5_precompute' , component_property ='columns'), Input('datatable-search-bedtype', 'pagination_settings'),
    Input('d_6_precompute' , component_property ='data'), Input('d_6_precompute' , component_property ='columns'), Input('datatable-search-calendar', 'pagination_settings'),
    Input('d_7_precompute' , component_property ='data'), Input('d_7_precompute' , component_property ='columns'), Input('datatable-search-cancellation_policy', 'pagination_settings'),
    Input('d_8_precompute' , component_property ='data'), Input('d_8_precompute' , component_property ='columns'), Input('datatable-search-city', 'pagination_settings'),
    Input('d_9_precompute' , component_property ='data'), Input('d_9_precompute' , component_property ='columns'), Input('datatable-search-country', 'pagination_settings'),
    Input('d_10_precompute' , component_property ='data'), Input('d_10_precompute' , component_property ='columns'), Input('datatable-search-host_verifications', 'pagination_settings'),
    Input('d_11_precompute' , component_property ='data'), Input('d_11_precompute' , component_property ='columns'), Input('datatable-search-is_equiped_with', 'pagination_settings'),
    Input('d_12_precompute' , component_property ='data'), Input('d_12_precompute' , component_property ='columns'), Input('datatable-search-property_type', 'pagination_settings'),
    Input('d_13_precompute' , component_property ='data'), Input('d_13_precompute' , component_property ='columns'), Input('datatable-search-reservation', 'pagination_settings'),
    Input('d_14_precompute' , component_property ='data'), Input('d_14_precompute' , component_property ='columns'), Input('datatable-search-response_time', 'pagination_settings'),
    Input('d_15_precompute' , component_property ='data'), Input('d_15_precompute' , component_property ='columns'), Input('datatable-search-reviewer', 'pagination_settings'),
    Input('d_16_precompute' , component_property ='data'), Input('d_16_precompute' , component_property ='columns'), Input('datatable-search-reviews', 'pagination_settings'),
    Input('d_17_precompute' , component_property ='data'), Input('d_17_precompute' , component_property ='columns'), Input('datatable-search-room_type', 'pagination_settings'),
    Input('d_18_precompute' , component_property ='data'), Input('d_18_precompute' , component_property ='columns'), Input('datatable-search-verifies', 'pagination_settings')]
    )

def display_tables(d1, c1, p1, d2, c2, p2, d3, c3, p3, d4, c4, p4, d5, c5, p5, d6, c6, p6, d7, c7, p7, d8, c8, p8, d9, c9, p9, d10, c10, p10, d11, c11, p11, d12, c12, p12, d13, c13, p13, d14, c14, p14, d15, c15, p15, d16, c16, p16, d17, c17, p17, d18, c18, p18):
    
    return pd.DataFrame(d1).iloc[
            p1['current_page']*p1['page_size']:
            (p1['current_page'] + 1)*p1['page_size']
        ].to_dict('records'), c1, pd.DataFrame(d2).iloc[
            p2['current_page']*p2['page_size']:
            (p2['current_page'] + 1)*p2['page_size']
        ].to_dict('records'), c2, pd.DataFrame(d3).iloc[
            p3['current_page']*p3['page_size']:
            (p3['current_page'] + 1)*p3['page_size']
        ].to_dict('records'), c3, pd.DataFrame(d4).iloc[
            p4['current_page']*p4['page_size']:
            (p4['current_page'] + 1)*p4['page_size']
        ].to_dict('records'), c4, pd.DataFrame(d5).iloc[
            p5['current_page']*p5['page_size']:
            (p5['current_page'] + 1)*p5['page_size']
        ].to_dict('records'), c5, pd.DataFrame(d6).iloc[
            p6['current_page']*p6['page_size']:
            (p6['current_page'] + 1)*p6['page_size']
        ].to_dict('records'), c6, pd.DataFrame(d7).iloc[
            p7['current_page']*p7['page_size']:
            (p7['current_page'] + 1)*p7['page_size']
        ].to_dict('records'), c7, pd.DataFrame(d8).iloc[
            p8['current_page']*p8['page_size']:
            (p8['current_page'] + 1)*p8['page_size']
        ].to_dict('records'), c8, pd.DataFrame(d9).iloc[
            p9['current_page']*p9['page_size']:
            (p9['current_page'] + 1)*p9['page_size']
        ].to_dict('records'), c9, pd.DataFrame(d10).iloc[
            p10['current_page']*p10['page_size']:
            (p10['current_page'] + 1)*p10['page_size']
        ].to_dict('records'), c10, pd.DataFrame(d11).iloc[
            p11['current_page']*p11['page_size']:
            (p11['current_page'] + 1)*p11['page_size']
        ].to_dict('records'), c11, pd.DataFrame(d12).iloc[
            p12['current_page']*p12['page_size']:
            (p12['current_page'] + 1)*p12['page_size']
        ].to_dict('records'), c12, pd.DataFrame(d13).iloc[
            p13['current_page']*p13['page_size']:
            (p13['current_page'] + 1)*p13['page_size']
        ].to_dict('records'), c13, pd.DataFrame(d14).iloc[
            p14['current_page']*p14['page_size']:
            (p14['current_page'] + 1)*p14['page_size']
        ].to_dict('records'), c14, pd.DataFrame(d15).iloc[
            p15['current_page']*p15['page_size']:
            (p15['current_page'] + 1)*p15['page_size']
        ].to_dict('records'), c15, pd.DataFrame(d16).iloc[
            p16['current_page']*p16['page_size']:
            (p16['current_page'] + 1)*p16['page_size']
        ].to_dict('records'), c16, pd.DataFrame(d17).iloc[
            p17['current_page']*p17['page_size']:
            (p17['current_page'] + 1)*p17['page_size']
        ].to_dict('records'), c17, pd.DataFrame(d18).iloc[
            p18['current_page']*p18['page_size']:
            (p18['current_page'] + 1)*p18['page_size']
        ].to_dict('records'), c18

if __name__ == '__main__':
    app.run_server(debug=True)