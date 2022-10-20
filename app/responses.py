from email import message
from flask import jsonify

def bad_request():
    return jsonify(
        {
            'success': False,
            'data':{
                'message': 'Bad request',
                'code': 400
            }
        }
    ), 400

def not_found():
    return jsonify(
        {
            'success': False,
            'data':{
                'message': 'Resource not found',
                'code': 404
            }
        }
    ), 404

def response(data, success = True):
    return jsonify(
        {
            'success': success,
            'data': data
        }
    ),200