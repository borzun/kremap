from Directions import DirectionFinder


class PlacesDistanceCalculator(object):
    def __init__(self, gmaps_client, origin_place, places):
        self.finder = DirectionFinder(gmaps_client)
        for place in places:
            self._calculate_distance(origin_place, place)

    def _calculate_distance(self, origin_place, place):
        duration = self.finder.get_duration_data([origin_place], [place.get_address()], mode='walking')
        place.add_distance_value(duration)



