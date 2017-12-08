import googlemaps
import concurrent.futures
import DirectionRoute
import time


class DirectionFinder(object):

    def __init__(self, gmaps_client):
        self.gmaps_client = gmaps_client
        if self.gmaps_client is None:
            raise ValueError("ERROR: {} the input gmaps_client is incorrect!").format(type(self))

    def __get_duration_data_from_place(self, from_place, to_places, mode='driving'):
        results = {}

        time_now = time.time()

        print("Started finding duration data from place:{}".format(from_place))
        for to_place in to_places:
            direction_data = self.gmaps_client.directions(from_place, to_place, mode=mode, units='metric')
            route_parser = DirectionRoute.RouteParser(direction_data)
            results[to_place] = route_parser.get_duration()

        elapsed_time = time.time() - time_now
        print("Finished finding duration data from place:{} in: {} seconds".format(from_place, elapsed_time))

        return results

    def get_duration_data(self, from_places, to_places, mode):
        executor = concurrent.futures.ThreadPoolExecutor(len(from_places))

        print("started executing duration data getters")
        futures = {executor.submit(DirectionFinder.__get_duration_data_from_place, self, place, to_places, mode): place for place in from_places}

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
