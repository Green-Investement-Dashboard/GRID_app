#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 16:02:54 2021

@author: Clement
"""
import pandas
import os
import numpy
import geopandas
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import tqdm
import json
import plotly.graph_objects as go
import plotly

class DataImport:
    def __init__ (self, dpt, town, list_db):
        self.dpt = dpt 
        self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
        self.town = town
        self.list_db = list_db
        
    def create_folder (self, directory):
        if os.path.exists(os.path.normcase(directory)) == False:
            os.makedirs(directory)
            print(f'Directory created: {directory}')
                
        return directory
        
    def import_data (self):
        data_location = f'{self.current}/data/tri_2020_sig_di_{self.dpt}/FRD_TRI_{self.town.upper()}'
        self.list_df = []
        for db in tqdm.tqdm(self.list_db):
            file = f'{db[0]}{self.town}{db[1]}{str(self.dpt).zfill(3)}{db[2]}'
            import_path = os.path.normcase(f'{data_location}/{file}')
            importing_df = geopandas.read_file(import_path)
            importing_df = importing_df.set_index('uuid')
            importing_df = importing_df.to_crs(epsg=4326)
            self.list_df.append(importing_df)
        #self.quick_plot ()
            
        return self.list_df
    
    def to_json (self):
        data_location = f'{self.current}/data/innondations/{self.town}'
        data_location = self.create_folder (data_location)
        
        for db, df in tqdm.tqdm(zip(self.list_db, self.list_df), total=len(self.list_df)):
            file = f'{db[0]}{self.town}{db[1]}{str(self.dpt).zfill(3)}.geojson'
            full_path = os.path.normcase(f'{data_location}/{file}')
            df.to_file (full_path, driver="GeoJSON")
        
    def read_json(self):
        self.list_json = []
        
        data_location = f'{self.current}/data/innondations/{self.town}'
        for db in tqdm.tqdm(self.list_db):
            file = f'{db[0]}{self.town}{db[1]}{str(self.dpt).zfill(3)}.geojson'
            full_path = os.path.normcase(f'{data_location}/{file}')
            
            with open(full_path) as geofile:
                j_file = json.load(geofile)
                self.list_json.append(j_file)
                
        return self.list_json
            
    
    def quick_plot (self):
        pdf = matplotlib.backends.backend_pdf.PdfPages(os.path.normcase('quick_view.pdf'))
        
        for db, df in tqdm.tqdm(zip(self.list_db, self.list_df), total=len(self.list_df)):
            fig, ax = plt.subplots(1, 1,num = str(db[1]), figsize=(11,7))
            fig.suptitle(str(db[1]))
            df.plot(ax=ax, column='typ_inond')
            pdf.savefig(fig, dpi=200)
            plt.close(fig)
        pdf.close()
        return df
class InternalPlot:
    def __init__ (self, geo_df):
        self.geo_df = geo_df
        
    def plot(self):
        print(self.geo_df.drop(columns=['geometry']))
        json_file = self.geo_df.__geo_interface__
        data = go.Choroplethmapbox(geojson = json_file,             #this is your GeoJSON
                                   locations = self.geo_df.index,    #the index of this dataframe should align with the 'id' element in your geojson
                                   z = self.geo_df['typ_inond'], #sets the color value
                                   )
        layout = go.Layout(mapbox_style="open-street-map",
                           mapbox=dict(bearing=0,center=dict(lat=43.58, lon=4.04),pitch=0, zoom=9),
                           paper_bgcolor='rgba(61,61,51,0.3)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           height=650
                           )
        fig=go.Figure(data=data, layout=layout)
        fig.write_html("innondations.html")
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return plot_json
        
            
        
    
    
dpt = 30
town = 'nimes'
list_db = [['n_tri_', '_carte_inond_s_', '.shp'], #cartes de surfaces inondables produites sur un TRI donné
           ['n_tri_', '_carte_risq_s_', '.shp'], #cartes de risque d’inondation produites sur un TRI donné
           ['n_tri_', '_tri_s_', '.shp'], #emprise et les caractéristiques utiles du territoire à risque d’inondation
           
           ['n_tri_', '_inondable_01_01for_s_', '.shp'], #surfaces inondables _[alea]_[scenario]_[cours d'eau]_s_.shp
           ['n_tri_', '_inondable_01_02moy_s_', '.shp'],
           ['n_tri_', '_inondable_01_04fai_s_', '.shp'],
           ['n_tri_', '_inondable_03_01for_s_', '.shp'],
           ['n_tri_', '_inondable_03_02moy_s_', '.shp'],
           ['n_tri_', '_inondable_03_03mcc_s_', '.shp'],
           ['n_tri_', '_inondable_03_04fai_s_', '.shp'],
           
           ['n_tri_', '_iso_ht_01_01for_s_', '.shp'], #aléa d’un certain type selon un certain scénario provoque une montée d’eau dont la hauteur se situe dans une plage de valeurs fixe.
           ['n_tri_', '_iso_ht_01_02moy_s_', '.shp'],
           ['n_tri_', '_iso_ht_01_04fai_s_', '.shp'],
           ['n_tri_', '_iso_ht_03_01for_s_', '.shp'],
           ['n_tri_', '_iso_ht_03_02moy_s_', '.shp'],
           ['n_tri_', '_iso_ht_03_03mcc_s_', '.shp'],
           ['n_tri_', '_iso_ht_03_04fai_s_', '.shp'],
           
           ['n_tri_', '_enjeu_dce_s_', '.shp'], #enjeux liés à des zones protégées au titre de la DCE
           ['n_tri_', '_enjeu_steu_p_', '.shp'], #enjeux liés aux stations de traitement des eaux usées
           ['n_tri_', '_enjeu_ippc_p_', '.shp'], #enjeux liés aux installations polluantes de la directive IPPC
           
           ['n_tri_', '_enjeu_crise_p_', '.shp'], #enjeux correspondant aux établissements, infrastructures et installations sensibles
           ['n_tri_', '_enjeu_crise_l_', '.shp'], 
           
           ['n_tri_', '_enjeu_eco_s_', '.shp'], #zones homogènes décrivant un type d’activités économiques se situant sur un TRI
           
           ['n_tri_', '_enjeu_patrim_s_', '.shp'], #enjeux liés au patrimoine culturel
           ['n_tri_', '_enjeu_patrim_p_', '.shp'],
           
           ['n_tri_', '_ouv_protec_l_', '.shp'], #ouvrages de protection œuvrant contre les inondations dans l’emprise du TRI
           
           ['n_tri_', '_commune_s_', '.shp'], #communes ayant servi à calculer les enjeux de nombres d'habitants et d'emplois pour chaque scénario d’inondation
           ] 

list_db =[['n_tri_', '_carte_inond_s_', '.shp'], #cartes de surfaces inondables produites sur un TRI donné
           ['n_tri_', '_carte_risq_s_', '.shp'], #cartes de risque d’inondation produites sur un TRI donné
           ['n_tri_', '_tri_s_', '.shp'], #emprise et les caractéristiques utiles du territoire à risque d’inondation
           
           ['n_tri_', '_inondable_01_01for_s_', '.shp'], #surfaces inondables _[alea]_[scenario]_[cours d'eau]_s_.shp
           ['n_tri_', '_inondable_01_02moy_s_', '.shp'],
           ['n_tri_', '_inondable_01_04fai_s_', '.shp'],
           ['n_tri_', '_inondable_03_01for_s_', '.shp'],
           ['n_tri_', '_inondable_03_02moy_s_', '.shp'],
           ['n_tri_', '_inondable_03_03mcc_s_', '.shp'],
           ['n_tri_', '_inondable_03_04fai_s_', '.shp'],
           ] 
           
list_db2 =[
           ['n_tri_', '_inondable_03_04fai_s_', '.shp'],
           ]            

def main (list_db, dpt, town):
    Innondations = DataImport(dpt, town, list_db2)
    list_df = Innondations.import_data()
    df = Innondations.quick_plot()
    print(list_df[0].loc[:,'geometry'])
    plot_json = InternalPlot(list_df[0]).plot()

    return plot_json

def read_json (list_db, dpt, town):
    Innondations = DataImport(dpt, town, list_db)
    list_json = Innondations.read_json()
    
    return list_json
    
           
if __name__ == '__main__':
    Innondations = DataImport(dpt, town, list_db2)
    list_df = Innondations.import_data()
    df = Innondations.quick_plot()
    print(list_df[0].loc[:,'geometry'])
    InternalPlot(list_df[0]).plot()




