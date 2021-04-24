# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from flask import jsonify, render_template, redirect, request, url_for, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template, flash, redirect

from os import environ
from sys import exit
from decouple import config
import logging

from config import config_dict
from app import create_app, db

import plotly
import plotly.graph_objs as go

import pandas
import numpy
import json

from agri_data import data_draw

from app.home.content_gen import index_renderer
from app.home.content_gen import map_generation as mgen
from app.home.content_gen import graph_generation as ggen
from app.home.content_gen import questionaire

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)
data_draw.RandomDraw().main()

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
	#ggen.PlotCanicule().find_closest()
	plot_canicule = ggen.CaniculePlot().main()
	plot_fire = mgen.FirePlot().main()
	
	critical_alert = index_renderer.CriticalAlert().main()

	return render_template('environnement.html', canicule_map=plot_canicule, plot_fire = plot_fire, critical_alert = critical_alert)

@app.route('/gouv')
def gouv():
	critical_alert = index_renderer.CriticalAlert().main()
	G6_indic = ggen.PieChart('G6', "Diversification d'activité").plot()
	G9_indic = ggen.BulletChart('G9', "Matériel mutualisé").plot()

	return render_template('gouvernance.html', G6_indic=G6_indic, G9_indic=G9_indic, critical_alert = critical_alert)

@app.route('/soc')
def soc():
	S1_indic = ggen.BulletChart('S1', "Communication").plot()
	S2_indic = ggen.BulletChart('S2', "Barrières douanières").plot()
	S3_indic = ggen.PieChart('G6', "Diversification d'activité").plot() 
	critical_alert = index_renderer.CriticalAlert().main()

	return render_template('social.html', bullet_charts = [S1_indic, S2_indic], S3_indic = S3_indic,
		critical_alert = critical_alert)
	

@app.route('/index')
def index():
	scoring = index_renderer.Scoring().main()
	critical_alert = index_renderer.CriticalAlert().main()

	list_graph = ggen.FinancialChart('F1', 'F2').plot_bar()
	#ebitda, endet = gen_graph.FinancialChart('F1', 'F2').plot_sgl_line()
	ebitda_endet = ggen.FinancialChart('F1', 'F2').plot_mltpl_line()

	return render_template('index.html', ebitda=list_graph[0], endet=list_graph[1], ebitda_endet = ebitda_endet, scoring=scoring, critical_alert = critical_alert)

@app.route('/questionnaire', methods=['GET', 'POST'])
def set_up_q():
	form = questionaire.QuestionairesAgri(request.form)

	if form.validate_on_submit():
		data = request.form
		result= questionaire.save_data(data)
		return render_template('questionaire.html',  end=True, message= 'Merci {}, données enregistrées'.format(form.name_exploit.data), table = result)	

	return render_template('questionaire.html',  end=False, form=form)



if __name__ == "__main__":
	data_draw.RandomDraw.main()
	app.run()
