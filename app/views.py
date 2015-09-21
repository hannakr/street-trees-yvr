from flask import render_template, flash, redirect, url_for, request
from app import app
from .forms import SearchForm
from models import *
from .utils import parse_address

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/search', methods=['GET'])
def search():
    form = SearchForm()
    houses = House.query.order_by(House.civicNumber).filter(House.stdStreet==parse_address(request.args.get('street')),
                                (House.civicNumber==request.args.get('number') if request.args.get('number') else '')).all()
    form.street.data = request.args.get('street')
    form.number.data = request.args.get('number')
    return render_template('search.html',
                           title='Find Address',
                           form=form,
                           houses=houses,
                           street=request.args.get('street'),
                           number=request.args.get('number'))

@app.route('/house/<id>')
def house(id):
    house = House.query.filter_by(id=id).first_or_404()
    return render_template('house.html', id=house.id,
                                           number=house.civicNumber,
                                           street=house.stdStreet,
                                           trees=house.trees.all())
