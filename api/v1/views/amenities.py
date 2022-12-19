#!/usr/bin/python3

""" Amenity objects that handles all default RESTFul API """

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import request, jsonify, abort

ignored = ['id', 'created_at', 'updated_at']


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET', 'POST'])
def all_amenity():
    if request.method == 'GET':
        amenity= storage.all(Amenity)
        amenities = []
        for key, val in amenity.items():
            amenities.append(val.to_dict())
        return jsonify(amenities)

    if request.method == 'POST':
        amenity = Amenity()
        if request.get_json(silent=True) is None:
            return 'Not a JSON', 400
        if 'name' not in request.get_json(silent=True).keys():
            return 'Missing name', 400

        for key in request.get_json(silent=True):
            if key not in ignored:
                setattr(amenity, key, request.get_json(silent=True)[key])
        amenity.save()
        return(amenity.to_dict()), 201
    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_by_id(amenity_id):
    if request.method == 'GET':
        amenity = storage.all(Amenity)
        for key, val in amenity.items():
            if val.id == amenity_id:
                return val.to_dict()
        abort(404)

    if request.method == 'DELETE':
        amenity = storage.all(Amenity)
        for key, val in amenity.items():
            if val.id == amenity_id:
                storage.delete(val)
                storage.save()
                return {}, 200
        abort(404)

    if request.method == 'PUT':
        if request.get_json(silent=True) is None:
            return 'Not a JSON', 400

        ignored_keys = ['id', 'created_at', 'updated_at']
        amenity_objects = storage.all(Amenity)
        for key, val in amenity_objects.items():
            if val.id == amenity_id:
                for key in request.get_json(silent=True):
                    if key not in ignored_keys:
                        setattr(val, key, request.get_json(silent=True)[key])
                storage.save()
                return val.to_dict(), 200
        abort(404)
