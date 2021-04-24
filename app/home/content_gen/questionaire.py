# -*- encoding: utf-8 -*-
from flask_wtf import FlaskForm, RecaptchaField
import wtforms
from wtforms.validators import InputRequired, Email, DataRequired
import pandas

class QuestionairesAgri(FlaskForm):
	name_exploit = wtforms.TextField('Nom exploitation', validators=[DataRequired()])
	address   = wtforms.TextField('Address', validators=[DataRequired()])
	age = wtforms.TextField('Age', validators=[DataRequired()])
	date = wtforms.DateField('Date')
	language = wtforms.SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
	text = wtforms.TextAreaField('Text multi ligne')
	selection = wtforms.RadioField(choices=[('ch1', 'Choix 1'), ('ch1', 'Choix 2'), ('ch1', 'Choix 3')]) #1ere valeur du tuple: ce qui s'affichera dans la DB et 2eme: ce qui s'affiche dans l'HTML
	multiple = wtforms.SelectMultipleField(choices=[('Elo 1','Bjr Elo 1'), ('Elo 2', 'Bjr Elo 2'), ('Elo 3', 'Bjr Elo 3')])
	#recaptcha = RecaptchaField()
	submit = wtforms.SubmitField('Enregistrer')


def save_data(data):
	df = pandas.read_json('data_agri.json', orient='table')
	name_exploit = data['name_exploit']

	for keys in data.keys():
		if keys not in ['csrf_token', 'name_exploit']:
			df.loc[name_exploit, keys] = data[keys]
	df = df.drop(columns=['submit'])
	df.to_json('data_agri.json', orient='table', indent=4)
	print(df.loc[[name_exploit]])

	return df.loc[[name_exploit]].T.to_html(classes='table tablesorter', header="true")



