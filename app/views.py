from flask import render_template, flash, redirect, url_for, request
from app import app
from .forms import LoginForm
from .forms import SearchForm
from models import *

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Keith'}  # fake user
    sites = [  # fake array of posts
        {
            'house': '189 Keefer Street',
            'tree': {'common_name': 'EASTERN REDBUD', 'genus_name': 'CERCIS', 'species_name': 'CANADENSIS'}
        },
        {
            'house': '778 Prior Street',
            'tree': {'common_name': 'SHORE PINE', 'genus_name': 'PINUS', 'species_name': 'CONTORTA'}
        },
        {   'house': '919 Station Street',
            'tree': {'common_name': 'WESTERN HEMLOCK', 'genus_name': 'TSUGA', 'species_name': 'HETEROPHYLLA'}
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           sites=sites)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/search', methods=['GET'])
def search():
    form = SearchForm()
    houses = House.query.order_by(House.civicNumber).filter(House.stdStreet==request.args.get('street'),
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
