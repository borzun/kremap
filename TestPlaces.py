import GeoCode
from places.RatingsSorter import RatingsSorter
from places.PlacesSearcher import PlacesSearcher
from places.PlacesFilterer import PlacesFilterer
from places.PlacesStatsCalculator import PlacesStatsCalculator


def run_places_nearby(gmaps_client, places):
    for place in places:
        geocode_result = gmaps_client.geocode(place)
        geocode = GeoCode.Parser(geocode_result)

        gyms = PlacesSearcher(gmaps_client, geocode).search_gyms_nearby(radius=500)
        gyms = RatingsSorter(gyms).get_results()
        filterer = PlacesFilterer(gyms)

        all_gyms = filterer.get_results()
        print("-------- RESULTS[{0}] ------ ".format(place))
        for result in all_gyms:
            print("name:{0}; ratings_num:{1}; ratings:{2}".format(result.get_name(), result.get_num_of_reviews(), result.get_rating()))

        average_rating = PlacesStatsCalculator(all_gyms).get_average_rating()
        print("-------- RATIO:[{0:.2f}]-----AVERAGE_RATING:[{1:.2f}] --------- ".format(filterer.get_results_ratio(), average_rating))
        [print() for _ in range(1, 3)]


def run_tests(gmaps_client):
    places = ['time ЖК',
              '5A, проспект Перемоги, 5А, Київ',
              'Житловий комплекс "Славутич"',
              'вулиця Г        либочицька, 43, Київ',
              'вулиця Євгена Сверстюка, 4, Київ']

    run_places_nearby(gmaps_client, places)

