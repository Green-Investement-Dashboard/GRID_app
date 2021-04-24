# -*- encoding: utf-8 -*-
from flask_wtf import FlaskForm, RecaptchaField
import wtforms
from wtforms.validators import InputRequired, Email, DataRequired
import pandas

class QuestionairesAgri(FlaskForm):
	name_exploit = wtforms.TextField('Nom exploitation', validators=[DataRequired()])
	address   = wtforms.TextField('Address', validators=[DataRequired()])
	age = wtforms.TextField('Age', validators=[DataRequired()])
	sau = wtforms.TextField('sau', validators=[DataRequired()])
	etp = wtforms.TextField('etp', validators=[DataRequired()])
	haie = wtforms.SelectField(u'Presence haies', choices=[('init', 'sélectionnez la proposition'),('y1', 'oui sur toutes les parcelles'), ('y2', 'oui sur une partie des parcelles'), ('no', 'non')])
	cepage = wtforms.SelectMultipleField(choices=[('init', 'sélectionnez la proposition'),('cep1', 'cabernet sauvignon'), ('cep2', 'carignan'), ('cep3', 'grenache noir'), ('cep4', 'syrah'), ('cep5', 'muscat'), ('cep6', 'chardonnay'), ('cep7', 'cinsault')])
	autract = wtforms.TextField('autre activite', validators=[DataRequired()])
	autrcult = wtforms.SelectField(u'autre cultures', choices=[('init', 'sélectionnez la proposition'),('y', 'oui'), ('n', 'non')])
	typecult = wtforms.TextField('type culture', validators=[DataRequired()])
	typefonc = wtforms.SelectField(u'type de foncier', choices=[('init', 'sélectionnez la proposition'),('prop', 'proprietaire'), ('loc', 'locataire'), ('mist', 'proprietaire et locataire')])
	certif = wtforms.SelectField(u'certification', choices=[('bio', 'label BIO'),('hve', 'label HVE'),('els', 'autre'),('n', 'aucune')])
	autrecertif = wtforms.TextField('autre certication', validators=[DataRequired()])
	qual = wtforms.SelectField(u'certification qualite', choices=[('init', 'sélectionnez la proposition'),('igp', 'IGP'),('aop', 'AOP'),('elsqual','autre'),('n', 'aucune')])
	autrequal = wtforms.TextField('autre qualite', validators=[DataRequired()])
	ift = wtforms.TextField('ift', validators=[DataRequired()])
	intrant = wtforms.TextField('intrant', validators=[DataRequired()])
	irrig = wtforms.RadioField(choices=[('init', 'sélectionnez la proposition'),('no_irrig','aucune irrigation'),('yes_irrig1', 'oui sur la majorité des parcelles'),('yes_irrig2', 'oui sur certaines parcelles')])
	mutu = wtforms.SelectMultipleField(choices=[('init', 'sélectionnez la proposition'),('yes_mutu', 'oui'),('no_mutu', 'non')])
	

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



