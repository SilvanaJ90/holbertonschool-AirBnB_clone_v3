#!/usr/bin/python3

"""Review object that handles all default RESTFul API actions"""

from models import storage
from models import review
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import request, jsonify, abort

ignored = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']


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
                if request.get_json(silent=True) is None:
                    return 'Not a JSON', 400
                if 'user_id' not in request.get_json(silent=True).keys():
                    return 'Missing user_id', 400
                if 'text' not in request.get_json(silent=True).keys():
                    return 'Missing text', 400
                users = storage.all(User)
                for key, value in users.items():
                    if value.id == request.get_json(silent=True)['user_id']:
                        for k in request.get_json(silent=True):
                            setattr(review, k, request.get_json(silent=True)[k])
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
                if request.get_json(silent=True) is None:
                    return 'Not a JSON', 400
                for k in request.get_json(silent=True):
                    if k not in ignored:
                        setattr(value, k, request.get_json(silent=True)[k])
                storage.save()
                return value.to_dict(), 200
    abort(404)
