"""
© GRID Team, 2021
"""

import pandas
import plotly
import plotly.graph_objs as go

import pandas
import numpy
import json
from agri_data import data_import

class Scoring:
    """Cette classe donne les données nécessaires au rendu des gauges indiquant les scores ESG 
    """
    def __init__ (self):
      self.data = data_import.ReadData('scoring').read_json()
        
    
    def bin (self):
      """Génère les intervalles autour de la valeur moyenne
      """
      self.data['min'] = 0.0
      self.data['low_avg'] = 0.9*self.data['average']
      self.data['high_avg'] = 1.1*self.data['average']
    
    def main (self):
      """
        :return: liste de listes (une par indicateur) contenant pour chaque: sa valeur, la valeur max de l'echelle, une liste avec les intervalles de couleurs
        :rtype: list
        """
      self.bin()
      list_output = []
      for indic in self.data.index:
        indic_val = [self.data.loc[indic, 'value']]
        indic_val.append(self.data.loc[indic, 'max'])
        indic_val.append([self.data.loc[indic, 'min'], self.data.loc[indic, 'low_avg'], self.data.loc[indic, 'high_avg'], float(self.data.loc[indic, 'max'])])
        list_output.append(indic_val)
    
      return list_output

class CriticalAlert:
    """Cette classe donne las liste des indicateurs considérés comme critique.
    """
    def __init__(self):
      self.data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/liste_indic.csv')
      self.data = self.data.set_index('Code input')
    
    def main(self):
      """
        :return: liste de listes (une par indicateur) contenant pour chaque la liste des indicateurs critiques
        :rtype: list
        """
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



  