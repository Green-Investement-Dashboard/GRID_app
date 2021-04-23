import pandas
import plotly
import plotly.graph_objs as go

import pandas
import numpy
import json

class Graph:
    def __init__ (self):
      pass
      
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
    
    def plot_ebitda(self):
        data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/sample_data/main/sample_data/ebitda_sample.csv')
        data.loc[:,'date'] = pandas.to_datetime(data.loc[:,'date'])
        data = [go.Bar(x=data.loc[:,'date'], y=data.loc[:,'alerte'])]
        layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                           xaxis_title='Date' , yaxis_title='EBITDA', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                           )
        fig = go.Figure(data=data, layout=layout)
        graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphjson

class Scoring:
    def __init__ (self):
      self.data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/sample_data/scoring.csv')
      self.data = self.data.set_index('indicateur')
    
    def bin (self):
      self.data['min'] = 0.0
      self.data['low_avg'] = 0.9*self.data['average']
      self.data['high_avg'] = 1.1*self.data['average']
    
    def main (self):
      self.bin()
      list_output = []
      for indic in self.data.index:
        indic_val = [self.data.loc[indic, 'value']]
        indic_val.append(self.data.loc[indic, 'max'])
        indic_val.append([self.data.loc[indic, 'min'], self.data.loc[indic, 'low_avg'], self.data.loc[indic, 'high_avg'], float(self.data.loc[indic, 'max'])])
        list_output.append(indic_val)
    
      return list_output

class CriticalAlert:
    def __init__(self):
      self.data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/sample_data/liste_indic.csv')
      self.data = self.data.set_index('Code input')
    
    def main(self):
      list_env = []
      list_soc = []
      list_gouv = []
    
      for an_id in self.data[self.data['Critique']==1].index:
        if 'E' in an_id:
          list_env.append(self.data.loc[an_id, 'Phénomène dangereux'])
    
        if 'S' in an_id:
          list_soc.append(self.data.loc[an_id, 'Phénomène dangereux'])
    
        if 'G' in an_id:
          list_gouv.append(self.data.loc[an_id, 'Phénomène dangereux'])
    
      return [list_env, list_soc, list_gouv]

#Graph().plot_ebitda()



  