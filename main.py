import googlemaps
import time

import TestDurationData
import schedule


def main(app_key):
    prev_time = time.time()
    gmaps_engine = googlemaps.Client(key=app_key)

    if gmaps_engine:
        print("GMaps Engine is successfully created!")
    else:
        raise Exception("ERROR - can't create google maps engine!")

    TestDurationData.run_kiev_tests(gmaps_engine)
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

times_workday = [
         "08:00",
         "09:00",
         "10:00",
         "13:00",
         "18:00",
         "19:00",
         "20:00"]

for str_time in times_workday:
    schedule.every().day.at(str_time).do(main_job, str_time)

# Main loop for timed run:
while True:
    schedule.run_pending()
    time.sleep(60)
