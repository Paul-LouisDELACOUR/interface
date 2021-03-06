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
def layout_searching() : 
    return html.Div([
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

layout_search = layout_searching()

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

                ])
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
                )

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
                )

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
        city = 'barcelona'
    elif(q2p1 == '3') :
        city ='berlin'

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

############### Q12
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_12', component_property = 'children'),
    [Input('search_12', 'n_clicks')],
    [State('q12p1', 'value')]
    )
def update_output(search, q12p1):
    city = 'Madrid'
    if(q12p1 == '1'):
        city = 'Madrid'
    elif(q12p1 == '2'):
        city = 'Barcelona'
    elif(q12p1 == '3'):
        city = 'Berlin'
    string_prefix_12  = '''
    \n Print all the neighborhouds in "{}" where more than 5 percent of their accommodation’s
    \n cancelation policy is strict with grace period.
    '''.format(city)

    return string_prefix_12

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
layout_insert= html.Div([
    html.Div( [
        html.Label('Type of insertion'),
            dcc.Dropdown(
                id = 'insertion_tab',
                options=[
                    {'label': 'Listing', 'value': 'listing'},
                    {'label': 'Host account creation', 'value': 'host'},
                    {'label': 'Review of listing', 'value': 'review'}
                            ],
                    value='3'
           )] ,
            style={'marginLeft': 10, 'marginTop': 5, 'width': '30%', 'display': 'inline-block'}
    ),
    
    html.Div(
        id='insertion_content',
        style = {'marginLeft ': 10 , 'marginTop' : 10 , 'width' : '100%', 'display' : 'inline-block'}
    )
])

@app.callback(Output('insertion_content', 'children'),
    [Input('insertion_tab', 'value')])

def render_content_insert(tab) :
    if tab == 'listing' :
        return layout_insert_listing()
    elif tab == 'host' :
        return layout_insert_host()
    elif tab == 'review' :
        return layout_insert_review()

# Read in the data 
#df = active_inactive10

# Get a list of all the parties
#parties = active_inactive10['Party'].unique()

def layout_insert_listing():
    return html.Div([
        dcc.Dropdown(
            id='madrid_neighbothood',
            options=[
            {'label': 'acacias', 'value': '1'},
            {'label': 'adelfas', 'value': '2'},
            {'label': 'almagro', 'value': '3'},
            {'label': 'almenara', 'value': '4'},
            {'label': 'aluche', 'value': '5'},
            {'label': 'arapiles', 'value': '6'},
            {'label': 'argaelles', 'value': '7'},
            {'label': 'arganzurla', 'value': '8'},
            {'label': 'atocha', 'value': '9'},
            {'label': 'barajas', 'value': '10'},
            {'label': 'bellas vistas','value':'11'},
            {'label': 'bellas vistas','value':'12'},
            {'label': 'bellas vistas','value':'13'},
            {'label': 'bellas vistas','value':'14'},
            {'label': 'bellas vistas','value':'15'},
            {'label': 'bellas vistas','value':'16'},
            {'label': 'bellas vistas','value':'17'},
            {'label': 'bellas vistas','value':'18'},
            
            ],
            multi=True,
            value='All Parties'),
        dcc.Graph(id='funnel-graph'),
    ])

@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Party', 'value')])


def layout_insert_host():
    return html.Div('host')

def layout_insert_review():
    return html.Div('review')

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
    	return layout_insert
    elif tab == 'delete':
    	return html.Div([
            html.H3('Tab content delete')
        ])
    

if __name__ == '__main__':
    app.run_server(debug=True)