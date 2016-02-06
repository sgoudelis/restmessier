#!env/bin/python
import json
import time

from bson import ObjectId
from config import *
from flask import Flask, jsonify, url_for, abort, request
from jsonschema import validate
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(mongodb_url)
astronomydb = client.AstronomyCatalogs
messier_collection = astronomydb.Messier


def message_template():
    """
    Return a message template for consistency throughout
    """
    message = {
        'responded': time.time(),
    }
    return message


def sanitize(message):
    """
     Sanitize message, use JSONEncoder
    :param message:
    :return:
    """

    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, ObjectId):
                return str(o)
            return json.JSONEncoder.default(self, o)

    message = JSONEncoder().encode(message)
    message = json.loads(message)
    return message


@app.route('/astronomy/messier/', methods=['GET'])
def list_messier_objects():
    """
    Reply with a list of Messier objects
    """
    messier_catalog = []
    messier_list = messier_collection.find()

    # make a list of objects
    for messier_object in messier_list:
        messier_object['url'] = url_for('get_messier_object_by_mid', mid=messier_object['mid'], _external=False)
        messier_catalog.append(messier_object)

    # get a message template
    message = message_template()

    # add the list of Messier objects
    message['messierobjects'] = messier_catalog

    message = sanitize(message)

    # return message
    return jsonify(message)


@app.route('/astronomy/messier/<string:mid>', methods=['GET'])
def get_messier_object_by_mid(mid):
    """
    Reply with the Messier object based on mid
    :param mid:
    :return:
    """

    # perform a case-insensitive search 
    messier_object = messier_collection.find_one({'mid': {'$regex': mid, '$options': '-i'}})

    if not messier_object:
        abort(404)

    messier_object['url'] = url_for('get_messier_object_by_mid', mid=messier_object['mid'], _external=False)

    message = message_template()

    message['object'] = messier_object

    message = sanitize(message)

    return jsonify(message)


@app.route('/astronomy/messier/', methods=['POST'])
def create_messier_object_by_mid():
    """
    Create a Messier object
    """

    if type(request.json) is not dict:
        abort(400)

    messier_object_schema = {
        "type": "object",
        "properties": {
            "loc": {"type": "object"},
            "mid": {"type": "string"},
            "ngcid": {"type": "string"},
            "remarks": {"type": "string"},
            "constellation": {"type": "string"}
        }
    }

    # verify POSTed Messier object schema
    try:
        validate(request.json, messier_object_schema)
        new_messier_object = request.json
    except:
        raise

    messier_collection.insert(new_messier_object)

    new_messier_object['url'] = url_for('get_messier_object_by_mid', mid=new_messier_object['mid'], _external=False)

    message = message_template()

    message['object'] = new_messier_object

    message = sanitize(message)

    return jsonify(message)


@app.route('/astronomy/messier/<string:mid>', methods=['PUT'])
def update_messier_object_by_mid(mid):
    """
    Update the Messier object in the database and return the new object as a reply.
    It will expect a PUT body in the following form:
    {'key': value, 'key': value} where key may be an already existing key in the Messier object
    of mid

    :param mid:
    :return:
    """

    mid = mid.upper()
    messier_object = messier_collection.find_one({'mid': mid})

    if not messier_object:
        abort(404)
    if type(request.json) is not dict:
        abort(400)

    updates = request.json

    for key in updates:
        messier_object[key] = updates[key]

    # update the db
    messier_collection.update_one({'_id': messier_object['_id']}, {"$set": messier_object})

    message = message_template()

    message['object'] = messier_object

    message = sanitize(message)

    return jsonify(message)


@app.route('/astronomy/messier/<string:mid>', methods=['DELETE'])
def delete_messier_object_by_mid(mid):
    """
    Delete Messier object by mid
    :param mid:
    :return:
    """

    mid = mid.upper()
    messier_object = messier_collection.find_one({'mid': mid})

    if not messier_object:
        abort(404)

    result = messier_collection.delete_one({'_id': messier_object['_id']})
    if result.deleted_count == 0:
        abort(501)

    messier_object['status'] = "deleted"

    message = message_template()

    message['object'] = messier_object

    message = sanitize(message)

    return jsonify(message)


@app.route('/astronomy/messier/<string:mid>/nearby/<int:degrees>', methods=['GET'])
def get_nearby_objects_by_mid(mid, degrees):
    """
    Based on a given Messier object and angular distance, find nearby objects
    :param mid:
    :param degrees:
    :return:
    """

    # find center object
    mid = mid.upper()
    center_object = messier_collection.find_one({'mid': mid})

    if not center_object or not degrees:
        abort(404)

    center_object['url'] = url_for('get_messier_object_by_mid', mid=center_object['mid'], _external=False)

    # calculate degrees from radians
    radians = degrees * (3.14 / 180)

    # find objects near
    nearby_objects = []
    nearby_objects_cursor = messier_collection.find({'loc': {'$geoWithin':
                                                    {'$centerSphere':
                                                        [[center_object['loc']['coordinates'][0],
                                                          center_object['loc']['coordinates'][1]],
                                                         radians]}
                                                          }})
    # loop through the result
    if nearby_objects_cursor:
        for nearby_object in nearby_objects_cursor:
            nearby_object['url'] = url_for('get_messier_object_by_mid', mid=nearby_object['mid'], _external=False)
            if nearby_object['mid'] != center_object['mid']:
                nearby_objects.append(nearby_object)

    message = message_template()

    message['centerobject'] = center_object
    message['nearbyobjects'] = nearby_objects

    message = sanitize(message)

    return jsonify(message)


@app.route('/astronomy/messier/nearby/<float:ra>/<float:dec>/<int:degrees>', methods=['GET'])
def get_nearby_objects_by_coord(ra, dec, degrees):
    """

    :param ra:
    :param dec:
    :param degrees:
    :return:
    """
    if not ra or not dec or not degrees:
        abort(400)

    # calculate radians from degrees
    radians = degrees * (3.14 / 180)

    # find objects near
    nearby_objects = []
    nearby_objects_cursor = messier_collection.find({'loc': {'$geoWithin': {'$centerSphere':[[ra, dec], radians]}}})
    # loop through the result
    if nearby_objects_cursor:
        for nearby_object in nearby_objects_cursor:
            nearby_object['url'] = url_for('get_messier_object_by_mid', mid=nearby_object['mid'], _external=False)
            nearby_objects.append(nearby_object)

    message = message_template()
    message['target'] = {'coordinates': (ra, dec), 'degrees': degrees}

    message['nearbyobjects'] = nearby_objects

    message = sanitize(message)

    return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True)
