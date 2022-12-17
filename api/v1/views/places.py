#!/usr/bin/python3
""" Place objects that handles all default RESTFul API"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def place_all():
    """Retrieves the list of all Place objects of a City"""
    place = []
    for i in storage.all("Place").values():
        place.append(i.to_dict())
    return jsonify(place)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(state_id):
    """Retrieves a Place object"""
    places = storage.get("State", state_id)
    if places is None:
        abort(404, description="Not found")
    return jsonify(places.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_id(state_id):
    """Deletes a Place object: DELETE /api/v1/places/<place_id>"""
    places = storage.get("State", state_id)
    if places is None:
        abort(404, description="Not found")
    places.delete()
    storage.save()
    return jsonify({}, 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place():
    """Creates a Place: POST"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    new_place= State(**request.get_json())
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/api/v1/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(state_id):
    """UUpdates a Place object: PUT"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not storage.get("State", state_id):
        abort(404, description="Not found")
    for key, value in request.get_json().items():
        if key not in  ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            places = storage.get("State", state_id)
            setattr(places, key, value)
    storage.save()
    return make_response(jsonify(places.to_dict()), 200)
