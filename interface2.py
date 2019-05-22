import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd

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

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='HOME', value='home'),
        dcc.Tab(label='SEARCH', value='search'),
        dcc.Tab(label='PREDEFINED QUERIES', value='predefined_queries'),
&        dcc.Tab(label='INSERT', value='insert'),
        dcc.Tab(label='DELETE', value='delete'),
    ]),
    html.Div(id='tabs-content')
])

#####Here are the different layouts for the different modes

##Search
'''
layout_search = html.Div([
    dcc.Input(id='loc_id', value='Location', type='text'),
    dcc.DatePickerSingle(
        id='start_date',
        min_date_allowed=dt(1995, 8, 5),
        max_date_allowed=dt(2020, 9, 19),
        initial_visible_month=dt(2017, 8, 5),
        date=str(dt(2019, 8, 25, 23, 59, 59))
    ),
    html.Div(id='output_container_search')
])

app.config['suppress_callback_exceptions']=True
@app.callback(
    Output(component_id='output_container_search', component_property='children'),
    [
    #Input(component_id='loc_id', component_property='value'),
    Input(component_id = 'start_date', component_property = 'date')
    #Input(component_id = 'end_date', component_property = 'date')
    ]
)
def update_output(start_date):
    #string_prefix = 'The location is "{}"'.format(loc_id_name)
    string_prefix = 'You have selected = '
    if start_date is not None :
        date = dt.strptime(start_date , '%Y-%m-%d')
        date_string = date.strftime('%B %d, %Y')
        return string_prefix + date_string 
    else : return string_prefix

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

layout_predefinied = html.Div([
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
	), 
    html.Div(id = 'output-container')
])

app.config['suppress_callback_exceptions']=True
@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('question-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


app.config['suppress_callback_exceptions']=True
@app.callback(
    Output('table-filtering', "data"),
    [Input('table-filtering', "pagination_settings"),
     Input('table-filtering', "filtering_settings")])

def update_graph(pagination_settings, filtering_settings):
    print(filtering_settings)
    filtering_expressions = filtering_settings.split(' && ')
    dff = df
    for filter in filtering_expressions:
        if ' eq ' in filter:
            col_name = filter.split(' eq ')[0]
            filter_value = filter.split(' eq ')[1]
            dff = dff.loc[dff[col_name] == filter_value]
        if ' > ' in filter:
            col_name = filter.split(' > ')[0]
            filter_value = float(filter.split(' > ')[1])
            dff = dff.loc[dff[col_name] > filter_value]
        if ' < ' in filter:
            col_name = filter.split(' < ')[0]
            filter_value = float(filter.split(' < ')[1])
            dff = dff.loc[dff[col_name] < filter_value]

    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('records')




@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])


def render_content(tab):
    if tab == 'home':
        return html.Div([
            dcc.Markdown(children = markdown_text)
        ])
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
