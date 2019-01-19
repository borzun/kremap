from kremap.gmaps_data_adapter import GMapsGeoCodeParser
from places.PlacesDistanceCalculator import PlacesDistanceCalculator
from places.PlacesFilterer import PlacesFilterer
from places.PlacesSearcher import PlacesSearcher
from places.RatingsSorter import RatingsSorter


def run_places_nearby(gmaps_client, places):
    for place in places:
        geocode_result = gmaps_client.geocode(place)
        geocode = GMapsGeoCodeParser(geocode_result)

        default_radius = 1000
        gyms = PlacesSearcher(gmaps_client, geocode).search_gyms_nearby(radius=500)
        all_gyms = _post_process_results(gmaps_client, place, gyms)

        # stores = PlacesSearcher(gmaps_client, geocode).search_grocery_stores_nearby(radius=500)
        # all_stores = _post_process_results(gmaps_client, place, stores)
        #
        # eating_places = PlacesSearcher(gmaps_client, geocode).search_eat_places_neasby(radius=500)
        # all_eating_places = _post_process_results(gmaps_client, place, eating_places)
        #
        # fun_places = PlacesSearcher(gmaps_client, geocode).search_fun_places_nearby(radius=500)
        # all_fun_places = _post_process_results(gmaps_client, place, fun_places)

        healthcare_places = PlacesSearcher(gmaps_client, geocode).search_healthcare_places_nearby(radius=500)
        all_healthcare_places = _post_process_results(gmaps_client, place, healthcare_places)

        print("-------- RESULTS[{0}] ------ ".format(place))
        print("----------- GYMS ------------ ")
        for result in all_gyms:
            print("name:{0}; ratings_num:{1}; ratings:{2}; distance:{3}".format(result.get_name(), result.get_num_of_reviews(), result.get_rating(), result.get_distance_value()))

        # print("----------- STORES ------------ ")
        # for result in all_stores:
        #     print("name:{0}; ratings_num:{1}; ratings:{2}; distance:{3}".format(result.get_name(), result.get_num_of_reviews(),
        #                                                           result.get_rating(), result.get_distance_value()))
        #
        # print("----------- EAT PLACES ------------ ")
        # for result in all_eating_places:
        #     print("name:{0}; ratings_num:{1}; ratings:{2}; distance:{3}".format(result.get_name(),
        #                                                                         result.get_num_of_reviews(),
        #                                                                         result.get_rating(),
        #                                                                         result.get_distance_value()))
        #
        # print("----------- FUN PLACES ------------ ")
        # for result in all_fun_places:
        #     print("name:{0}; ratings_num:{1}; ratings:{2}; distance:{3}".format(result.get_name(),
        #                                                                         result.get_num_of_reviews(),
        #                                                                         result.get_rating(),
        #                                                                         result.get_distance_value()))

        print("----------- HEALTHCARE PLACES ------------ ")
        for result in all_healthcare_places:
            print("name:{0}; ratings_num:{1}; ratings:{2}; distance:{3}".format(result.get_name(),
                                                                                result.get_num_of_reviews(),
                                                                                result.get_rating(),
                                                                                result.get_distance_value()))

        # average_rating = PlacesStatsCalculator(all_gyms).get_average_rating()
        # print("-------- GYMS_RATIO:[{0:.2f}]-----AVERAGE_RATING:[{1:.2f}] --------- ".format(filterer.get_results_ratio(), average_rating))
        [print() for _ in range(1, 3)]

def _post_process_results(gmaps_client, place, results):
    results = RatingsSorter(results).get_results()
    results = PlacesFilterer(results).get_results()
    PlacesDistanceCalculator(gmaps_client, place, results)

    return results


def run_tests(gmaps_client):
    # places = ['time ЖК',
    #           '5A, проспект Перемоги, 5А, Київ',
    #           'Житловий комплекс "Славутич"',
    #           'вулиця Глибочицька, 43, Київ',
    #           'вулиця Євгена Сверстюка, 4, Київ']

    # rent_places = ['Kyiv, Yordanska St, 32А',   # Obolon#1
    #                '''Kyiv, Marshala Malynovs'koho St, 11Б''',
    #                'Kyiv, Obolonska St, 25А']

    rent_places = ['вулиця Глибочицька, 43, Київ']

    # places = ['вулиця Кирилівська 15, Київ']
    run_places_nearby(gmaps_client, rent_places)




