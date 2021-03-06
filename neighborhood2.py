import dash
import dash_html_components as html
import dash_table
import dash_core_components as dcc
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State 



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

madrid_n =pd.read_csv('table/madrid.csv',sep=',')
#values_madrid =[(i[0],str(i[1])) for i in madrid_n.values]
barcelona_n =pd.read_csv('table/barcelona.csv',sep=',')
#values_barcelona=[(i[0],str(i[1])) for i in barcelona_n.values]
berlin_n =pd.read_csv('table/berlin.csv',sep=',')
#values_berlin=[(i[0], str(i[1])) for i in berlin_n.values]

location = html.Div([
	html.Div([
		html.Label('City'),
		dcc.Dropdown(
		id = 'cities_n',
		options = [
			{'label' : 'Madrid' , 'value' : 'madrid' },
			{'label' : 'Barcelona' , 'value' : 'barcelona' },
			{'label' : 'Berlin' , 'value' : 'berlin' },
			],
		value = '',
		),
	],
	style ={'marginLeft': 10, 'marginTop': 10, 'width': '50%'}
	),
	
	html.Div([
		html.Label('Neighborhood'),
		html.Div(id='output_container_neighborhood')
	],
	style ={'marginLeft': 10, 'marginTop': 10, 'width': '50%'}
	)
	
])


app.config['suppress_callback_exceptions']=True
@app.callback(
    Output(component_id='output_container_neighborhood', component_property='children'),
    [Input(component_id='cities_n', component_property='value')]
)

def render_target(val):
	if val == 'madrid' :
		return  html.Div([
				dcc.Dropdown(
					id = 'madrid_neighborhood',
					options=[{'label': i[0], 'value': str(i[1])} for i in madrid_n.values],
					value='',
				)
				])
	elif val == 'barcelona' :
		return html.Div([
				dcc.Dropdown(
					id = 'barcelona_neighborhood',
					options=[{'label': i[0], 'value': str(i[1])} for i in barcelona_n.values],
					value='',
				)
				])
	elif val == 'berlin' :
		return html.Div([
				dcc.Dropdown(
					id = 'berlin_neighborhood',
					options=[{'label': i[0], 'value': str(i[1])} for i in berlin_n.values],
					value='',
				)
				])
		
	
def location():
	return location



#if __name__ == '__main__':
  #  app.run_server(debug=True)