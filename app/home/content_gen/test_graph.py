import plotly
import plotly.graph_objs as go

import pandas
import numpy
import json


def plot_co2():
    data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/sample_data/main/sample_data/co2_sample.csv')
    data.loc[:,'date'] = pandas.to_datetime(data.loc[:,'date'])
    data = [go.Scatter(x=data.loc[:,'date'], y=data.loc[:,'co2'])]
    layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                       xaxis_title='Date' , yaxis_title='Emission de CO2', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                       )
    fig = go.Figure(data=data, layout=layout)
    
    graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphjson



def plot_pct():
    data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/sample_data/main/sample_data/pctge_sample.csv')
    data.loc[:,'date'] = pandas.to_datetime(data.loc[:,'date'])
    data = [go.Scatter(x=data.loc[:,'date'], y=data.loc[:,'pct'])]
    layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                       xaxis_title='Date' , yaxis_title='% femmes', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                       )
    fig = go.Figure(data=data, layout=layout)
    graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphjson

def plot_alerte():
    data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/sample_data/main/sample_data/alerte_sample.csv')
    data.loc[:,'date'] = pandas.to_datetime(data.loc[:,'date'])
    data = [go.Scatter(x=data.loc[:,'date'], y=data.loc[:,'alerte'])]
    layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                       xaxis_title='Date' , yaxis_title='Alertes environmentales', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                       )
    fig = go.Figure(data=data, layout=layout)
    graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphjson

def plot_ebitda():
    data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/sample_data/main/sample_data/ebitda_sample.csv')
    data.loc[:,'date'] = pandas.to_datetime(data.loc[:,'date'])
    data = [go.Bar(x=data.loc[:,'date'], y=data.loc[:,'alerte'])]
    layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                       xaxis_title='Date' , yaxis_title='EBITDA', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                       )
    fig = go.Figure(data=data, layout=layout)
    graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphjson


def prepare_data_plot ():
    df = pandas.read_csv('https://www.data.gouv.fr/fr/datasets/r/b273cf3b-e9de-437c-af55-eda5979e92fc', sep=';')
    df.loc[:,'jour'] = pandas.to_datetime(df.loc[:,'jour'], format='%Y-%m-%d')
    df = df.groupby('jour').sum()

    return df

def get_plot ():
    df = prepare_data_plot()
    data = [go.Scatter(x=df.index, y=df.loc[:,'n_cum_dose1'], name='Dose 1'),
                go.Scatter(x=df.index, y=df.loc[:,'n_cum_dose2'], name='Dose 2')]
    layout = go.Layout( paper_bgcolor='rgba(61,61,51,0.3)', plot_bgcolor='rgba(0,0,0,0)',
    					xaxis_title='Date' , yaxis_title='Nombre doses', font=dict(color='#5cba47'),
    					title=go.layout.Title(text="Nombre de personnes vaccinées en France"))

    fig = go.Figure(data=data, layout=layout)
    graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphjson

def data_graph():
	total_confirmed=pandas.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',encoding='utf-8',na_values=None)
	total_confirmed.replace(to_replace='US', value='United States', regex=True, inplace=True)
	total_death=pandas.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',encoding='utf-8',na_values=None)
	total_death.replace(to_replace='US', value='United States', regex=True, inplace=True)
	total_recovered=pandas.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',encoding='utf-8',na_values=None)
	total_recovered.replace(to_replace='US', value='United States', regex=True, inplace=True)

	grouped_total_confirmed = total_confirmed[["Country/Region",total_confirmed.columns[-1]]].groupby("Country/Region").sum().sort_values(by=total_confirmed.columns[-1], ascending=False)
	grouped_total_confirmed.reset_index(inplace=True)
	grouped_total_confirmed.columns=["Country/Region", 'confirmed']
	grouped_total_confirmed.replace(to_replace='US', value='United States', regex=True, inplace=True)
	grouped_total_confirmed

	df_pop = pandas.read_json('https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json')
	df_pop.columns=['Country/Region','population']
	df_pop=df_pop.replace(to_replace='Russian Federation', value='Russia')

	url = "https://gist.githubusercontent.com/komasaru/9303029/raw/9ea6e5900715afec6ce4ff79a0c4102b09180ddd/iso_3166_1.csv"
	country_code = pandas.read_csv(url)
	country_code = country_code[["English short name","Alpha-3 code","Numeric"]]
	country_code.columns=["Country/Region", "code3", "id"]

	country_code=country_code.replace(to_replace='Russian Federation (the)', value='Russia')
	country_code=country_code.replace(to_replace='United Kingdom (the)', value='United Kingdom')
	country_code=country_code.replace(to_replace='United States (the)', value='United States')
	country_code=country_code.replace(to_replace='Viet Nam', value='Vietnam')
	country_code

	final_df=pandas.merge(grouped_total_confirmed,df_pop,how='inner',on='Country/Region')
	final_df=pandas.merge(country_code,final_df,how='inner',on='Country/Region')
	final_df = final_df.sort_values(by="confirmed", ascending=False)
	final_df.reset_index(inplace=True, drop=True)
	final_df.to_json("new_map.json")
	final_df['cases/million'] = ((final_df['confirmed']/final_df['population'])*1000000).round(2)

	return final_df

def plot_map():
	df = data_graph()
	fig = go.Figure(data=go.Choropleth(
	    locations = df['code3'],
	    z = df['cases/million'],
	    text = df['Country/Region'],
	    colorscale = 'Darkmint',
	    autocolorscale=False,
	    reversescale=False,
	    marker_line_color='darkgray',
	    marker_line_width=0.5,
	    colorbar_tickprefix = '',
	    colorbar_title = '#cases <br>per million populations',
	))

	fig.update_layout( title_text='Covid 19 confirmed cases',
	    	geo=dict(
	        showframe=False,
	        showcoastlines=False,
	        projection_type='equirectangular'
	    ),
	    annotations = [dict(
	        x=0.55,
	        y=0.1,
	        xref='paper',
	        yref='paper',
	        text='Source: <a href="https://github.com/CSSEGISandData/COVID-19">\
	            CSSE at Johns Hopkins University</a>',
	        showarrow = False
	    )],paper_bgcolor='rgba(61,61,51,0.3)', plot_bgcolor='rgba(0,0,0,0)',
    					font=dict(color='#5cba47'),
	)

	plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

	return plot_json

def ana_viti():
    name = 'viti_france.csv'
    list_features_map = ["Chiffre d'affaires", "TOTAL DE L'ACTIF"]
    gen_features = ["Nom de l'entreprise", "Code postal", "Dernière année disponible", "Nom de la banque"]
    pnl_features = ["Chiffre d'affaires", "Chiffre d'affaires net (H.T.)", "Valeur ajoutée", "Excédent brut d'exploitation", "Résultat de l'exercice"]
    bs_features = ["Total capitaux propres", "Capital social ou individuel", "TOTAL DE L'ACTIF"]
    loans_features = ["Empr. obligataires convertibles", "Autres emprunts obligataires", "Empr. & dettes auprès ét. créd.", "Empr. et dettes fin. divers"]
    debt_features = ["Dettes fourn. et cptes ratt.", "Dettes fiscales et sociales", "Dettes sur immob. & cptes ratt.", "Autres dettes"]

    VitiAna = VAS.DataAnalysis(name, pnl_features, bs_features, loans_features, debt_features, list_features_map)
    bank, exploit, bs, pnl = VitiAna.main()
    
    return bank, exploit, bs, pnl