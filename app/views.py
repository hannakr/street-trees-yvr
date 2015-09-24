from flask import render_template, flash, redirect, url_for, request
from app import app
from .forms import SearchForm
from models import *
from .utils import parse_address

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home',
                           is_home=True)


@app.route('/search', methods=['GET'])
def search():
    form = SearchForm()
    response = request.args.get('address')
    number, street = parse_address(response)
    print street
    houses = House.query.order_by(House.civicNumber).filter(House.stdStreet==street,
                                (House.civicNumber==number if number else '')).all()
    form.address.data = number + " " + street
    return render_template('search.html',
                           title='Find Address',
                           form=form,
                           houses=houses,
                           is_search=True)

@app.route('/house/<id>')
def house(id):
    house = House.query.filter_by(id=id).first_or_404()
    houses = House.query.order_by(House.civicNumber).filter(House.stdStreet==house.stdStreet).all()
    main_house_index = houses.index(house)
    if main_house_index > 0:
        prev_house_id = houses[main_house_index - 1].id
    else:
        prev_house_id = None
    try:
        next_house_id = houses[main_house_index + 1].id
    except IndexError:
        next_house_id = None
    return render_template('house.html', id=house.id,
                                            prev_house_id=prev_house_id,
                                            next_house_id=next_house_id,
                                           number=house.civicNumber,
                                           street=house.stdStreet,
                                           trees=house.trees.order_by(Tree.cell).all())
