import pprint
import GeoCode
import DirectionRoute
import WebGoogleMaps


def run_tests(gmaps_client, location):
    # Geocoding an address
    geocode_result = gmaps_client.geocode(location)
    pprint.pprint(geocode_result, depth=3)

    geocode = GeoCode.Parser(geocode_result)
    status = geocode.get_status()
    place_id = geocode.get_place_id()
    print("------ GeoCode test: status:{0}; place_id:{1} ------ ".format(status, place_id))

    direction_output = gmaps_client.directions('Житловий комплекс "Славутич"', 'Paris', mode='driving', units='metric')
    pprint.pprint(direction_output, depth=7)

    direction_route = DirectionRoute.RouteParser(direction_output)
    status = direction_route.get_status()
    duration = direction_route.get_duration()
    print("------ DirectionRoute test: status:{0}; duration:{1} ------ ".format(status, duration))

    'WebGoogleMaps.open_with_place_id(place_id)'