
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import os
import plotly.graph_objs as go
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
                      html.P('  Select Gender'),
                        html.Div([
                          dcc.RadioItems(
                                      id='dropdown_a',
                                      options=[{'label' : i, 'value': i} for i in['M','F']],
                                      value =''),
                                     ],style = {'width':400, 'margin':25}),
                          html.Br(),#create space
                      html.P('  Select Race'),
                        html.Div([
                          dcc.Dropdown(
                                      id='dropdown_b',
                                      options =
                                      [{'label' : i, 'value': i} for i in['Asian or Pacific Islander',
                                     'Black or African American', 'White','Hispanic or Latino',
                                     'American Indian or Alaska Native']],
                                      value='')],style = {'width':400, 'margin':25}),
                          html.Br(), #space
                        html.Div(id='output-graph')
                        ]),

                    html.Div([
                      html.Strong('BMI Calculator'),
                        html.Div([
                          html.P('  Enter Height in inches'),
                          dcc.Input(id='input-1', type='text', value=''),
                          html.Br(),
                          html.P('  Enter Weight in pounds'),
                          dcc.Input(id='input-2', type='text', value=''),
                          html.Br()])
                        ]),
                    html.Div([
                      html.Strong('Average Body Mass Index by Age'),
                        html.Div([
                          dcc.Graph(
                                  id='BMI_graph')],
                                  style= {'width':'50%','display':'inline-block','padding':'0 20'}),
                        html.Div([
                                dcc.Graph(id='BMI Chart')]
                                ,style={'display': 'inline-block', 'width': '49%'}),
                        html.Div(id='output-graph2')])
                    ])


@app.callback(
        Output(component_id='output-graph',component_property = 'children'),
        [Input(component_id= 'slider-1', component_property='value'),
         Input(component_id='dropdown_a',component_property='value'),
         Input(component_id='dropdown_b',component_property='value')]
        )

def update_value(slider_data,dropdown,dropdownb):
    df= pd.read_csv('health_risk_data.csv')
    df= df[df['Crude Rate'] != 'Unreliable']
    
    df2 = df[df['Age'] == slider_data]
    df2 = df2[df2['Gender']== dropdown]
    df2 = df2[df2['Race']==dropdownb]

    return dcc.Graph(
        id='output-graph1',
        figure={
            'data' : [
                {'x':df2['Cause of Death'],'y':df2['Crude Rate'], 'type':'bar','name': dropdownb},
            ],
            'layout' : {
                'title':'Top Health Risks for Selected Individual'
                    }
                }
            )

@app.callback(
        Output(component_id='output-graph2',component_property = 'children'),
        [Input(component_id= 'input-1', component_property='value'),
         Input(component_id='input-2',component_property='value'),
         Input(component_id='slider-1',component_property='value')]
        )

def update_BMI(input_1,input_2,slider_data):
    slider_age = pd.to_numeric(slider_data)
    height = pd.to_numeric(input_1)
    weight = pd.to_numeric(input_2)
    body_mass_index = (weight * 703) / (height * height)
    if body_mass_index < 18.5:
        over_under = print("A person with a BMI of " + str(body_mass_index ) + " is underwieght ")
    elif body_mass_index < 24.9:
        over_under = print("A person with a BMI of " + str(body_mass_index ) + " is normal weight ")
    else:
        over_under = print("A person with a BMI of " + str(body_mass_index ) + " is overweight ")
    body_mass_index = pd.to_numeric('body_mass_index')   
    
    bmi= pd.read_excel('Average_BMI.xlsx')
    bmi['Age'] = pd.to_numeric(bmi['Age'])
    bmi['Average BMI'] = pd.to_numeric(bmi['Average BMI'])
    trace0= go.Scatter(
                    x= bmi['Age'],
                    y= bmi['Average BMI'],
                    mode = 'lines',
                    name= 'Average')
    trace1 = go.Scatter(
                    x= body_mass_index,
                    y= slider_age,
                    mode = 'markers',
                    size = '30',
                    name = 'You',
                    title = over_under)
    return  dcc.Graph(
            id='output-graph2',
            figure={
            'data': [trace0,trace1],
            'layout': go.Layout(
                    xaxis={
                            'title':'Age'},
                    yaxis={
                            'title':'BMI'},
                    height=450),
                    }
            )

          
if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    