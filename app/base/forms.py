# -*- encoding: utf-8 -*-
"""
Modified for GRID, 2021

Copyright (c) 2019 - present AppSeed.us

Génère les formulaires d'inscription et de connexion
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Email, DataRequired, Length

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])
    key = TextField('Password', id='pwd_login'        , validators=[DataRequired(), Length(min=6, max=6, message='Code à 6 chiffres')])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])
    cle =TextField('Key' , id='key')


