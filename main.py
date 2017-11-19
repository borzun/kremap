import googlemaps
import pprint
import GeoCode
import WebGoogleMaps


gmaps_engine = googlemaps.Client(key='Enter your API!')
if gmaps_engine:
    print("GMaps Engine is successfully created!")
else:
    raise Exception("ERROR - can't create google maps engine!")

# Geocoding an address
geocode_result = gmaps_engine.geocode('Житловий комплекс "Славутич"')
pprint.pprint(geocode_result, depth=3)

geocode = GeoCode.Parser(geocode_result)
status = geocode.get_status()
place_id = geocode.get_place_id()
print("status:{0}; place_id:{1}".format(status, place_id))

WebGoogleMaps.open_with_place_id(place_id)