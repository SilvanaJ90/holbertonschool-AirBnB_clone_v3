#!/usr/bin/python3
"""
State objects that handles all default RESTFul API
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/states',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def all_states():
    """ GET, POST Retrieves the list of  State objects """
    if request.method == 'GET':
        states = storage.all(State)
        states_list = []
        for key, value in states.items():
            states_list.append(value.to_dict())
        return jsonify(states_list)

    if request.method == 'POST':
        data = request.get_json(silent=True)
        state = State()
        if data is None:
            return 'Not a JSON', 400
        if 'name' not in data.keys():
            return 'Missing name', 400
        ignored_keys = ['id', 'created_at', 'updated_at']
        for key in data:
            if key not in ignored_keys:
                setattr(state, key, data[key])
        state.save()
        return(state.to_dict()), 201
    abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def states_by_id(state_id):
    """ GET, DELETE and PUT requests for state by id """
    if request.method == 'GET':
        states = storage.all(State)
        for key, value in states.items():
            if value.id == state_id:
                return value.to_dict()
        abort(404)

    if request.method == 'DELETE':
        states = storage.all(State)
        for key, value in states.items():
            if value.id == state_id:
                storage.delete(value)
                storage.save()
                return {}, 200
        abort(404)

    if request.method == 'PUT':
        valid_request = request.get_json(silent=True)
        if valid_request is None:
            return 'Not a JSON', 400

        ignored_keys = ['id', 'created_at', 'updated_at']
        states = storage.all(State)
        for key, value in states.items():
            if value.id == state_id:
                for key in valid_request:
                    if key not in ignored_keys:
                        setattr(value, key, valid_request[key])
                storage.save()
                return value.to_dict(), 200
        abort(404)
