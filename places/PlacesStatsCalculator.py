class PlacesStatsCalculator(object):

    def __init__(self, places):
        self.places = places

    def get_average_rating(self):
        average = 0.
        if len(self.places) > 0:
            for place in self.places:
                average += place.get_rating()

            return average / len(self.places)

        return average
