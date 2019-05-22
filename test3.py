import dash
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import cx_Oracle


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)

app = dash.Dash(__name__)

PAGE_SIZE = 5

app.layout = html.Div([dash_table.DataTable(
    id='datatable',
    data = [],
    columns=[],
),
    dcc.Dropdown(id = 'My Dropdown', options = [{'label': '1', 'value': '1'}, {'label' : '2', 'value' : '2'}], value = '1')
])


@app.callback(
    [Output('datatable', 'data'), Output('datatable', 'columns')],
    [Input('My Dropdown', 'value')])
def update_graph(value):
    if value == '1':
        c = conn.cursor()
        c.execute('select * from BED_TYPE') 
        columns = [
            {"id": 0, "name": "bedtype id"},
            {"id": 1, "name": "bedtype_name"},
            ]
        return pd.DataFrame.from_records(list(c)).to_dict('records'), columns
    elif value == '2':
        c2 = conn.cursor()
        c2.execute('select * from ROOM_TYPE') 
        columns = [
            {"id": 0, "name": "roomtype id"},
            {"id": 1, "name": "roomtype_name"},
            ]
        return pd.DataFrame.from_records(list(c2)).to_dict('records'), columns


if __name__ == '__main__':
    app.run_server(debug=True)