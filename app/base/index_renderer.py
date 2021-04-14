import pandas
import plotly
import plotly.graph_objs as go

import pandas
import numpy
import json

def plots():
	co2 = plot_co2()
	pct = plot_pct()
	alerte = plot_alerte()
	ebitda = plot_ebitda()

	return co2, pct, alerte, ebitda
  

def plot_co2():
    data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/sample_data/main/sample_data/co2_sample.csv')
    data.loc[:,'date'] = pandas.to_datetime(data.loc[:,'date'])
    data = [go.Scatter(x=data.loc[:,'date'], y=data.loc[:,'co2'])]
    layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                       xaxis_title='Date' , yaxis_title='Emission de CO2', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                       )
    fig = go.Figure(data=data, layout=layout)
    
    graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphjson



def plot_pct():
    data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/sample_data/main/sample_data/pctge_sample.csv')
    data.loc[:,'date'] = pandas.to_datetime(data.loc[:,'date'])
    data = [go.Scatter(x=data.loc[:,'date'], y=data.loc[:,'pct'])]
    layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                       xaxis_title='Date' , yaxis_title='% femmes', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                       )
    fig = go.Figure(data=data, layout=layout)
    graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphjson

def plot_alerte():
    data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/sample_data/main/sample_data/alerte_sample.csv')
    data.loc[:,'date'] = pandas.to_datetime(data.loc[:,'date'])
    data = [go.Scatter(x=data.loc[:,'date'], y=data.loc[:,'alerte'])]
    layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                       xaxis_title='Date' , yaxis_title='Alertes environmentales', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                       )
    fig = go.Figure(data=data, layout=layout)
    graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphjson

def plot_ebitda():
    data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/sample_data/main/sample_data/ebitda_sample.csv')
    data.loc[:,'date'] = pandas.to_datetime(data.loc[:,'date'])
    data = [go.Bar(x=data.loc[:,'date'], y=data.loc[:,'alerte'])]
    layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                       xaxis_title='Date' , yaxis_title='EBITDA', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                       )
    fig = go.Figure(data=data, layout=layout)
    graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphjson