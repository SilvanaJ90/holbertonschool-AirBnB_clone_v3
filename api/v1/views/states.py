#!/usr/bin/python3
"""
State objects that handles all default RESTFul API
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import request, jsonify, abort

ignored = ['id', 'created_at', 'updated_at']


@app_views.route('/states', strict_slashes=False,
                 methods=['GET', 'POST'])
def get_all_states():
    """ Retrieves the list of all State objects: GET, POST """
    if request.method == 'GET':
        state = storage.all(State)
        states = []
        for key, value in state.values():
            states.append(value.to_dict())
        return jsonify(states)

    if request.method == 'POST':
        state = State()
        if request.get_json(silent=True) is None:
            return 'Not a JSON', 400
        if 'name' not in request.get_json(silent=True).keys():
            return 'Missing name', 400
        for key in request.get_json(silent=True):
            if key not in ignored:
                setattr(state, key, request.get_json(silent=True)[key])
        state.save()
        return(state.to_dict()), 201
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_del_put_state_id(state_id):
    """ GET, DELETE and PUT requests for state by id """
    if request.method == 'GET':
        state = storage.all(State)
        for key, value in state.values():
            if value.id == state_id:
                return value.to_dict()
        abort(404)
    if request.method == 'DELETE':
        state = storage.all(State)
        for key, value in state.values():
            if value.id == state_id:
                storage.delete(value)
                storage.save()
                return {}, 200
        abort(404)

    if request.method == 'PUT':
        if request.get_json(silent=True) is None:
            return 'Not a JSON', 400
        state = storage.all(State)
        for key, value in state.values():
            if value.id == state_id:
                for key in request.get_json(silent=True):
                    if key not in ignored:
                        setattr(value, key, request.get_json(silent=True)[key])
                storage.save()
                return value.to_dict(), 200
        abort(404)
