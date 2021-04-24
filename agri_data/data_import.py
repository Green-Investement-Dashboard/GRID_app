import pandas 
import os

class ReadData:
	def __init__ (self, name):
		self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
		self.name = name

	def read_json(self):
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/data_agri.json', orient='table')

		full_path = os.path.normcase(f'{self.current}/{self.name}.json')
		df = pandas.read_json(full_path, orient='table')

		return df

