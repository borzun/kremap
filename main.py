import googlemaps
import time
import TestDurationData


def main(app_key):

    prev_time = time.time()

    gmaps_engine = googlemaps.Client(key=app_key)
    if gmaps_engine:
        print("GMaps Engine is successfully created!")
    else:
        raise Exception("ERROR - can't create google maps engine!")

    from_places = ['time ЖК',
                   '5A, проспект Перемоги, 5А, Київ',
                   'Житловий комплекс "Славутич"',
                   'вулиця Глибочицька, 43, Київ',
                   'вулиця Євгена Сверстюка, 4, Київ',  # ЖК Галактика
                   'ЖК Метрополис',
                   'ЖК JackHouse']

    TestDurationData.run_tests(gmaps_engine, from_places)

    elapsed_time = time.time() - prev_time
    print("Total time in main() is:".format(elapsed_time))


def read_googlemaps_api_key():
    with open('googlemaps_key.dat', 'r', encoding='utf-8') as file:
        return file.readline()

app_key = read_googlemaps_api_key()
main(app_key)