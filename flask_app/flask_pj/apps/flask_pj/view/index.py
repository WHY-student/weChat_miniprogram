import os

import flask
from flask import Blueprint, current_app, render_template, request
from flask_pj.apps.utils import get_abs_dir
from flask_pj.apps.utils.constants import METHODTYPE
index = Blueprint('index', __name__, url_prefix='/index')


@index.route('/', methods=[METHODTYPE.GET, METHODTYPE.POST])
def index_home():
    # current_app.logger.info(f'{request.method} for index.home')
    if request.method == METHODTYPE.GET:
        name = request.args.get('name', 'Python')
        return render_template('home.html', name=name)  # return html Content
    else:
        # name = request.form.get('name', 'Python')   # for request that POST with application/x-www-form-urlencoded
        print("OK")
        return "OK"
        # return f"Hello {name}", 200         # return plain text Content
