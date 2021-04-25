# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
Modfied the GRID, 2021
"""

from flask import Blueprint

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)


