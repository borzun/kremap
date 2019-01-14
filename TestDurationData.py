import Directions
import Helper
import json
import datetime
import time
import os
import errno


to_places_leisure = ['Багатофункціональний комплекс Gulliver',
                     'Океан Плаза, вулиця Антоновича, 176, Київ, 03150',
                     'Майдан Незалежності, Київ',
                     'Залізничний вокзал, Київ, 02000',
                     'Ботанічний сад ім. М. М. Гришка, вулиця Тимірязєвська, 4, Київ, 02000',
                     'ВДНГ Експоцентр, 03127, проспект Академіка Глушкова, 1, Київ',
                     'Площа Льва Толстого, Київ, 02000',
                     'Києво-Печерська лавра, Київ, 02000',
                     'Блокбастер, проспект Степана Бандери, 34В, Київ, 04655']

to_places_work = ['СофтСерв, вулиця Дегтярівська, 33В, Київ, 02000',
                  'SoftServe, б, вулиця Лейпцизька, 15, Київ',
                  'ТОВ "ГлобалЛоджик Україна", вулиця Миколи Грінченка, 2/1, Київ, 02000',
                  'Luxoft Ukraine, вулиця Радищева, 10/14, Київ, 02000',
                  'IT-Універ компанії Інфопульс, вулиця Польова, 24, Київ, 03056',
                  'вулиця Кирилівська, 39, Київ',
                  '(2I build.), Okhtyrskyi Ln, 7, Kiev, Kyiv city, 03680',
                  'Daxx IT Staffing Kiev, Куренівський провулок, 12, Киев, 04073',
                  'ELEKS, вулиця Антоновича, 172, Київ, 03150',
                  'Materialise Ukraine, вулиця Раїси Окіпної, 8, Київ, 02000']


# TODO: add to_places
def run_lviv_tests(gmaps_client):
    places = [" 79000, Pid Dubom Street, 26, Lviv, Lviv Oblast",            # Forum Appartments
              "ЖК Avalon",
              "Viacheslava Chornovola Ave, 69, L'viv, Lviv Oblast, 79000",  # ЖК Сіті
              "Semycvit",
              "ЖК Велика Британія",
              "ЖК Америка",
              "Naukova St, 5А, L'viv",                                      # ЖК Парус Смарт
              "вул. Червоної Калини, 60, Львів"]                            # ЖК Avalon Up

    run_tests(gmaps_client, places)


def run_kiev_tests(gmaps_client):
    from_places = ['time ЖК',
                   '5A, проспект Перемоги, 5А, Київ',
                   'Житловий комплекс "Славутич"',
                   'вулиця Глибочицька, 43, Київ',
                   'вулиця Євгена Сверстюка, 4, Київ']

    run_tests(gmaps_client, from_places)


def run_kiev_rent_duration_tests(gmaps_client):
    from_places = ['Mykhaila Lomonosova St, 54А Kyiv',
                   '51 Shchekavytska St Kyiv',
                   'Lukianivska St, 7А, 76, Kyiv',
                   "Obolons'kyi Ave, 9, Kyiv",
                   'Heroiv Stalinhradu Avenue, 17А, Kyiv']

    run_tests(gmaps_client, from_places)


def run_tests(gmaps_client, from_places):
    def sleeper(): return time.sleep(10)
    # Run tests for traffic driving:
    run_driving_with_traffic_tests(gmaps_client, from_places, sleeper)

    # Run tests for simple driving:
    # run_driving_tests(gmaps_client, from_places, sleeper)

    # Run tests for subway transit
    run_subway_transit_tests(gmaps_client, from_places, sleeper)

    # Run tests for simple transit
    run_transit_tests(gmaps_client, from_places, sleeper)


def run_driving_with_traffic_tests(gmaps_client, from_places, after_test_executor):
    driving_with_traffic = {}
    driving_with_traffic["departure_time"] = datetime.datetime.now()
    driving_with_traffic["traffic_model"] = "best_guess"
    __perform_duration_step_test(gmaps_client, from_places, to_places_leisure,
                                 'driving', "traffic_leisure", driving_with_traffic)
    after_test_executor()
    __perform_duration_step_test(gmaps_client, from_places, to_places_work,
                                 'driving', "traffic_work", driving_with_traffic)
    after_test_executor()


def run_driving_tests(gmaps_client, from_places, after_test_executor):
    __perform_duration_step_test(gmaps_client, from_places,
                                 to_places_leisure, 'driving', "leisure")
    after_test_executor()
    __perform_duration_step_test(gmaps_client, from_places, to_places_work, 'driving', "work")
    after_test_executor()


def run_subway_transit_tests(gmaps_client, from_places, after_test_executor):
    subway_transit_params = {}
    subway_transit_params["transit_mode"] = "subway"
    subway_transit_params["transit_routing_preference"] = "fewer_transfers"
    __perform_duration_step_test(gmaps_client, from_places, to_places_leisure,
                                 'transit', "subway_leisure", subway_transit_params)
    after_test_executor()
    __perform_duration_step_test(gmaps_client, from_places, to_places_work,
                                 'transit', "subway_work", subway_transit_params)
    after_test_executor()


def run_transit_tests(gmaps_client, from_places, after_test_executor):
    __perform_duration_step_test(gmaps_client, from_places,
                                 to_places_leisure, 'transit', "leisure")
    after_test_executor()
    __perform_duration_step_test(gmaps_client, from_places, to_places_work, 'transit', "work")
    after_test_executor()


def __perform_duration_step_test(gmaps_client, from_places, to_places, mode, suffix, additional_params=None):
    print("{}_STARTED TestDurationData:{}_{}".format(datetime.datetime.now(), mode, suffix))
    finder = Directions.DirectionFinder(gmaps_client)
    duration_data = finder.get_duration_data(
        from_places, to_places, mode=mode, additional_params=additional_params)
    __save_duration_dict_to_json(duration_data, mode, suffix)
    print("{}_FINISHED TestDurationData:{}_{}".format(datetime.datetime.now(), mode, suffix))


def __save_duration_dict_to_json(duration_data, mode, suffix):
    # Ensure that folder is properly created:
    curr_datetime = datetime.datetime.now()
    day_month_str = curr_datetime.strftime("%d_%m")

    result_format_dir = "C:\\Temp\\{}\\{}\\{}"
    curr_dir = result_format_dir.format(day_month_str, mode, suffix)

    try:
        if not os.path.exists(curr_dir):
            os.makedirs(curr_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("ERROR - can't create dir[{}] - something bad happens:{}".format(curr_dir, e))
        else:
            print(
                "ERROR - while creating a dir[{}] - something bad happened:{}".format(curr_dir, e))

    date_str = curr_datetime.strftime("%H-%M")
    file_name = "{}\\{}.json".format(curr_dir, date_str)
    with open(file_name, "w", encoding='utf-8') as file:
        json.dump(duration_data, file, indent=4, ensure_ascii=False)

    best_places = {}
    for key, value in duration_data.items():
        average = Helper.mean([Helper.convert_to_minutes(time_value)
                               for time_value in value.values()])
        best_places[key] = average

    sorted_places = sorted(best_places.items(), key=lambda x: x[1])
    with open(file_name, "a", encoding='utf-8') as file:
        file.write("\n" * 3 + "-" * 50 + "SUMMARY" + "-" * 50 + "\n" * 3)
        for tuple_value in sorted_places:
            formatted_tuple_value = (tuple_value[0], "{0:.2f}".format(tuple_value[1]))
            file.write(str(formatted_tuple_value) + "\n")
