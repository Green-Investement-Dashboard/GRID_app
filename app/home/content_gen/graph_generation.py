import plotly.graph_objects as go
import pandas
import json
import plotly
import numpy
from plotly.subplots import make_subplots
from agri_data import data_import
import os

class BulletChart:
    def __init__ (self, indic, indic_name):
        self.data = data_import.ReadData('gauges_data').read_json()
        #self.data = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/gauges_val.json', orient='table')

        self.value_range = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/value_range.json', orient='table')
        self.indic = indic
        self.indic_name = indic_name

    def plot(self):
        data = go.Indicator(mode = "gauge", 
                      gauge = {'shape': "bullet",
                               'steps': [
                                   {'range': [self.value_range.loc[self.indic, 'Min'], self.value_range.loc[self.indic, 'Bin'][0]], 'color': "#e5f5e0"},
                                   {'range': [self.value_range.loc[self.indic, 'Bin'][0], self.value_range.loc[self.indic, 'Bin'][1]], 'color': "#a1d99b"},
                                   {'range': [self.value_range.loc[self.indic, 'Bin'][1], self.value_range.loc[self.indic, 'Max']], 'color': "#31a354"}
                                   ],
                               'axis': {'range': [self.value_range.loc[self.indic, 'Min'], self.value_range.loc[self.indic, 'Max']]},
                               'bar': {'color': "black"}
                               },
                      #title = {'text': f'<b>{self.indic_name}</b>'},
                      value = self.data.loc[self.indic, 'Value'], 
                      #delta = {'reference': 300},
                      domain = {'x': [0, 1], 'y': [0, 1]}
                      )
        
        layout = go.Layout(height=250, 
                     paper_bgcolor='rgba(61,61,51,0.01)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           )

        fig = go.Figure(data, layout)
        #fig.write_html("gauge.html")
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        if self.data.loc[self.indic, 'Value'] < self.value_range.loc[self.indic, 'Bin'][0]:
          color = 'red'
        elif self.data.loc[self.indic, 'Value'] > self.value_range.loc[self.indic, 'Bin'][0] and self.data.loc[self.indic, 'Value'] <= self.value_range.loc[self.indic, 'Bin'][1]:
          color = 'yellow'
        else:
          color = 'red'

        return {'graph':plot_json, 'title': self.indic_name, 'color':color, 'value':self.data.loc[self.indic, 'Value']}

class PieChart:
  def __init__ (self, indic, indic_name):
    #self.data = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/graph_val.json', orient='table')
    self.data =  data_import.ReadData('graph_data').read_json()
    self.value_range = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/value_range.json', orient='table')
    self.indic = indic
    self.indic_name = indic_name
    self.colors = ['#35978f', '#66c2a4', '#c7eae5', "#dfc27d"]
    #tonalités autour du vin ultra gentil :) 

  def plot(self):
    data = go.Pie(labels=self.data.loc[self.indic, 'list_x'], values=self.data.loc[self.indic, 'list_y'], marker=dict(colors=self.colors))
    layout = go.Layout(height=600,
                     paper_bgcolor='rgba(61,61,51,0.01)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                     
                           )
    fig = go.Figure(data, layout)
    #fig.write_html("pie_ch.html")
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

class FinancialChart:
  def __init__ (self, *args):
    #self.data = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/financial_data.json', orient='table')
    self.data =  data_import.ReadData('financial_data').read_json()
    self.data['list_x'] = self.data.apply(lambda x: [pandas.to_datetime(date) for date in x['list_x']], axis=1)
    self.list_indic = args
    self.color = '#3D3D34'

  def plot_bar(self):
    list_graph = []

    for indic in self.list_indic:
      data = go.Bar(x=self.data.loc[indic, 'list_x'], y=self.data.loc[indic, 'list_y'], marker_color=self.color)
      layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , yaxis_title=self.data.loc[indic, 'name'], font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0),
                         )
      fig = go.Figure(data=data, layout=layout)
      graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
      list_graph.append(graphjson)
      #fig.write_html(f"{indic}.html")
    a,b=list_graph

    return list_graph

  def plot_sgl_line (self):
    list_graph = []

    for indic in self.list_indic:
      data = go.Scatter(x=self.data.loc[indic, 'list_x'], y=self.data.loc[indic, 'list_y'])
      layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , yaxis_title=self.data.loc[indic, 'name'], font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                         )
      fig = go.Figure(data=data, layout=layout)
      graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
      list_graph.append(graphjson)
      #fig.write_html(f"{indic}_sgl.html")

    return list_graph

  def plot_mltpl_line (self):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    secondary_axes = False
    for indic in self.list_indic:
      fig.add_trace(go.Scatter(x=self.data.loc[indic, 'list_x'], y=self.data.loc[indic, 'list_y'],
                               name=self.data.loc[indic, 'name']),
                    secondary_y=secondary_axes
                    
                    )
      
      fig.update_layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                         )
      fig.update_yaxes(title_text=self.data.loc[indic, 'name'], secondary_y=secondary_axes)
      secondary_axes=True

    #fig.write_html(f"{indic}_mtpl.html")  
    graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphjson

class CaniculePlot:
  def __init__ (self):
    self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
    self.file_name='data/full_data_heatwave.json'
    self.full_path = os.path.normcase(f'{self.current}/{self.file_name}')
    self.df = pandas.read_json(self.full_path, orient='table')

    self.agri_data =  data_import.ReadData('data_agri').read_json()

    self.colors = ['#3D3D34', '#72B857', '#BA475C', "#4771BA"]

  def find_closest (self):
    temp_df = self.df.reset_index()
    temp_df['diff_lon'] = temp_df['lon'].sub(self.agri_data['Long'].iloc[-1]).abs()
    temp_df['diff_lat'] = temp_df['lat'].sub(self.agri_data['Lat'].iloc[-1]).abs()
    temp_df['global_diff'] = temp_df.apply(lambda x: numpy.sqrt(x['diff_lat']**2 + x['diff_lon']**2), axis=1 )

    self.lat = temp_df.loc[temp_df['global_diff'].idxmin(), 'lat']
    self.lon = temp_df.loc[temp_df['global_diff'].idxmin(), 'lon']
    print(self.lat, self.lon)
    

  def plot (self):
      data_extract = self.df.loc[(self.lat, self.lon, slice(None)), ['HWD_EU_climate']].reset_index()
      
      data = go.Scatter(x=data_extract['time'], y=data_extract['HWD_EU_climate'], line=dict(color=self.colors[0]))
      layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , yaxis_title='Nombre de jours de canicules', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                         )
      fig = go.Figure(data=data, layout=layout)
      self.graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
      
  
  def main(self):
      #self.find_closest()
      self.lat = 43.8 
      self.lon = 3.9
      self.plot()
      
      return self.graphjson
      
      
      



    
if __name__ == '__main__':
  #BulletChart('S1', 'Test').plot()
  #PieChart('G6', "Diversification d'activité").plot()
  #FinancialChart('F1', 'F2').plot_bar()
  #FinancialChart('F1', 'F2').plot_sgl_line()
  #FinancialChart('F1', 'F2').plot_mltpl_line()
  
  PlotCanicule().find_closest()


