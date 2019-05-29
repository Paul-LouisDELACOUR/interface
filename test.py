import dash
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import cx_Oracle
import datetime

now = datetime.datetime.now()

dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', sid='ORCLCDB')
conn = cx_Oracle.connect(user=r'C##DB2019_G04', password='DB2019_G04', dsn=dsn_tns)
host_id = 1

host_check = conn.cursor()
host_check.execute('SELECT COUNT(*) from HOST where host_id = {}'.format(host_id))

listing_max = conn.cursor()
listing_max.execute('SELECT MAX(listing_id) FROM LISTING')

print(list(listing_max)[0][0])

acc_cursor = conn.cursor()
acc_cursor.execute('SELECT DISTINCT CA.calendar_date, CA.calendar_id FROM CALENDAR CA, RESERVED_ON RE WHERE RE.calendar_id = CA.calendar_id')

interm_list = [elem for sublist in [(lambda x : [x[0].strftime('%Y-%m-%d'), x[1]])(x) for x in list(acc_cursor)] for elem in sublist]
date_id_dict = dict(zip(interm_list[::2], interm_list[1::2]))
print(date_id_dict)

print(now.strftime("%Y-%m-%d"))