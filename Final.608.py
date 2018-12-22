
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import os
os.chdir('C:\\Users\\User\\Desktop\\MSDS\\DATA608\\CUNY_DATA_608\\Final Project')

import warnings
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)
print('x' in np.arange(5))   #returns False, without Warning



app = dash.Dash(__name__)

app.layout = html.Div(children = 
                      [html.H1(children='Personal Heath & Risk App'),
                       html.Div([
                               html.Strong('Top Health Risks'),
                               html.P('  Select Age'),
                               html.Div([
                               dcc.Slider(
                                       id='slider-1',
                                       min=1,
                                       max=10,
                                       step=1,
                                       marks={i: 'Age {}'.format(i) for i in range (10)},
                                       value='1'),
                                       ],style = {'width':400, 'margin':25}),
                                html.Br(), #create space 
                                html.Br(), #create space
                                html.P('  Select Gender'),
                                html.Div([
                                dcc.RadioItems(
                                        id='dropdown_a',
                                        options=[{'label' : i, 'value': i} for i in['M','F']],
                                        value =''),
                                       ],style = {'width':400, 'margin':25}),
                                html.Br(),#create space
                                html.Br(),#create space under
                                html.P('  Select Race'),
                                html.Div([
                                dcc.Dropdown(id='dropdown_b',
                                             options =
                                            [{'label' : i, 'value': i} for i in['Asian or Pacific Islander',
                                             'Black or African American', 'White','Hispanic or Latino',
                                             'American Indian or Alaska Native']],
                                            value='')],style = {'width':400, 'margin':25}),
                                html.Br(), #space
                                
                                html.Div(id='output-graph',
                                style = {'width':700, 'margin':50 })
])
                        
])                       
    
app.css.append_css({
'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})        

@app.callback(
        Output(component_id='output-graph',component_property = 'children'),
        [Input(component_id= 'slider-1', component_property='value'),
         Input(component_id='dropdown_a',component_property='value'),
         Input(component_id='dropdown_b',component_property='value')]
        )

def update_value(slider_data,dropdown,dropdownb):
    df= pd.read_csv('health_risk_data.csv')
    df= df[df['Crude Rate'] != 'Unreliable']
    

    slider_data2 = pd.to_numeric(slider_data)
    
    df = df[df['Age'] == slider_data2]
    df = df[df['Gender']== dropdown]
    df = df[df['Race']==dropdownb]
    

    return dcc.Graph(
        id='example-graph',
        figure={
            'data' : [
                {'x':df['Cause of Death'],'y':df['Crude Rate'], 'type':'bar','name': dropdownb},
            ],
            'layout' : {
                'title':'Top Health Risks for Selected Individual'
                    }
                }
            )

    
    
       
if __name__ == '__main__':
    app.run_server(debug=True)
    
    