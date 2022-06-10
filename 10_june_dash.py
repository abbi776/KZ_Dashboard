#importing libraries
import dash
from dash import dcc
from dash import html
import numpy as np
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
from shapely.geometry import shape
import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 


#data cleaning for parcel 6
s1_time_series_url_p6 = 'https://demodev2.kappazeta.ee/ard_api_demo/v1/time_series/s1?limit_to_rasters=true&parcel_foreign_id=6&properties=parcel_foreign_id%2Cs1product_end_time%2Cs1product_ron%2Ccohvh_avg%2Ccohvv_avg%2Cvhvv_avg'
r_s1_time_series_p6 = requests.get(s1_time_series_url_p6)
json_s1_time_series_p6 = r_s1_time_series_p6.json()
df_s1_time_series_p6 = pd.DataFrame(json_s1_time_series_p6['s1_time_series'])
s2_time_series_url_p6 = 'https://demodev2.kappazeta.ee/ard_api_demo/v1/time_series/s2?limit_to_rasters=true&parcel_foreign_id=6&properties=parcel_foreign_id%2Cs2product_start_time%2Cs2product_ron%2Cndvi_avg'
r_s2_time_series_p6 = requests.get(s2_time_series_url_p6)
json_s2_time_series_p6 = r_s2_time_series_p6.json()
df_s2_time_series_p6 = pd.DataFrame(json_s2_time_series_p6['s2_time_series'])
df_s2_time_series_p6.s2product_start_time=df_s2_time_series_p6.s2product_start_time.str[0:11]
df_s1_time_series_p6.s1product_end_time=df_s1_time_series_p6.s1product_end_time.str[0:11]
dfinal_p6 = df_s1_time_series_p6.merge(df_s2_time_series_p6, how='inner', left_on='s1product_end_time', right_on='s2product_start_time')
cols_p6 = ['parcel_foreign_id_x', 's1product_ron','parcel_foreign_id_y','s2product_ron']
dfinal_p6[cols_p6] = dfinal_p6[cols_p6].apply(pd.to_numeric, errors='coerce', axis=1)


parcels=json.load(open ("C:/Users/AbdullahToqeer/Desktop/dashboard data/parcel_n.geojson"))
for feature in parcels['features']:
    feature['id'] = feature['properties']['parcel_id']
df = pd.read_csv('C:/Users/AbdullahToqeer/Downloads/df_n.csv')
fig = px.choropleth_mapbox (df, geojson=parcels, locations="parcel ID", featureidkey="id", zoom=9.5, center = {"lat": 47.3824, "lon": 2.9253}, height=800, width=1000)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


app.layout = html.Div([
    html.H2('Agriculture Parcels Dashboard', style={'textAlign': 'center'}),
  
    html.Div([
        html.Div([
            html.H4('Parcel # 6', style={'textAlign': 'center','color': 'blue', 'fontSize': 20}),
            dcc.Graph(
        id='scatter_chart',
        figure=px.line(dfinal_p6,x="s1product_end_time", y=["ndvi_avg", "vhvv_avg","cohvv_avg","cohvh_avg"],markers=True, width=1000,height=600,
                      labels={"s1product_end_time": "Date"}))], className="six columns"),

        html.Div([
            html.H4('Parcel location', style={'textAlign': 'center','color': 'blue', 'fontSize': 20}),
            dcc.Graph(figure=fig, className="six columns")
])
])
])



if __name__ == '__main__':
    app.run_server(port=4058)