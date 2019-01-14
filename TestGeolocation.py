import pprint
import GeoCode
import DirectionRoute
import WebGoogleMaps


def run_tests(gmaps_client, location):
    print("<------ GeoCode_{}_STARTED ------> ".format(location))
    # Geocoding an address
    geocode_result = gmaps_client.geocode(location)
    if geocode_result is None:
        print("     ----- GeoCode_{}_FAILED: geocode_result is None ----->".format(location))
    else:
        print("     ----- GeoCode_{}_SUCCESS ----->".format(location))

    geocode = GeoCode.Parser(geocode_result)
    status = geocode.get_status()
    place_id = geocode.get_place_id()
    print(
        "     ------ GeoCode_{0}_Data: status:{1}; place_id:{2} ------ ".format(location, status, place_id))

    WebGoogleMaps.open_with_place_id(place_id)
