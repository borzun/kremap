from RouteCalculator import RouteCalculator


class PlacesDistanceCalculator(object):
    def __init__(self, gmaps_client, origin_place, places):
        self.finder = RouteCalculator(gmaps_client)
        for place in places:
            self._calculate_distance(origin_place, place)

    def _calculate_distance(self, origin_place, place):
        duration_data = self.finder.get_duration_data(
            [origin_place], [place.get_address()], mode='walking')
        if duration_data:
            if origin_place in duration_data:
                duration_pair = duration_data[origin_place]
                if place.get_address() in duration_pair:
                    duration_value = duration_pair[place.get_address()]
                    place.add_distance_value(duration_value)
                    return
