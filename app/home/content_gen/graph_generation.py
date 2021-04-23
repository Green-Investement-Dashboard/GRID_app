import plotly.graph_objects as go
import pandas
import json
import plotly
from plotly.subplots import make_subplots

class BulletChart:
	def __init__ (self, indic, indic_name):
		self.data = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/gauges_val.json', orient='table')
		self.value_range = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/value_range.json', orient='table')
		self.indic = indic
		self.indic_name = indic_name

	def plot(self):
		data = go.Indicator(mode = "number+gauge+delta", 
                      gauge = {'shape': "bullet",
                               'steps': [
                                   {'range': [self.value_range.loc[self.indic, 'Min'], self.value_range.loc[self.indic, 'Bin'][0]], 'color': "#30B32D"},
                                   {'range': [self.value_range.loc[self.indic, 'Bin'][0], self.value_range.loc[self.indic, 'Bin'][1]], 'color': "#FFDD00"},
                                   {'range': [self.value_range.loc[self.indic, 'Bin'][1], self.value_range.loc[self.indic, 'Max']], 'color': "#F03E3E"}
                                   ],
                               'axis': {'range': [self.value_range.loc[self.indic, 'Min'], self.value_range.loc[self.indic, 'Max']]},
                               'bar': {'color': "black"}
                               },
                      #title = {'text': f'<b>{self.indic_name}</b>'},
                      value = self.data.loc[self.indic, 'Value'], 
                      #delta = {'reference': 300},
                      domain = {'x': [0, 1], 'y': [0, 1]},
                      )

		layout = go.Layout(height=250, width=700,
                     paper_bgcolor='rgba(61,61,51,0.01)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           )

		fig = go.Figure(data, layout)
		#fig.write_html("gauge.html")
		plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

		return plot_json

class PieChart:
  def __init__ (self, indic, indic_name):
    self.data = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/graph_val.json', orient='table')
    self.value_range = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/value_range.json', orient='table')
    self.indic = indic
    self.indic_name = indic_name

  def plot(self):
    data = go.Pie(labels=self.data.loc[self.indic, 'list_x'], values=self.data.loc[self.indic, 'list_y'])
    layout = go.Layout(height=600,
                     paper_bgcolor='rgba(61,61,51,0.01)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           )
    fig = go.Figure(data, layout)
    #fig.write_html("pie_ch.html")
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

class FinancialChart:
  def __init__ (self, *args):
    self.data = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/financial_data.json', orient='table')
    self.data['list_x'] = self.data.apply(lambda x: [pandas.to_datetime(date) for date in x['list_x']], axis=1)
    self.list_indic = args

  def plot_bar(self):
    list_graph = []

    for indic in self.list_indic:
      data = go.Bar(x=self.data.loc[indic, 'list_x'], y=self.data.loc[indic, 'list_y'])
      layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , yaxis_title=self.data.loc[indic, 'name'], font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
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


    
if __name__ == '__main__':
  #BulletChart('S1', 'Test').plot()
  #PieChart('G6', "Diversification d'activité").plot()
  FinancialChart('F1', 'F2').plot_bar()
  FinancialChart('F1', 'F2').plot_sgl_line()
  FinancialChart('F1', 'F2').plot_mltpl_line()


