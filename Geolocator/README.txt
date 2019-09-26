README

This service can be initialized by creating a virtualenv and installing flask.
Then the main `app.py` can be run in python

$ virtualenv flask
$ flask/bin/pip install flask
$ python app.py

The server starts on http://localhost:5000 by default


CREDENTIALS
You will need to add API credentials for Google and Here in the credentials.txt
file. Google's API does not need an api_id, but Here's API does. 


API DOCUMENTATION
The API accepts an address as a parameter to the GET endpoint `/credentials`, and
returns a set of coordinates, latitude and longitude, in JSON.

The API will attempt to query the Google Geocoding service first, and then
will try the Here service if that fails. If both fail, an error will be returned.

Example URL to query endpoint:
http://localhost:5000/coordinates/575+Shotwell+st+san+francisco