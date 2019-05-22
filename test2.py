import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import cx_Oracle
     
app = dash.Dash()
application = app.server

app.layout = html.Div([
    html.Div([
        html.Iframe(id = 'datatable', height = 500, width = 1200)
    ]),  
    html.Div([
        html.Button('SEARCH FOR YOUR RESERVATION', id='submit-button')
        ],
        style={'marginLeft': 400, 'marginTop': 40, 'width': '100%'}
    )      
])

#boal = False
 
@app.callback(Output('datatable', component_property = 'srcDoc'),
            [Input('submit-button','n_clicks')],)

def update_datatable(button):            
    #df =  pd.read_csv(csv_file)
    
    
    #boal = not boal
    if boal :
        dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
        conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
        c = conn.cursor()
        c.execute('select * from BED_TYPE')
        df = pd.DataFrame(list(c))
        return df.to_html()

    #bool =  not bool
    if not boal :
        dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
        conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
        c = conn.cursor()
        c.execute('select * from ROOM_TYPE')
        df = pd.DataFrame(list(c))
        return df.to_html()
        

if __name__ == '__main__':       
    application.run(debug=False, port=8080)