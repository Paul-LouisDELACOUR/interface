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
                {'label': 'Q10', 'value': '10'}
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
                            {'label': 'Desc
ending', 'value': '2'}
                            ],
                        value='1'
    l = list(c)
    return html.Div(l)

############## Q2
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_2', component_property ='children'),
    [Input('search_2', 'n_clicks')],
    [State('q2p1', 'value'),
    State('q2p2' , 'value')]
)
def uptdapte_output(search,q2p1,q2p2) :
    city = 'Madrid'
    if(q2p1 == '2'):    
        city = 'Barcelona'
    elif(q2p2 == '3') :
        city =='berlin'

    review_scores = 'review_scores_rating'
    if(q2p2 == '2') :
        review_scores = 'review_scores_communication'
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
def update_output(search ,q3p1):
    order = 'highest'
    if(q3p1 == '2') :
        order = 'lowest'
    string_prefix_3 = ''' 
        \n Find all the hosts (host_ids, host_names) with the "{}" number of listings.
        '''.format(order)

    return html.Div([string_prefix_3])

############## Q4
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_4', component_property = 'children'),
    [Input('search_4', 'n_clicks')],
    [State('q4p1', 'value'),
    State('q4p2', 'value'),
    State('q4p3', 'value')]
    )
def update_output(search ,q4p1,q4p2,q4p3):
    extremum = 'cheapest'
    if(extremum == 2 ) :
        extremum = 'highest'

    if(q3p1 == '2') :
        order = 'lowest'
    
    cancellation = 'flexible'
    if(q3p2 == '2') :
        cancellation = 'moderate'
    elif(q3p2 == '3') :   
        cancellation = 'strict'
    elif(q3p2 == '4') :   
        cancellation = 'strict_14_with_grace_period'
    elif(q3p2 == '5') :   
        cancellation = 'super_strict_30'
    elif(q3p2 == '6') : cancellation = 'super_strict_60'
    
    beds = '2'
    if(q3p3 == '3') :
        beds = '3'
    elif(q3p3 == '4') :
        beds = '4'
    if(q3p3 == '5') :
        beds = '5'

    string_prefix_4 = '''
    \n Find the 5 most "{}" Apartments (based on average price within the available dates) in Berlin
    \n available for at least one day between 01-03-2019 and 30-04-2019 having at least 2 beds, a location
    \n review score of at least 8, flexible cancellation, and listed by a host with a verifiable government id.
    '''.format(extremum, cancellation, beds)

    return html.Div([string_prefix_4])


############## Q5
app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('output_container_query_5s rqery y', component_property = 'children'),
    [Input('search_1', 'n_clicks')],
    [State('q1p1', 'value')]
    )
def update_output(search ,q1p1):
    order = 'ascending'
    if(q1p1 == '2') :
        order = 'descending'
    string_prefix = ''' 
        \n Print how many hosts in each city have declared the area of their property in square meters. Sort the
        \n output based on the city name in "{}" order
        '''.format(order)

    return html.Div([string_prefix])

############## Q6

############## Q7

############## Q8

############## Q9

############## Q10

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
