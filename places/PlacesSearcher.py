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
    def search_gyms_nearby(self, radius=1500):
        return self._search_places_impl(['gym'], ['Sports Complex'], radius)

    # TODO: need to add caching here!
    def search_grocery_stores_nearby(self, radius=1000):
        return self._search_places_impl(['supermarket', 'shopping_mall'], ['Продукты'], radius)

    def search_eat_places_neasby(self, radius=1000):
        return self._search_places_impl(types=['bar', 'cafe', 'restaurant'], keywords=[], radius=radius)

    def search_fun_places_nearby(self, radius=1500):
        return self._search_places_impl(types=['amusement_park', 'bowling_alley', 'movie_theater', 'shopping_mall'], keywords=[], radius=radius)

    def search_healthcare_places_nearby(self, radius=2000):
        return self._search_places_impl(types=['dentist', 'doctor', 'hospital'], keywords=[], radius=radius)

    def _create_place_details_list(self, gmaps_places):
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

    def _search_places_impl(self, types: list, keywords: list, radius) -> "list of places":
        location = self.place.get_location()

        all_places = []

        # Find all places by types:
        for t in types:
            type_places = self.gmaps_client.places_nearby(location=location,
                                                          language='RU',
                                                          type=t,
                                                          radius=radius)
            type_places = self._create_place_details_list(type_places)
            all_places = all_places + type_places

        # Find all places by specific keywords:
        for key in keywords:
            keyword_places = self.gmaps_client.places_nearby(location=location,
                                                             language='RU',
                                                             keyword=key,
                                                             radius=radius)
            keyword_places = self._create_place_details_list(keyword_places)
            all_places = all_places + keyword_places

        return list(OrderedDict.fromkeys(all_places))

