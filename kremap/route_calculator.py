import concurrent.futures

from _internal import durations


def calculate_duration_data(gmaps_client, from_places, to_places, mode, additional_params=None):
    if gmaps_client is None:
        raise ValueError("ERROR: {} the input gmaps_client is incorrect!").format(calculate_duration_data.__name__)

    executor = concurrent.futures.ThreadPoolExecutor(len(from_places))
    futures = {executor.submit(durations.calculate_duration_data_from_place, gmaps_client,
                               place, to_places, mode, additional_params): place for place
               in from_places}

    results = {}
    try:
        for future in concurrent.futures.as_completed(futures, timeout=60):
            place = futures[future]
            try:
                duration_data = future.result()
            except Exception as exc:
                print("ERROR - can't get data from place at:{} with exc:{}".format(place,
                                                                                   exc))
                return None
            else:
                results[place] = duration_data
    except TimeoutError as exc:
        print("ERROR - timeout error for place: {} with exc:{}!".format(from_places, exc))
        return None

    return results
