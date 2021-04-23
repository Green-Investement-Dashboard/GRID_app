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
import numpy

class CaniculePlot:
    def __init__ (self):
         self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
         self.file_name='data/full_data_heatwave.json'
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
                                           zmin=0, zmax=temp_df['HWD_EU_climate'].max(),
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
    def main(self):
        self.read_json()
        plot_json = self.plot2()
        return plot_json


class FirePlot:
    def __init__ (self):
         self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
         self.file_name=f'data/full_data_fire.json'
         self.full_path = os.path.normcase(f'{self.current}/{self.file_name}')
         
         
    def read_json (self):
         self.df = pandas.read_json(self.full_path, orient='table')
         self.df = self.df.set_index(['lat','lon', 'time'])
         self.df = self.df.sort_index()
         
         print(self.df)
         
    def color_scale (self, value):
         colorscale=[[0.00, 'rgb(148, 201, 255)'],#[5.20, '#94C9FF'],
                     [5.20, 'rgb(148, 143, 25'')'],#[11.2, '#948FFE'],
                     [11.2, 'rgb(204, 139, 250)'],#[21.3, '#CC8BFA'],
                     [21.3, 'rgb(246, 135, 233)'],#[38.0, '#F687E9'],
                     [38.0, 'rgb(242, 131, 169)'],#[50.0, '#F283A9'],
                     [50.0, 'rgb(13, 149, 128)'],#[60.0, "#ED9580"],
                     ]
         for k in range(len(colorscale)-1):
             if value >= colorscale[k][0] and value <colorscale[k+1][0]:
                 return colorscale[k][1]
         
         #colorscale=[[0, 'green'], [0.5, 'red'], [1.0, 'rgb(0, 0, 255)']]
         return colorscale[k+1][1]
     
    def color_scale_2(self, zmax):
        colorscale=[[0.00, '#FF6474'],
                     [5.20, '#FD6D68'],
                     [11.2, '#F9856C'],
                     [21.3, '#F59A70'],
                     [38.0, '#F0AD75'],
                     [50.0, "#ECBD79"],
                     [zmax, "#E8CB7D"],
                     ]
        all_values = [0.00, 5.20, 11.2, 21.3, 38.0, 50.0]
        tick_val = []
        val_min = colorscale[0][0]
        val_max = colorscale[-1][0]
        Delta = val_max - val_min
        
        colorscheme = []
        
        current_val = 0
        for k in range(len(colorscale)-1):
            delta = colorscale[k+1][0] - colorscale[k][0]
            step = delta/Delta
            tick_val.append(colorscale[k][0])
            tick_val.append((colorscale[k+1][0] - colorscale[k][0])/2.0+colorscale[k][0] )
            for a_val in numpy.linspace(current_val, current_val+step, num=10, endpoint=False):
                colorscheme.append([a_val, colorscale[k][1]])
            a_val = 0.99*(colorscale[k+1][0]/val_max)
            colorscheme.append([a_val, colorscale[k][1]])
            
            current_val = colorscale[k+1][0]/val_max
            
        colorscheme.append([1.0, colorscale[k][1]])
        tick_val.append(int(colorscale[k+1][0]))
        print(colorscheme)

        return colorscheme, tick_val
            
         
         
    def plot (self):
        date = pandas.to_datetime('2097-11-01')
        self.df = self.df.loc[(slice(None), slice(None), date),:]
        self.df = self.df.reset_index()
        data = go.Densitymapbox(lat=self.df['lat'], lon=self.df['lon'], 
                                         z=self.df['fwi-mean-jjas'], radius=10)
    
        layout = go.Layout(mapbox_style="open-street-map",
                           mapbox=dict(bearing=0,center=dict(lat=43.58, lon=4.04),pitch=0, zoom=4),
                           paper_bgcolor='rgba(61,61,51,0.3)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           height=650
                           )
        fig=go.Figure(data=data, layout=layout)
        fig.write_html("fire.html")
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return plot_json
    
    def plot2 (self):
        #self.df = self.df.reset_index()
        data_slider = []
        fig = go.Figure()
        beg_date = pandas.to_datetime("2021-11-01")
        end_date = pandas.to_datetime("2080-11-01")
        #list_date=pandas.date_range(start=beg_date, end=end_date, freq="Y")
        list_date = ["2021-11-01", "2031-11-01", "2041-11-01", "2051-11-01", "2061-11-01", "2081-11-01"]
        list_date = [pandas.to_datetime(k) for k in list_date]
        partial_df = self.df.loc[(slice(None), slice(None), list_date),:]
        #partial_df['color'] = "#ffffff"
        partial_df['color'] = partial_df.apply(lambda x: self.color_scale(x['fwi-mean-jjas']), axis=1)
        #print(partial_df)
        zmax = partial_df['fwi-mean-jjas'].max()
        colorscheme, tick_val = self.color_scale_2(zmax)
        
                                      
        
        #partial_df = self.df.loc[(slice(None), slice(None), slice(beg_date,end_date)),:]
        #list_date = partial_df.index.get_level_values('time').unique()
        
        for date in tqdm.tqdm(list_date):
            temp_df = partial_df.loc[(slice(None), slice(None), date),:].reset_index()
            temp_df['int_days'] = temp_df.apply(lambda x: round(x['fwi-mean-jjas'],2), axis=1)
            temp_df['year'] = temp_df.apply(lambda x: x['time'].strftime('%Y'), axis=1)
            """
            fig.add_trace(go.Densitymapbox(lat=temp_df['lat'], lon=temp_df['lon'], 
                                           z=temp_df['fwi-mean-jjas'], radius=10,
                                           colorbar= {'title':'Index feu'},
                                           zmin=0, zmax=zmax,
                                           colorscale = colorscheme,
                                           customdata = temp_df[['int_days', 'year']],
                                           hovertemplate = '<b>%{customdata[0]}</b> index feu<br>' + "%{customdata[1]} <extra></extra>"
                                           )
                          )
            """
            fig.add_trace(go.Scattermapbox(lat=temp_df['lat'], lon=temp_df['lon'], 
                                           #fill = "toself",
                                           #fillcolor=temp_df['color'], 
                                           marker = dict(color=temp_df['fwi-mean-jjas'],
                                                         size=20,
                                                         colorscale = colorscheme,
                                                         colorbar= {'title':'Probabilité de feu',
                                                                    'tickvals':tick_val,
                                                                    'ticktext':[0, "<b>Très bas</b>", 5.2, "<b>Bas</b>", 11.2, "<b>Modéré</b>", 21.3, "<b>Haut</b>", 38.0, "<b>Très haut</b>", 50.0, "<b>Extrême</b>"],
                                                                    'ticks':"outside"
                                                                    },
                                                         cmin=0, cmax=zmax, opacity=1
                                                         ),
                                           #radius=10,
                                           #colorbar= {'title':'Index feu'},
                                           #zmin=0, zmax=zmax,
                                           #colorscale='aggrnyl',
                                           customdata = temp_df[['int_days', 'year']],
                                           hovertemplate = '<b>%{customdata[0]}</b> index feu<br>' + "%{customdata[1]} <extra></extra>"
                                           )
                          )
        fig.add_trace(go.Scattermapbox(lat=[43.58], lon=[4.04], marker = {'size': 30, 'color':["#0D9580"]},
                                       hovertemplate = "<b>Exploitation</b> <extra></extra>"))
            
        steps = []
        for i, date in zip(range(len(fig.data)-1), list_date):
            step = dict(method='update',
                        args=[{"visible": [False] * (len(fig.data)-1) + [True]},
                              {"title": f"Carte des canicules {date.strftime('%Y')}"}],
                        label=f"Year: {date.strftime('%Y')}",
                        )
            step["args"][0]["visible"][i] = True
            steps.append(step)
            
        sliders = [dict(active=0, pad={"t": 1}, steps=steps)]  
            
    
        fig.update_layout(mapbox_style="open-street-map",
                           mapbox=dict(bearing=0,center=dict(lat=43.58, lon=4.04),pitch=0, zoom=6),
                           paper_bgcolor='rgba(61,61,51,0.3)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           height=650, sliders=sliders, showlegend=False
                           )
        #fig=go.Figure(data=data_slider, layout=layout)
        fig.write_html("fire.html")
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return plot_json
    
    def main(self):
        self.read_json()
        plot_json = self.plot2()
        return plot_json
        
         
         
         
if __name__ == '__main__':
    canicule = FirePlot().main()
    