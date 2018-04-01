from pprint import pprint

class PlaceDetails(object):
    NAME_KEY = 'name'
    RATING_KEY = 'rating'
    REVIEWS_KEY = 'reviews'
    PLACE_ID_KEY = 'place_id'
    ADDRESS_ID_KEY = 'formatted_address'

    DISTANCE_ID_KEY = '__KREMAP_distance'

    def __init__(self, place_results):
        self.place_results = place_results["result"]
        if self.place_results is None:
            raise ValueError("Invalid place_results")

    def is_valid(self):
        '''
        Check whether place details are valid dict
        :return: True if there are valid results in
        '''
        return self.place_results is not None

    def is_valid_ratings(self):
        return self.get_rating() is not None and self.get_num_of_reviews() is not None

    def get_name(self):
        return self._get_key_value(self.NAME_KEY, absent_value="")

    def get_rating(self):
        return self._get_key_value(self.RATING_KEY, absent_value=0)

    def get_num_of_reviews(self):
        reviews = self._get_key_value(self.REVIEWS_KEY, absent_value=[])
        return len(reviews)

    def get_place_id(self):
        return self._get_key_value(self.PLACE_ID_KEY, absent_value="")

    def get_address(self):
        return self._get_key_value(self.ADDRESS_ID_KEY, absent_value="")

    def add_distance_value(self, distance):
        self.place_results[self.DISTANCE_ID_KEY] = distance

    def get_distance_value(self):
        return self._get_key_value(self.DISTANCE_ID_KEY, absent_value=0)

    def _get_key_value(self, key, absent_value=None):
        if not self.is_valid():
            return None

        if key in self.place_results:
            return self.place_results[key]

        return absent_value
