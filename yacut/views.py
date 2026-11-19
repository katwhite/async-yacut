from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import FileForm, MainForm
from .models import URLMap


def get_unique_short_id():
    """алгоритм формирования коротких идентификаторов переменной длины"""
    ...


@app.route('/')
def index_view():
    ...


@app.route('/files')
def index_view():
    ...