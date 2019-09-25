import unittest

from Geolocator import GoogleCoordinatesService, HereCoordinatesService


class TestGoogleCoordinatesService(unittest.TestCase):
    
    example_json = {
       "results" : [
          {
             "address_components" : [
                {
                   "long_name" : "1600",
                   "short_name" : "1600",
                   "types" : [ "street_number" ]
                },
                {
                   "long_name" : "Amphitheatre Parkway",
                   "short_name" : "Amphitheatre Pkwy",
                   "types" : [ "route" ]
                },
                {
                   "long_name" : "Mountain View",
                   "short_name" : "Mountain View",
                   "types" : [ "locality", "political" ]
                },
                {
                   "long_name" : "Santa Clara County",
                   "short_name" : "Santa Clara County",
                   "types" : [ "administrative_area_level_2", "political" ]
                },
                {
                   "long_name" : "California",
                   "short_name" : "CA",
                   "types" : [ "administrative_area_level_1", "political" ]
                },
                {
                   "long_name" : "United States",
                   "short_name" : "US",
                   "types" : [ "country", "political" ]
                },
                {
                   "long_name" : "94043",
                   "short_name" : "94043",
                   "types" : [ "postal_code" ]
                }
             ],
             "formatted_address" : "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
             "geometry" : {
                "location" : {
                   "lat" : 37.4267861,
                   "lng" : -122.0806032
                },
                "location_type" : "ROOFTOP",
                "viewport" : {
                   "northeast" : {
                      "lat" : 37.4281350802915,
                      "lng" : -122.0792542197085
                   },
                   "southwest" : {
                      "lat" : 37.4254371197085,
                      "lng" : -122.0819521802915
                   }
                }
             },
             "place_id" : "ChIJtYuu0V25j4ARwu5e4wwRYgE",
             "plus_code" : {
                "compound_code" : "CWC8+R3 Mountain View, California, United States",
                "global_code" : "849VCWC8+R3"
             },
             "types" : [ "street_address" ]
          }
       ],
       "status" : "OK"
    }

    def test_parse_results(self):
        google_coord_svc = GoogleCoordinatesService()
        result = google_coord_svc.parse_results(self.example_json)

        self.assertIsNotNone(result)
        self.assertEqual(result.latitude, 37.4267861)
        self.assertEqual(result.longitude, -122.0806032)

    
class TestHereCoordinatesService(unittest.TestCase):
   
    example_json = {
        "Response": {
          "MetaInfo": {"Timestamp": "2016-11-02T13:24:11.575+0000"},
          "View": [{
            "_type": "SearchResultsViewType",
            "ViewId": 0,
            "Result": [{
              "Relevance": 1,
              "MatchLevel": "houseNumber",
              "MatchQuality": {
                "City": 1,
                "Street": [0.9],
                "HouseNumber": 1
              },
              "MatchType": "pointAddress",
              "Location": {
                "LocationId": "NT_Opil2LPZVRLZjlWNLJQuWB_0ITN",
                "LocationType": "point",
                "DisplayPosition": {
                  "Latitude": 41.88432,
                  "Longitude": -87.6387699
                },
                "NavigationPosition": [{
                  "Latitude": 41.88449,
                  "Longitude": -87.6387699
                }],
                "MapView": {
                  "TopLeft": {
                    "Latitude": 41.8854442,
                    "Longitude": -87.6402799
                  },
                  "BottomRight": {
                    "Latitude": 41.8831958,
                    "Longitude": -87.6372599
                  }
                },
                "Address": {
                  "Label": "425 W Randolph St, Chicago, IL 60606, United States",
                  "Country": "USA",
                  "State": "IL",
                  "County": "Cook",
                  "City": "Chicago",
                  "District": "West Loop",
                  "Street": "W Randolph St",
                  "HouseNumber": "425",
                  "PostalCode": "60606",
                  "AdditionalData": [
                    {
                      "value": "United States",
                      "key": "CountryName"
                    },
                    {
                      "value": "Illinois",
                      "key": "StateName"
                    },
                    {
                      "value": "Cook",
                      "key": "CountyName"
                    },
                    {
                      "value": "N",
                      "key": "PostalCodeType"
                    }
                  ]
                }
              }
            }]
          }]
        }}

    def test_parse_results(self):
        here_coord_svc = HereCoordinatesService()
        result = here_coord_svc.parse_results(self.example_json)

        self.assertIsNotNone(result)
        self.assertEqual(result.latitude, 41.88432)
        self.assertEqual(result.longitude, -87.6387699)

if __name__ == '__main__':
    unittest.main()