import googlemaps
import concurrent.futures
import DirectionRoute
import time


class DirectionFinder(object):

    def __init__(self, gmaps_client):
        self.gmaps_client = gmaps_client
        if self.gmaps_client is None:
            raise ValueError("ERROR: {} the input gmaps_client is incorrect!").format(type(self))

    def __get_duration_data_from_place(self, from_place, to_places, mode='driving', additional_params=None):
        results = {}

        time_now = time.time()

        departure_time = None
        transit_mode = None
        transit_routing_preference = None
        traffic_model = None

        if additional_params is not None:
            if "departure_time" in additional_params:
                departure_time = additional_params["departure_time"]
            if "transit_mode" in additional_params:
                transit_mode = additional_params["transit_mode"]
            if "transit_routing_preference" in additional_params:
                transit_routing_preference = additional_params["transit_routing_preference"]
            if "traffic_model" in additional_params:
                traffic_model = additional_params["traffic_model"]

        print("Started finding duration data from place:{}".format(from_place))
        for to_place in to_places:
            direction_data = self.gmaps_client.directions(from_place,
                                                          to_place,
                                                          mode=mode,
                                                          units='metric',
                                                          departure_time=departure_time,
                                                          transit_mode=transit_mode,
                                                          transit_routing_preference=transit_routing_preference,
                                                          traffic_model=traffic_model)
            route_parser = DirectionRoute.RouteParser(direction_data)
            results[to_place] = route_parser.get_duration()

        elapsed_time = time.time() - time_now
        print("Finished finding duration data from place:{} in: {} seconds".format(from_place, elapsed_time))

        return results

    def get_duration_data(self, from_places, to_places, mode, additional_params=None):
        executor = concurrent.futures.ThreadPoolExecutor(len(from_places))
        futures = {executor.submit(DirectionFinder.__get_duration_data_from_place, self, place, to_places, mode, additional_params): place for place in from_places}

        results = {}
        try:
            for future in concurrent.futures.as_completed(futures, timeout=15):
                place = futures[future]
                try:
                    duration_data = future.result()
                except Exception as exc:
                    print("ERROR - can't get data from place at:{} with exc:{}".format(place, exc))
                    return None
                else:
                    results[place] = duration_data
        except TimeoutError:
            print("ERROR - timeout error is happened while executing Futures!")
            return None

        return results
