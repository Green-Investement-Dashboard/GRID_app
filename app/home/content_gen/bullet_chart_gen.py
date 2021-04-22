import plotly.graph_objects as go
import pandas
import json
import plotly

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
                      title = {'text': f'<b>{self.indic_name}</b>'},
                      value = self.data.loc[self.indic, 'Value'], 
                      #delta = {'reference': 300},
                      domain = {'x': [0, 1], 'y': [0, 1]},
                      )

		layout = go.Layout(height=200,
                     paper_bgcolor='rgba(61,61,51,0.01)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           )

		fig = go.Figure(data, layout)
		#fig.write_html("gauge.html")
		plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

		return plot_json
    
if __name__ == '__main__':
  BulletChart('S1', 'Test').plot()


