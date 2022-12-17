#!/usr/bin/python3

""" d """

from models import storage
from models import review
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import request, jsonify, abort

ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def all_place_reviews(place_id):

    places = storage.all(Place)
    for key, value in places.items():
        if value.id == place_id:
            if request.method == 'GET':
                review_list = []
                reviews = storage.all(Review)
                for key, value in reviews.items():
                    if value.place_id == place_id:
                        review_list.append(value.to_dict())
                return jsonify(review_list)

            if request.method == 'POST':
                review = Review()
                valid_request = request.get_json(silent=True)
                if valid_request is None:
                    return 'Not a JSON', 400
                if 'user_id' not in valid_request.keys():
                    return 'Missing user_id', 400
                if 'text' not in valid_request.keys():
                    return 'Missing text', 400
                users = storage.all(User)
                for key, value in users.items():
                    if value.id == valid_request['user_id']:
                        for k in valid_request:
                            setattr(review, k, valid_request[k])
                        setattr(review, 'place_id', place_id)
                        review.save()
                        return review.to_dict(), 201
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def review_by_id(review_id):

    reviews = storage.all(Review)
    for key, value in reviews.items():
        if value.id == review_id:

            if request.method == 'GET':
                return value.to_dict()

            if request.method == 'DELETE':
                storage.delete(value)
                storage.save()
                return {}, 200

            if request.method == 'PUT':
                valid_request = request.get_json(silent=True)
                if valid_request is None:
                    return 'Not a JSON', 400
                for k in valid_request:
                    if k not in ignored_keys:
                        setattr(value, k, valid_request[k])
                storage.save()
                return value.to_dict(), 200
    abort(404)
