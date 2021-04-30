# -*- encoding: utf-8 -*-
"""
Modified for GRID, 2021

Copyright (c) 2019 - present AppSeed.us

Gère les routines des connnexions et inscription
"""

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
import pandas, os
import pyotp

from app import db, login_manager

from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User

from app.base.util import verify_pass

import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

import run
from agri_data import data_draw

import qrcode

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'key' in request.form:
        print('C1', request.form)
        username = request.form['username']
        password = request.form['password']
        var_key = request.form['key']

        user = User.query.filter_by(username=username).first()
        key = user.two_fa_key
        current_var_key = pyotp.TOTP(key).now()

        if user and verify_pass( password, user.password):
            print('C1.1', request.form)
            if var_key == current_var_key:
                print('C1.1.1', request.form)
                login_user(user)
                data_draw.RandomDraw().main()

                render = run.index()
                return render
            else:
                print('C1.1.2', request.form)
                return render_template('accounts/login.html', msg = 'Clé incorrecte', type='wrong',
                    two_fa=True, pwd = True, user=user, form=login_form)

        else:
            print('C2.1', request.form)
            return render_template('accounts/login.html', msg = 'Mot de passe incorrecte', type='wrong',
                    two_fa=True, pwd = True, user=user, form=login_form)

    elif 'login' in request.form:
        # read form data
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        print('C2', request.form)
        if user:
            if 'password' in request.form:
                password = request.form['password']
                print('C2.1')
                if user and verify_pass( password, user.password):
                    print('C2.1.1')
                    login_user(user)
                    data_draw.RandomDraw().main()

                    render = run.index()
                    return render
                else:
                    print('C.1.2', request.form)
                    return render_template('accounts/login.html', msg = 'Mot de passe incorrecte', type='wrong',
                        two_fa=False, pwd = True, user=user, form=login_form)

            else :
                print('C2.2')
                if user.two_fa:
                    print('C2.2.1')
                    return render_template('accounts/login.html', msg = 'Rentrez votre mot de passe et clé unique', type='info',
                        two_fa=True, pwd = True, user=user, form=login_form)

                else:
                    print('C2.2.2')
                    return render_template('accounts/login.html', msg = 'Rentrez votre mot de passe', type='info',
                        two_fa=False, pwd = True, user=user, form=login_form)
        else:
            return redirect(f"/register")

        """
            login_user(user)
            data_draw.RandomDraw().main()

            render = run.index()
            return render
        """
        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Utilisateur non existant ou mot de passe incorrecte', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form, user='test')

    render = run.index()
    return render


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:
        if 'cle' not in request.form.keys():
            username  = request.form['username']
            email     = request.form['email'   ]

            # Check usename exists
            user = User.query.filter_by(username=username).first()
            
            if user:
                return render_template( 'accounts/register.html', 
                                        msg='Username already registered',
                                        success=False,
                                        register = True,
                                        registration = True,
                                        form=create_account_form)

            # Check email exists
            user = User.query.filter_by(email=email).first()
            if user:
                return render_template( 'accounts/register.html', 
                                        msg='Email already registered', 
                                        success=False,
                                        register = True,
                                        registration = True,
                                        form=create_account_form)
                
            type_auth = 'totp'
            issuer = 'GRID'
            account = username

            key = pyotp.random_base32()
            url = f'otpauth://{type_auth}/{issuer}:{account}?secret={key}'

            current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
            file_name='qrcode_test.png'
            full_path = os.path.normcase(f'{current}/static/assets/img/{file_name}')

            img = qrcode.make(url)
            img.save(full_path)

            data = {'two_fa' : True, 'two_fa_key': key}
            
            user = User(**request.form, 
                **data
                )
            print(user)
            
            db.session.add(user)
            db.session.commit()
            
            return render_template( 'accounts/register.html', 
                                    img=file_name, 
                                    register = True,
                                    registration=False,
                                    form=create_account_form)
            

        else:
            return render_template( 'accounts/register.html', 
                                    msg='User created please <a href="/login">login</a>', 
                                    success=True,
                                    register = False,
                                    registration=True,
                                    form=create_account_form)

            """
            user = User.query.filter_by(username=username).first()
            key = user.two_fa_key
            current_var_key = pyotp.TOTP(key).now()

            current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
            file_name='qrcode_test.png'
            full_path = os.path.normcase(f'{current}/static/assets/img/{file_name}')

            print (int(request.form['cle']))
            print(current_key)
            print(type(current_key))

            if request.form['cle'] == current_key:
                print('hey')
                return render_template( 'accounts/register.html', 
                                    msg='User created please <a href="/login">login</a>', 
                                    success=True,
                                    register = False,
                                    registration=True,
                                    form=create_account_form)
            else:
                return render_template( 'accounts/register.html',
                                    register = True,
                                    registration=False,
                                    form=create_account_form)
            """

    else:
        return render_template( 'accounts/register.html', form=create_account_form, register = True, registration=True)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'





## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
