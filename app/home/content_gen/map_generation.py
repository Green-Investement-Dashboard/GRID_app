#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:29:01 2021

@author: Clement
"""
import pandas
import os
import json
import plotly.graph_objects as go
import plotly
import tqdm

class CaniculePlot:
    def __init__ (self, data, rcp):
         self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
         self.file_name=f'data/{data}_EU_climate_rcp{rcp}_mean_v1.json'
         self.full_path = os.path.normcase(f'{self.current}/{self.file_name}')
         
    def read_json (self):
         self.df = pandas.read_json(self.full_path, orient='table')
         

         print(self.df)
         
    def plot (self):
        date = pandas.to_datetime('2035-01-01')
        self.df = self.df.loc[(slice(None), slice(None), date),:]
        self.df = self.df.reset_index()
        data = go.Densitymapbox(lat=self.df['lat'], lon=self.df['lon'], 
                                         z=self.df['HWD_EU_climate'], radius=10)
    
        layout = go.Layout(mapbox_style="open-street-map",
                           mapbox=dict(bearing=0,center=dict(lat=43.58, lon=4.04),pitch=0, zoom=4),
                           paper_bgcolor='rgba(61,61,51,0.3)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           height=650
                           )
        fig=go.Figure(data=data, layout=layout)
        #fig.write_html("cannicule.html")
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return plot_json
    
    def plot2 (self):
        #self.df = self.df.reset_index()
        data_slider = []
        fig = go.Figure()
        beg_date = pandas.to_datetime("2021-01-01")
        end_date = pandas.to_datetime("2081-01-01")
        #list_date=pandas.date_range(start=beg_date, end=end_date, freq="Y")
        list_date = ["2021-01-01", "2031-01-01", "2041-01-01", "2051-01-01", "2061-01-01", "2081-01-01"]
        list_date = [pandas.to_datetime(k) for k in list_date]
        
        
        for date in tqdm.tqdm(list_date):
            temp_df = self.df.loc[(slice(None), slice(None), date),:].reset_index()
            temp_df['int_days'] = temp_df.apply(lambda x: int(x['HWD_EU_climate']), axis=1)
            temp_df['year'] = temp_df.apply(lambda x: x['time'].strftime('%Y'), axis=1)
            fig.add_trace(go.Densitymapbox(lat=temp_df['lat'], lon=temp_df['lon'], 
                                           z=temp_df['HWD_EU_climate'], radius=10,
                                           colorbar= {'title':'Nb de jours'},
                                           zmin=0, zmax=self.df['HWD_EU_climate'].max(),
                                           customdata = temp_df[['int_days', 'year']],
                                           hovertemplate = '<b>%{customdata[0]}</b> jours<br>' + "%{customdata[1]} <extra></extra>"
                                           )
                          )
        
        steps = []
        for i, date in zip(range(len(fig.data)), list_date):
            step = dict(method='update',
                        args=[{"visible": [False] * len(fig.data)},
                              {"title": f"Carte des canicules {date.strftime('%Y')}"}],
                        label=f"Year: {date.strftime('%Y')}"
                        )
            step["args"][0]["visible"][i] = True
            steps.append(step)
            
        sliders = [dict(active=0, pad={"t": 1}, steps=steps)]  
            
    
        fig.update_layout(mapbox_style="open-street-map",
                           mapbox=dict(bearing=0,center=dict(lat=43.58, lon=4.04),pitch=0, zoom=6),
                           paper_bgcolor='rgba(61,61,51,0.3)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           height=650, sliders=sliders
                           )
        #fig=go.Figure(data=data_slider, layout=layout)
        #fig.write_html("cannicule.html")
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return plot_json
        
         
         
         
if __name__ == '__main__':
    canicule = CaniculePlot('HWD', '85')
    canicule.read_json()
    canicule.plot2()
    