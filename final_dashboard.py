#importing libraries
import dash
import dash_leaflet as dl
import geopandas as gpd
from dash import html, Input, ctx, Output
import dash_leaflet as dl
from dash_extensions.javascript import arrow_function, assign
import geojson
from dash import dcc
import plotly.express as px
import pandas as pd
import requests

#opening parcel geomteries in geojson format
with open('C:/Users/AbdullahToqeer/Desktop/dashboard data/map.geojson') as f:
    geojson_data = geojson.load(f)

#creating empty dataframe to load all the parcels data
column_names = ["parcel_foreign_id_x", "s1product_end_time", "s1product_ron","cohvh_avg", "cohvv_avg", "vhvv_avg","parcel_foreign_id_y", "s2product_start_time", "s2product_ron", "ndvi_avg" ]
df = pd.DataFrame(columns = column_names)

#function to automatically load all the parcels data 
foreign=1

#specify the total number of parcels whose data are needed to be save in dataframe 
while (foreign <=140):   

    #fetching data from API, cleaning it and saving relevant data in the dataframe
    s1_time_series_url_p6 = 'https://demodev2.kappazeta.ee/api-ard_demo/v1/time_series/s1?limit_to_rasters=true&parcel_foreign_id=0&properties=parcel_foreign_id%2Cs1product_end_time%2Cs1product_ron%2Ccohvh_avg%2Ccohvv_avg%2Cvhvv_avg'
    s2_time_series_url_p6 = 'https://demodev2.kappazeta.ee/api-ard_demo/v1/time_series/s2?limit_to_rasters=true&parcel_foreign_id=0&properties=parcel_foreign_id%2Cs2product_start_time%2Cs2product_ron%2Cndvi_avg'
    position = 101
    foreign_n=str(foreign)
    s1_time_series_url_p6 = s1_time_series_url_p6[:position] + foreign_n + s1_time_series_url_p6[position+1:]
    s2_time_series_url_p6 = s2_time_series_url_p6[:position] + foreign_n + s2_time_series_url_p6[position+1:]
    r_s1_time_series_p6 = requests.get(s1_time_series_url_p6)
    r_s2_time_series_p6 = requests.get(s2_time_series_url_p6)
    json_s1_time_series_p6 = r_s1_time_series_p6.json()
    json_s2_time_series_p6 = r_s2_time_series_p6.json()
    df_s1_time_series_p6 = pd.DataFrame(json_s1_time_series_p6['s1_time_series'])
    df_s2_time_series_p6 = pd.DataFrame(json_s2_time_series_p6['s2_time_series'])
    df_s2_time_series_p6.s2product_start_time=df_s2_time_series_p6.s2product_start_time.str[0:11]
    df_s1_time_series_p6.s1product_end_time=df_s1_time_series_p6.s1product_end_time.str[0:11]
    dfinal_p6 = df_s1_time_series_p6.merge(df_s2_time_series_p6, how='inner', left_on='s1product_end_time', right_on='s2product_start_time')
    cols_p6 = ['parcel_foreign_id_x', 's1product_ron','parcel_foreign_id_y','s2product_ron']
    dfinal_p6[cols_p6] = dfinal_p6[cols_p6].apply(pd.to_numeric, errors='coerce', axis=1)
    df = pd.concat([dfinal_p6,df],ignore_index = True)
    foreign = foreign+1

df = df.astype({"parcel_foreign_id_x": str}, errors='raise') 
df['s1product_end_time']= pd.to_datetime(df['s1product_end_time'])

#styling sheets for dashboard
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

