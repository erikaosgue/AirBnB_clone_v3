#!/usr/bin/python3
"""New view for Place objects """


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place

app.url_map.strict_slashes = False


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_places(city_id):
    """Retrieves the list of all place objects from a city"""
    dict_places = []
    obj_city = storage.get("City", city_id)
    if obj_city is None:
        abort(404)

    for obj_place in obj_city.places:
        dict_places.append(obj_place.to_dict())
    return jsonify(dict_places)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE'])
def place_id(place_id):
    """ Retrieves or deletes a place object based on the place_id"""

    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)

    if request.method == "GET":
        return jsonify(obj_place.to_dict())

    if request.method == "DELETE":
        storage.delete(obj_place)
        storage.save()
        return jsonify({}), 200


@app_views.route('cities/<city_id>/places', methods=['POST'])
def place_post(city_id):
    """Creates and Add a new place object to a city based on the city_id"""

    obj_city = storage.get("City", city_id)
    if obj_city is None:
        abort(404)

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    if "name" not in data.keys():
        abort(400, description="Missing name")
    if "user_id" not in data.keys():
        abort(400, description="Missing user_id")

    user_id = data["user_id"]
    obj_user = storage.get("User", user_id)
    if obj_user is None:
        abort(404)

    data["city_id"] = city_id
    obj_place = Place(**data)
    print("herhehre\n", obj_place.to_dict())
    storage.new(obj_place)
    storage.save()
    return jsonify(obj_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_delete(place_id):
    """ Retrieves or deletes a place object based on the place_id"""

    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")

    ingore_keys = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for key, value in data.items():
        if key not in ingore_keys:
            setattr(obj_place, key, value)
    obj_place.save()
    return jsonify(obj_place.to_dict()), 200