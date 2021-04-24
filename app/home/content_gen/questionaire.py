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



