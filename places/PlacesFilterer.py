class PlacesFilterer(object):
    def __init__(self, places):
        self.results = [place for place in places if self._pass_filter(place)]
        self.results_ratio = len(self.results) / len(places) if len(places) > 0 else 0

    def get_results(self):
        return self.results

    def get_results_ratio(self):
        return self.results_ratio

    @staticmethod
    def _pass_filter(place):
        if place is None or place.is_valid_ratings() is False:
            return False

        return place.get_num_of_reviews() >= 5



