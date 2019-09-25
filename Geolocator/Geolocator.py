
"""
Author: Ethan Wright, 9/20/19
"""
import json
import urllib
from ConfigParser import SafeConfigParser


class CoordinateException(Exception):
    pass


class Coordinate(object):
    latitude = None
    longitude = None

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class AddressToCoordinateConverter(object):

    errors = []

    def convert_address_to_coordinates(self, address):
       
        coordinates = self._call_coordinates_service(GoogleCoordinatesService, address)
        if not coordinates:
            coordinates = self._call_coordinates_service(HereCoordinatesService, address)

        return {
            'coordinates': coordinates,
            'errors': self.errors
        }

    def _call_coordinates_service(self, service, address):

        try:
            coordinates = service().get_coordinates(address)

        except CoordinateException as e:
            self.errors.append(str(e))
            return None

        return coordinates

   
class BaseCoordinatesService(object):

    def __init__(self):
        parser = SafeConfigParser()
        parser.read('credentials.txt')

        self.api_key = parser.get(self.service_type, 'app_code')
        self.api_id = parser.get(self.service_type, 'app_id')

    def call_coordinates_service(self, address):
        """Call the coordinate service"""
        formatted_uri = self.url.format(
            api_id=self.api_id, api_key=self.api_key, address=address
            )

        connection = urllib.urlopen(formatted_uri)
        try:
            coordinates = connection.read()
        finally:
            connection.close()

        return json.loads(coordinates)

    def get_coordinates(self, address):
        """Return the latitude and longitude coordinates for an address"""

        result_json = self.call_coordinates_service(address)

        return self.parse_results(result_json)
    
    def parse_results(self, address):
        raise NotImplementedError()
   
    def construct_url(self):
        raise NotImplementedError()
   

class GoogleCoordinatesService(BaseCoordinatesService):

    service_type = 'google'
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&sensor=false&key={api_key}"

    def parse_results(self, result_json):
        
        if result_json.get('status') == 'REQUEST_DENIED':
            raise CoordinateException("Google API request denied")

        elif result_json.get('status') == 'ZERO_RESULTS':
            raise CoordinateException("Error looking up address")

        if 'bounds' in result_json['results'][0]['geometry']:
            bounds = result_json['results'][0]['geometry']['bounds']
            latitude = (bounds['northeast']['lat'] + bounds['southwest']['lat']) / 2
            longitude = (bounds['northeast']['lng'] + bounds['southwest']['lng']) / 2

        elif 'location' in result_json['results'][0]['geometry']:
            latitude = result_json['results'][0]['geometry']['location']['lat']
            longitude = result_json['results'][0]['geometry']['location']['lng']

        else:
            raise CoordinateException("Error looking up address")

        return Coordinate(latitude, longitude)


class HereCoordinatesService(BaseCoordinatesService):

    service_type = 'here'
    url = "https://geocoder.api.here.com/6.2/geocode.json?app_id={api_id}&app_code={api_key}&searchtext={address}"

    def parse_results(self, result_json):

        view = result_json['Response']['View']
        if not view:
            raise CoordinateException("Error looking up address")

        coordinates = view[0]['Result'][0]['Location']['DisplayPosition']
        latitude = coordinates.get('Latitude')
        longitude = coordinates.get('Longitude')

        if not latitude or not longitude:
            raise CoordinateException("Error looking up address")

        return Coordinate(latitude, longitude)
