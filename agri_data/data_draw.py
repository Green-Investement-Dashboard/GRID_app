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
		v0 = {'F1':1000, 'F2':1.2}
		var = {'F1': [1.03, 1.1], 'F2': [0.95, 1.2]}

		for index in df.index :
			new_list = [numpy.random.random()*(var[index][1]*v0[index] - var[index][0]*v0[index]) + var[index][1]*v0[index]]
			for k in range(len(df.loc[index, 'list_x'])-1):
				rd_num = numpy.random.random()*(var[index][1]*new_list[-1] - var[index][0]*new_list[-1]) + var[index][1]*new_list[-1]
				new_list.append(rd_num)


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

	def scoring_data (self):
		df = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/scoring.csv')
		df = df.set_index('indicateur')
		range_env = [43,72]
		range_soc = [45,55]
		rang_gouv = [55,100]
		
		for index, a_range in zip(df.index, [range_env, range_soc, rang_gouv]):
			df.loc[index, 'value'] = numpy.random.randint(a_range[0], a_range[1])
		#print(df)

		full_path = os.path.normcase(f'{self.current}/scoring.json')
		print('Saved Scoring Data')
		df.to_json(full_path, orient='table', indent=4)

	def main(self):
		self.data_agri()
		self.financial_data()
		self.gauges_val()
		self.graph_val()
		self.indic_critique()
		self.stat_data()
		self.scoring_data()
		print('data_generated')
