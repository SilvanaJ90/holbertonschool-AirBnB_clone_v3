#!/usr/bin/python3

"""  Place objects that handles all default RESTFul API"""

from models import storage
from models.user import User
from models.city import City
from models.place import Place
from api.v1.views import app_views
from flask import request, jsonify, abort

ignored = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def all_places(city_id):
    place = storage.all(City)
    for key, val in place.items():
        if val.id == city_id:
            if request.method == 'GET':
                place_list = []
                places = storage.all(Place)
                for keys, vals in places.items():
                    if vals.city_id == city_id:
                        place_list.append(vals.to_dict())
                return jsonify(place_list)

            if request.method == 'POST':
                place = Place()
                if request.get_json(silent=True) is None:
                    return 'Not a JSON', 400
                if 'user_id' not in request.get_json(silent=True).keys():
                    return 'Missing user_id', 400
                if 'name' not in request.get_json(silent=True).keys():
                    return 'Missing name', 400
                user = storage.all(User)
                for keys, val in user.items():
                    if val.id == request.get_json(silent=True)["user_id"]:
                        for key in request.get_json(silent=True):
                            setattr(place, key, request.get_json(silent=True)[key])
                        setattr(place, "city_id", city_id)
                        place.save()
                        return place.to_dict(), 201
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def places_by_id(place_id):
    place_obj = storage.all(Place)
    for key, value in place_obj.items():
        if value.id == place_id:

            if request.method == 'GET':
                return value.to_dict()

            if request.method == 'PUT':
                data = request.get_json(silent=True)
                if data is None:
                    return 'Not a JSON', 400
                for key in data:
                    if key not in ignored:
                        setattr(value, key, data[key])
                storage.save()
                return value.to_dict(), 200

            if request.method == 'DELETE':
                storage.delete(value)
                storage.save()
                return {}, 200
    abort(404)
