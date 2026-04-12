from flask import jsonify


def api_ok(data=None, message='ok'):
    return jsonify({'code': 0, 'message': message, 'data': data if data is not None else {}}), 200


def api_error(message, status=400, code=1, data=None):
    payload = {'code': code, 'message': message}
    if data is not None:
        payload['data'] = data
    return jsonify(payload), status
