from places.PlaceDetails import PlaceDetails
from collections import OrderedDict

from itertools import chain
from pprint import pprint


class PlacesSearcher(object):
    PLACE_ID_KEY = "place_id"

    def __init__(self, gmaps_client, place):
        self.place = place
        self.gmaps_client = gmaps_client

    #TODO: need to add caching here!
    def search_gyms_nearby(self, radius=1000):
        location = self.place.get_location()

        # Find Sports Complexes
        gmaps_sport_complexes = self.gmaps_client.places_nearby(location=location,
                                                                language='RU',
                                                                keyword='Sports Complex',
                                                                radius=radius)
        sport_complexes = self.create_place_details_list(gmaps_sport_complexes)

        # Find gyms
        gmaps_gyms = self.gmaps_client.places_nearby(location=location,
                                                     language='RU',
                                                     type='gym',
                                                     radius=radius)
        gyms = self.create_place_details_list(gmaps_gyms)


        # Combine both sport complexes and gyms
        all_gyms = sport_complexes + gyms

        return list(OrderedDict.fromkeys(all_gyms))

    def create_place_details_list(self, gmaps_places):
        place_details = []

        if "results" in gmaps_places:
            place_results = gmaps_places["results"]

            for place in place_results:
                if "place_id" in place:
                    place_id = place[self.PLACE_ID_KEY]

                    gmaps_place_details = self.gmaps_client.place(place_id)
                    try:
                        details = PlaceDetails(gmaps_place_details)
                        place_details.append(details)
                    except ValueError as err:
                        print("ERROR: Incorrect PlaceDetails error: {0} for place_id: {1}!".format(err, place_id))

        return place_details
