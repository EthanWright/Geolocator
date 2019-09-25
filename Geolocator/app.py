#!flask/bin/python
from flask import Flask, jsonify, request, abort
from Geolocator import AddressToCoordinateConverter


app = Flask(__name__)

@app.errorhandler(400)
def custom400(error):
    return jsonify(error.description)


@app.route('/coordinates/<string:address>', methods=['GET'])
def get_coordinates(address):
    convert_service = AddressToCoordinateConverter()
    result = convert_service.convert_address_to_coordinates(address)

    if not result.get('coordinates'):
        abort(400, result.get('errors'))

    return jsonify({
        'latitude': result.get('coordinates').latitude,
        'longitude': result.get('coordinates').longitude
    })


if __name__ == '__main__':
    app.run(debug=True)