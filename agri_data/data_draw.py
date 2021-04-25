"""
© GRID Team, 2021
"""

import pandas
import numpy
import os

class RandomDraw:
	"""Cette classe télécharge les données de GitHub et les stocke en locale. Pour certains jeux de données, ils sont modifiés par un tri 
	alétoire à chaque login
    """

	def __init__(self):
		self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))

	def data_agri (self):
		"""Télécharge et enrehistre les données liées à l'emplacement de l'agriculteur
        """
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/data_agri.json', orient='table')

		full_path = os.path.normcase(f'{self.current}/data_agri.json')
		print('Saved Data Agri')
		df.to_json(full_path, orient='table', indent=4)

	def financial_data (self):
		"""Télécharge et enrehistre les données liées aux données financières
		Elles sont randomisées avant l'enregistrement
        """
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/financial_data.json', orient='table')
		v0 = {'F1':1000, 'F2':1.2}
		var = {'F1': [0.95, 1.1], 'F2': [0.90, 1.1]}

		for index in df.index :
			new_list = [numpy.random.random()*(var[index][1]*v0[index] - var[index][0]*v0[index]) + var[index][1]*v0[index]]
			for k in range(len(df.loc[index, 'list_x'])-1):
				rd_num = numpy.random.random()*(var[index][1]*new_list[-1] - var[index][0]*new_list[-1]) + var[index][1]*new_list[-1]
				new_list.append(rd_num)

			df.loc[index,'list_y'] = new_list

		print(df)


		full_path = os.path.normcase(f'{self.current}/financial_data.json')
		print('Saved Financial Data')
		df.to_json(full_path, orient='table', indent=4)

	def gauges_val (self):
		"""Télécharge et enregistre les données pour générer échelles de couleurs
        """
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/gauges_val.json', orient='table')
		
		full_path = os.path.normcase(f'{self.current}/gauges_data.json')
		print('Saved Gauges Val')
		df.to_json(full_path, orient='table', indent=4)

	def graph_val (self):
		"""Télécharge et enregistre les données pour générer les graphs
        """
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/graph_val.json', orient='table')
		
		full_path = os.path.normcase(f'{self.current}/graph_data.json')
		print('Saved Graph Val')
		df.to_json(full_path, orient='table', indent=4)

	def indic_critique (self):
		"""Télécharge et enregistre les données donnant les indices critiques
        """
		df = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/liste_indic.csv')

		full_path = os.path.normcase(f'{self.current}/indic_data.json')
		print('Saved Index Critique')
		df.to_json(full_path, orient='table', indent=4)

	def stat_data (self):
		"""Télécharge et enregistre les données donnant les statiques liés à la région
        """
		df = pandas.read_json('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/stat.json', orient='table')
		
		full_path = os.path.normcase(f'{self.current}/stat_data.json')
		print('Saved Stat data')
		df.to_json(full_path, orient='table', indent=4)

	def scoring_data (self):
		"""Télécharge et enregistre les données de scoring ESG.
		Elles sont randomisées avant l'enregistrement
        """
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
