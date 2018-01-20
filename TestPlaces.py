import GeoCode
import pprint


def run_tests(gmaps_client, places):
    for place in places:
        geocode_result = gmaps_client.geocode(place)
        pprint.pprint(geocode_result, depth=3)

        geocode = GeoCode.Parser(geocode_result)

        location = geocode.get_location()
        results = gmaps_client.places_nearby(location=location, rank_by='distance', language='RU', type='food')

        '''Another usage of places:
        gmaps_engine.places_nearby(self.location, keyword='foo',
                              language=self.language, min_price=1,
                              max_price=4, name='bar', open_now=True,
                              rank_by='distance', type=self.type) '''

        pprint.pprint(results, depth=7)
