#!/usr/bin/python3
"""city"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, make_response, request, abort
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_id(state_id):
    """Retrieves the list of all City objects of a State"""
    if not storage.get(State, state_id):
        abort(404)
    state = storage.get(State, state_id)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object. : GET /api/v1/cities/<city_id>"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_cities_id(city_id):
    """Deletes a City object: DELETE /api/v1/cities/<city_id>"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_cities(state_id):
    """Creates a City: POST /api/v1/states/<state_id>/cities"""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    req = request.get_json()
    new_city = City(**req)
    new_city.state_id = state.id
    new_city.save()
    return make_response(jsonify(new_city .to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id):
    """Updates a City object: PUT /api/v1/cities/<city_id>"""
    req = request.json
    if not req:
        abort(400, description="Not a JSON")
    if not storage.get(City, city_id):
        abort(404)
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in req.items():
        if key not in ignore:
            cities = storage.get(City, city_id)
            setattr(cities, key, value)
    storage.save()
    return make_response(jsonify(cities.to_dict()), 200)
