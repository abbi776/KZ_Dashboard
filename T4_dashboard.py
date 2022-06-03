#importing libraries
import dash
from dash import dcc
from dash import html
import pandas as pd
import requests
import numpy as np
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from plotly.subplots import make_subplots


#css style sheet to modify parts of dashboard
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 



##Graph 1##
#reading data from API
s1_time_series_url_p1 = 'https://demodev2.kappazeta.ee/ard_api_demo/v1/time_series/s1?limit_to_rasters=true&parcel_foreign_id=0&properties=parcel_id%2Cparcel_foreign_id%2Cs1product_end_time%2Cs1product_ron%2Ccohvh_avg%2Ccohvv_avg%2Cvhvv_avg%2Cs0vh_avg%2Cs0vv_avg%20'
r_s1_time_series_p1 = requests.get(s1_time_series_url_p1)
json_s1_time_series_p1 = r_s1_time_series_p1.json()
df_s1_time_series_p1 = pd.DataFrame(json_s1_time_series_p1['s1_time_series'])

s2_time_series_url_p1 = 'https://demodev2.kappazeta.ee/ard_api_demo/v1/time_series/s2?limit_to_rasters=true&parcel_foreign_id=0&properties=parcel_id%2Cparcel_foreign_id%2Cs2product_start_time%2Cs2product_ron%2Cndvi_avg'
r_s2_time_series_p1 = requests.get(s2_time_series_url_p1)
json_s2_time_series_p1 = r_s2_time_series_p1.json()
df_s2_time_series_p1 = pd.DataFrame(json_s2_time_series_p1['s2_time_series'])

#planning to visualize data for sentinel 1 and 2 time series together, as data available on same dates have different time, so taking only day, month and year
df_s2_time_series_p1.s2product_start_time=df_s2_time_series_p1.s2product_start_time.str[0:11]
df_s1_time_series_p1.s1product_end_time=df_s1_time_series_p1.s1product_end_time.str[0:11]

#merging both dataframes based on the columns that have some similar values 
dfinal_p1 = df_s1_time_series_p1.merge(df_s2_time_series_p1, how='inner', left_on='s1product_end_time', right_on='s2product_start_time')
cols_p1 = ['parcel_foreign_id_x', 's1product_ron','parcel_foreign_id_y','s2product_ron']
dfinal_p1[cols_p1] = dfinal_p1[cols_p1].apply(pd.to_numeric, errors='coerce', axis=1)




##Graph 2##
#reading data from API
s1_time_series_url_p2 = 'https://demodev2.kappazeta.ee/ard_api_demo/v1/time_series/s1?limit_to_rasters=true&parcel_foreign_id=10&properties=parcel_id%2Cparcel_foreign_id%2Cs1product_end_time%2Cs1product_ron%2Ccohvh_avg%2Ccohvv_avg%2Cvhvv_avg%2Cs0vh_avg%2Cs0vv_avg%20'
r_s1_time_series_p2 = requests.get(s1_time_series_url_p2)
json_s1_time_series_p2 = r_s1_time_series_p2.json()
df_s1_time_series_p2 = pd.DataFrame(json_s1_time_series_p2['s1_time_series'])

s2_time_series_url_p2 = 'https://demodev2.kappazeta.ee/ard_api_demo/v1/time_series/s2?limit_to_rasters=true&parcel_foreign_id=10&properties=parcel_id%2Cparcel_foreign_id%2Cs2product_start_time%2Cs2product_ron%2Cndvi_avg'
r_s2_time_series_p2 = requests.get(s2_time_series_url_p2)
json_s2_time_series_p2 = r_s2_time_series_p2.json()
df_s2_time_series_p2 = pd.DataFrame(json_s2_time_series_p2['s2_time_series'])

#planning to visualize data for sentinel 1 and 2 time series together, as data available on same dates have different time, so taking only day, month and year
df_s2_time_series_p2.s2product_start_time=df_s2_time_series_p2.s2product_start_time.str[0:11]
df_s1_time_series_p2.s1product_end_time=df_s1_time_series_p2.s1product_end_time.str[0:11]

#merging both dataframes based on the columns that have some similar values 
dfinal_p2 = df_s1_time_series_p2.merge(df_s2_time_series_p2, how='inner', left_on='s1product_end_time', right_on='s2product_start_time')
cols_p2 = ['parcel_foreign_id_x', 's1product_ron','parcel_foreign_id_y','s2product_ron']
dfinal_p2[cols_p2] = dfinal_p2[cols_p2].apply(pd.to_numeric, errors='coerce', axis=1)


#Dashboard heading
app.layout = html.Div([
    html.H2('Agriculture Parcels Dashboard', style={'textAlign': 'center'}),

#Graph 1 display  
    html.Div([
        html.Div([
            html.H4('Parcel # 1', style={'textAlign': 'center','color': 'green', 'fontSize': 20}),
            dcc.Graph(
        id='scatter_chart',
        figure=px.line(dfinal_p1,x="s1product_end_time", y=["ndvi_avg", "s0vv_avg", "s0vh_avg","vhvv_avg","cohvv_avg","cohvh_avg"],markers=True, width=1000,height=600,
                      labels={"s1product_end_time": "Date", "variable": "Parameters"}))], className="six columns"),


#Graph 2 display
        html.Div([
            html.H4('Parcel # 10', style={'textAlign': 'center','color': 'green', 'fontSize': 20}),
            dcc.Graph(
        id='scatter_chart_1',
        figure=px.line(dfinal_p2,x="s1product_end_time", y=["ndvi_avg", "s0vv_avg", "s0vh_avg","vhvv_avg","cohvv_avg","cohvh_avg"],markers=True, width=1000,height=600,
                      labels={"s1product_end_time": "Date", "variable": "Parameters"}))], className="six columns"),
    ], className="row")
])


#running dashboard on server
if __name__ == '__main__':
    app.run_server(port=4056)