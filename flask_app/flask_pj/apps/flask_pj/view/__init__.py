from .index import index
from .api import api
from .changeBook import changeBook
from .homepage import homepage
from .practice import practice
from .select import select
from .myPlan import myPlan
from .words import words
from .personal import personal
from .login import login
from .pay import pay

bps = [index, api, changeBook, homepage, practice, myPlan, select, words, personal, login, pay]


def init_blue_print(app):
    for bp in bps:
        app.register_blueprint(bp)
