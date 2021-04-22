# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from flask import jsonify, render_template, redirect, request, url_for, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app.base.forms import Questionaires
from flask import render_template, flash, redirect

from os import environ
from sys import exit
from decouple import config
import logging

from config import config_dict
from app import create_app, db
import app.base.index_renderer as index_renderer
#%%
import plotly
import plotly.graph_objs as go

import pandas
import numpy
import json

from app.home.content_gen import index_renderer
from app.home.content_gen import test_graph
from app.home.content_gen import canicule
from app.home.content_gen import bullet_chart_gen

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config ) 

Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )


@app.route('/env')
def env():
	canicule_instance = canicule.CaniculePlot('HWD', '85')
	canicule_instance.read_json()
	plot_canicule = canicule_instance.plot2()
	critical_alert = index_renderer.CriticalAlert().main()

	return render_template('environement.html', canicule_map=plot_canicule, critical_alert = critical_alert)

@app.route('/gouv')
def gouv():
	critical_alert = index_renderer.CriticalAlert().main()

	return render_template('gouvernance.html', critical_alert = critical_alert)

@app.route('/soc')
def soc():
	S1_indic = bullet_chart_gen.BulletChart('S1', 'Test').plot()
	critical_alert = index_renderer.CriticalAlert().main()

	return render_template('social.html', s1=S1_indic, critical_alert = critical_alert)
	

@app.route('/index')
def index():
	ebitda = index_renderer.Plots().plot_ebitda()
	scoring = index_renderer.Scoring().main()
	critical_alert = index_renderer.CriticalAlert().main()
	print(scoring)

	return render_template('index.html', ebitda=ebitda, scoring=scoring, critical_alert = critical_alert)

@app.route('/questionnaire', methods=['GET', 'POST'])
def set_up_q():
	form = Questionaires(request.form)

	if form.validate_on_submit():
		data = request.form
		print(data)
		save_data(data)
		return render_template('questionaire.html',  end=True, message= 'Merci {}, données enregistrées'.format(form.name_exploit.data))

	return render_template('questionaire.html',  end=False, form=form)

def save_data (data):
	df = pandas.read_json('data_agri.json', orient='table')
	name_exploit = data['name_exploit']

	for keys in data.keys():
		if keys not in ['csrf_token', 'name_exploit']:
			df.loc[name_exploit, keys] = data[keys]

	df.to_json('data_agri.json', orient='table', indent=4)


if __name__ == "__main__":
    app.run()
    
#Bonjour la GRID TEAM 