classes = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#dashboard layout
app.layout = html.Div([

#dashboard title
    html.H2('ARD Demo Dashboard', style={'textAlign': 'center', 'color': 'cyan'}),

#dropdown menu
    html.Div([
        "Select parcel ID" ,
    dcc.Dropdown(['1', '2', '3','4', '5', '6','7', '8', '9','10',
                  '11', '12', '13','14', '15', '16','17', '18', '19','20',
                  '21', '22', '23','24', '25', '26','27', '28', '29','30',
                  '31', '32', '33','34', '35', '36','37', '38', '39','40',
                  '41', '42', '43','44', '45', '46','47', '48', '49','50',
                  '51', '52', '53','54', '55', '56','57', '58', '59','60',
                  '61', '62', '63','64', '65', '66','67', '68', '69','70',
                  '71', '72', '73','74', '75', '76','77', '78', '79','80',
                  '81', '82', '83','84', '85', '86','87', '88', '89','90',
                  '91', '92', '93','94', '95', '96','97', '98', '99','100',
                  '101', '102', '103','104', '105', '106','107', '108', '109','110',
                  '111', '112', '113','114', '115', '116','117', '118', '119','120',
                  '121', '122', '123','124', '125', '126','127', '128', '129','130',
                  '131', '132', '133','134', '135', '136','137', '138', '139','140'], '1', multi=False, id='my-dropdown', style={"width": "50%"})],style={'color': 'white'}),

#Graph and map
    html.Div([

        html.Div([
            
            dcc.Graph(
                    id='graph',
                       className="six columns",figure={
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background']
                }}
                       ),    
                      
            html.Div([
                dl.Map(center = [47.3824, 2.9253],
                zoom=10,children=[
                    dl.TileLayer(),
                    dl.GeoJSON(data=geojson_data, zoomToBounds=True, zoomToBoundsOnClick=True, hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')), hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="density"),options=dict(style=dict(color="darkgreen")), id="geojson"),
                    ], style={'width': '950px', 'height': '800px', 'margin': "auto", "display": "block"}, id="map"),
],className="six columns")],className='row'),

#display of parcel number upon selecting from map
    html.Div([  
                

                html.Div(id="state",style={'textAlign': 'center', 'color': 'red'},
                       className="six columns")], className='row')
             
])
])

#duplicate callback outputs to make graph chnage from both dropdown input and click from map
@app.callback(Output('graph', 'figure'),Input('my-dropdown', 'value'), Input('geojson', 'hover_feature'), prevent_initial_call=True)

def update_graph(parcel_foreign_id_x_selected, features):
    triggered_id = ctx.triggered_id
    print(triggered_id)
    if triggered_id == 'my-dropdown':
         return draw_graph(parcel_foreign_id_x_selected)
    elif triggered_id == 'geojson':
         return state_hover(features)

def draw_graph(parcel_foreign_id_x_selected):
    dff = df[df.parcel_foreign_id_x==parcel_foreign_id_x_selected]
    fig = px.line(data_frame=dff, x="s1product_end_time", y=["ndvi_avg", "vhvv_avg","cohvv_avg","cohvh_avg"],markers=True, width=1000,height=600,
                      labels={"s1product_end_time": "Date"})
    fig.layout.plot_bgcolor = '#424242'
    fig.layout.paper_bgcolor = '#339999'
    return fig

def state_hover(features):
    if features is not None:
        clickfeatureresult =f"{features['properties']['parcel_id']}"
        dfff= df[df.parcel_foreign_id_x==clickfeatureresult]
        fig = px.line(data_frame=dfff, x="s1product_end_time", y=["ndvi_avg", "vhvv_avg","cohvv_avg","cohvh_avg"],markers=True, width=1000,height=600,
                      labels={"s1product_end_time": "Date"})
    fig.layout.plot_bgcolor = '#424242'
    fig.layout.paper_bgcolor = '#339999'
    return fig

#callback to update the parcel name upon clicking from map
@app.callback(Output("state", "children"), [Input("geojson", "hover_feature")])

def state_hover_name(features):
    if features is not None:
        return f"You selected Parcel # {features['properties']['parcel_id']}"

if __name__ == '__main__':
        app.run_server(port=4099)
