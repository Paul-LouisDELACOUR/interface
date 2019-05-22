import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import numpy as np
#import pymysql as _mysql
#import _mysql
import cx_Oracle

from dash.dependencies import Input, Output
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
    html.Div( [
        html.Div([
            html.Label('Start date - end date')
            ]),
        dcc.DatePickerSingle(
            id='start_date',
            min_date_allowed=dt(2000, 8, 5),
            max_date_allowed=dt(2020, 9, 19),
            initial_visible_month=dt(2019, 8, 5),
            date=str(dt(2019, 8, 25, 23, 59, 59))
        ) , 
        dcc.DatePickerSingle(
            id='end_date',
            min_date_allowed=dt(2000, 8, 5),
            max_date_allowed=dt(2020, 9, 19),
            initial_visible_month=dt(2019, 8, 5),
            date=str(dt(2019, 8, 25, 23, 59, 59))
        ) ],
        style={'marginLeft': 10, 'marginTop': 10, 'width': '49%'}
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
        html.Label('Price range'),
        dcc.RangeSlider(
            marks={i: '{} '.format(i) for i in range(500,2000,100)},
            min=500,
            max=2000,
            value=[1, 15]
        ) 
        ],
        style={'marginLeft': 10, 'marginTop': 10, 'width': '100%'}
    ),

    html.Div([
        html.Button('SEARCH FOR YOUR RESERVATION', id='button_reservation')
        ],
        style={'marginLeft': 400, 'marginTop': 40, 'width': '100%'}
    ),
    

    html.Div(id='output_container_search',
        style={'marginLeft': 10, 'marginTop': 50, 'width': '49%', 'display': 'inline-block'}
    )
])

app.config['suppress_callback_exceptions']=True
@app.callback(
    Output(component_id='output_container_search', component_property='children'),
    [
    Input(component_id='loc_id', component_property='value'),
    Input(component_id = 'start_date', component_property = 'date')
    #Input(component_id = 'end_date', component_property = 'date')
    ]
)
def update_output(loc_id_name, date):
    string_prefix = 'The location is "{}"'.format(loc_id_name)
    
    #return string_prefix
    if date is not None:
        string_prefix += ' and you have selected '
        date = date.split(' ')[0]
        date = dt.strptime(date, '%Y-%m-%d')
        date_string = date.strftime('%B %d, %Y')

        dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
        conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
        c = conn.cursor()
        c.execute('select * from BED_TYPE')
        #return html.Div([string_prefix + date_string])
        return pd.DataFrame(list(c)).to_html()

'''
layout_search = html.Div([
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=dt(1995, 8, 5),
        max_date_allowed=dt(2017, 9, 19),
        initial_visible_month=dt(2017, 8, 5),
        date=str(dt(2017, 8, 25, 23, 59, 59))
    ),
    html.Div(id='output-container-date-picker-single')
])

app.config['suppress_callback_exceptions']=True
@app.callback(
    dash.dependencies.Output('output-container-date-picker-single', 'children'),
    [dash.dependencies.Input('my-date-picker-single', 'date')])
def update_output(date):
    string_prefix = 'You have selected: '
    if date is not None:
        date = dt.strptime(date, '%Y-%m-%d')
        date_string = date.strftime('%B %d, %Y')
        return string_prefix + date_string
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
        style={'marginLeft': 10, 'marginTop': 10, 'width': '49%', 'display': 'inline-block'}
    ), 
    html.Div(id = 'output-container' ,
        style={'marginLeft': 10, 'marginTop': 50, 'width': '49%'}
        )
])

app.config['suppress_callback_exceptions']=True
@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('question-dropdown', 'value')])
def update_output(value):
    
    if value == '1'  :
            return html.Div([
                html.Div( [
                    html.Label('param 1 query 1'),
                    dcc.Input(value='exemple', type='text')],
                    style={'marginLeft': 10, 'marginTop': 8, 'width': '100%', 'display': 'inline-block'}
                ) , 
                html.Div( [
                    html.Label('param 2 query 1'),
                    dcc.Input(value='exemple', type='text')],
                    style={'marginLeft': 10, 'marginTop': 8, 'width': '100%', 'display': 'inline-block'}
                ) ,
                html.Div([
                    html.Button('SEARCH', id='button')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                )
            ])
    elif value == '2' : 
            return html.Div([
                html.Div( [
                    html.Label('param 1 query 2'),
                    dcc.Input(value='exemple', type='text')],
                    style={'marginLeft': 10, 'marginTop': 8, 'width': '100%', 'display': 'inline-block'}
                ) , 
                html.Div( [
                    html.Label('param 2 query 2'),
                    dcc.Input(value='exemple', type='text')],
                    style={'marginLeft': 10, 'marginTop': 8, 'width': '100%', 'display': 'inline-block'}
                ),
                html.Div([
                    html.Button('SEARCH', id='button')],
                    style={'marginLeft': 10, 'marginTop': 20, 'width': '100%', 'display': 'inline-block'}
                )

            ])
    elif value == '3' :
            return html.Div([
                html.Label('param 1 query 3'),
                dcc.Input(value='exemple', type='text')
                ]) 
    
    
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