
class RatingsSorter(object):
    # Places should contain only PlaceDetails objects
    def __init__(self, places_results):
        if places_results is None:
            raise ValueError("Incorrect places_results dict!")

        # sort by ratings:
        self.results = sorted(places_results, key=lambda x: x.get_rating(), reverse=True)

    def get_results(self):
        return self.results
