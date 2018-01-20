import googlemaps
import time

import TestGeolocation
import TestDurationData
import TestPlaces

import schedule



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
                   'ЖК Manhattan, Київ, 02000']

    TestDurationData.run_tests(gmaps_engine, from_places)

    elapsed_time = time.time() - prev_time
    print("Total time in main() is:".format(elapsed_time))


def read_googlemaps_api_key():
    with open('googlemaps_key.dat', 'r', encoding='utf-8') as file:
        return file.readline()


def main_job(t):
    print("JOB_STARTED: {0}".format(t))
    app_key = read_googlemaps_api_key()
    main(app_key)
    print("JOB_FINISHED: {0}".format(t))
    return


# Run on specific times
times = ["07:00",
         "07:30",
         "08:00",
         "08:30",
         "09:00",
         "09:30",
         "10:00",
         "12:00",
         "14:00",
         "16:00",
         "17:30",
         "18:00",
         "18:30",
         "19:00",
         "19:30",
         "20:00"]
for str_time in times:
    schedule.every().day.at(str_time).do(main_job, str_time)

# Main loop for timed run:
while True:
    schedule.run_pending()
    time.sleep(60)
