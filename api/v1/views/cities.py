#!/usr/bin/python3

""" City objects that handles all default RESTFul API """

from models import storage
from api.v1.views import app_views
from models.state import State, City
from flask import request, jsonify, abort

ignored = ['id', 'created_at', 'updated_at', 'state_id']


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST', 'POST'])
def all_cities(state_id):
    """ GET, POST City objects of a State"""
    state = storage.all(State)
    for key, value in state.items():
        if value.id == state_id:
            if request.method == 'GET':
                city = storage.all(City)
                cities = []
                for key, value in city.items():
                    if value.state_id == state_id:
                        cities.append(value.to_dict())
                return jsonify(cities)

            if request.method == 'POST':
                cities = City()
                request.get_json(silent=True)
                if request.get_json(silent=True) is None:
                    return 'Not a JSON', 400
                if 'name' not in request.get_json(silent=True).keys():
                    return 'Missing name', 400
                for key in request.get_json(silent=True):
                    if key not in ignored:
                        setattr(cities, key, request.get_json(silent=True)[key])
                    setattr(cities, "state_id", state_id)
                cities.save()
                return cities.to_dict(), 201
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def cities_by_id(city_id):
    """ GET, DELETE and PUT cities by id """
    city = storage.all(City)
    for key, value in city.items():
        if value.id == city_id:

            if request.method == 'GET':
                return value.to_dict()

            if request.method == 'PUT':
                if request.get_json(silent=True) is None:
                    return 'Not a JSON', 400
                for key in request.get_json(silent=True):
                    if key not in ignored:
                        setattr(value, key, request.get_json(silent=True)[key])
                storage.save()
                return value.to_dict(), 200

            if request.method == 'DELETE':
                storage.delete(value)
                storage.save()
                return {}, 200
    abort(404)
