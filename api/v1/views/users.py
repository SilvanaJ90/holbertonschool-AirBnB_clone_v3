#!/usr/bin/python3

""" User object that handles all default RESTFul API  """

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, abort

ignored = ['id', 'created_at', 'updated_at']


@app_views.route('/users', strict_slashes=False,
                 methods=['GET', 'POST'])
def all_users():
    if request.method == 'GET':
        user = storage.all(User)
        users = []
        for key, val in user.items():
            users.append(val.to_dict())
        return jsonify(users)

    if request.method == 'POST':
        user = User()
        if request.get_json(silent=True) is None:
            return 'Not a JSON', 400
        if 'email' not in request.get_json(silent=True).keys():
            return 'Missing email', 400
        if 'password' not in request.get_json(silent=True).keys():
            return 'Missing password', 400
        ignored_keys = ['id', 'created_at', 'updated_at']
        for key in request.get_json(silent=True):
            if key not in ignored_keys:
                setattr(user, key, request.get_json(silent=True)[key])
        user.save()
        return(user.to_dict()), 201
    abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def users_by_id(user_id):
    if request.method == 'GET':
        user = storage.all(User)
        for key, value in user.items():
            if value.id == user_id:
                return value.to_dict()
        abort(404)

    if request.method == 'DELETE':
        user = storage.all(User)
        for key, value in user.items():
            if value.id == user_id:
                storage.delete(value)
                storage.save()
                return {}, 200
        abort(404)

    if request.method == 'PUT':
        if request.get_json(silent=True) is None:
            return 'Not a JSON', 400
        user = storage.all(User)
        for key, value in user.items():
            if value.id == user_id:
                for key in request.get_json(silent=True):
                    if key not in ignored:
                        setattr(value, key, request.get_json(
                                silent=True)[key])
                storage.save()
                return value.to_dict(), 200
        abort(404)
