import pandas
import numpy
import os

class RandomDraw:
	def __init__(self):
		self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))

	def data_agri (self):
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/data_agri.json', orient='table')

		full_path = os.path.normcase(f'{self.current}/data_agri.json')
		print('Saved Data Agri')
		df.to_json(full_path, orient='table', indent=4)

	def financial_data (self):
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/financial_data.json', orient='table')
		
		full_path = os.path.normcase(f'{self.current}/financial_data.json')
		print('Saved Financial Data')
		df.to_json(full_path, orient='table', indent=4)

	def gauges_val (self):
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/gauges_val.json', orient='table')
		
		full_path = os.path.normcase(f'{self.current}/gauges_data.json')
		print('Saved Gauges Val')
		df.to_json(full_path, orient='table', indent=4)

	def graph_val (self):
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/graph_val.json', orient='table')
		
		full_path = os.path.normcase(f'{self.current}/graph_data.json')
		print('Saved Graph Val')
		df.to_json(full_path, orient='table', indent=4)

	def indic_critique (self):
		df = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/liste_indic.csv')

		full_path = os.path.normcase(f'{self.current}/indic_data.json')
		print('Saved Index Critique')
		df.to_json(full_path, orient='table', indent=4)

	def stat_data (self):
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/stat.json', orient='table')
		
		full_path = os.path.normcase(f'{self.current}/stat_data.json')
		print('Saved Stat data')
		df.to_json(full_path, orient='table', indent=4)

	def main(self):
		self.data_agri()
		self.financial_data()
		self.gauges_val()
		self.graph_val()
		self.indic_critique()
		self.stat_data()
		print('data_generated')
