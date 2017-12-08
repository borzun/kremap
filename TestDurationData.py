import Directions
import Helper
import json
import datetime
import time


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
                  'Ciklum, вулиця Миколи Амосова, 12, Київ, 03680',
                  'Daxx IT Staffing Kiev, Куренівський провулок, 12, Киев, 04073',
                  'ELEKS, вулиця Антоновича, 172, Київ, 03150',
                  'Materialise Ukraine, вулиця Раїси Окіпної, 8, Київ, 02000']

json_format_file = "C:\\Temp\\data_results_{}_{}_{}.json"


def run_tests(gmaps_client, from_places):
    __perform_duration_step_test(gmaps_client, from_places, to_places_leisure, 'driving', "leisure")
    time.sleep(10)
    __perform_duration_step_test(gmaps_client, from_places, to_places_leisure, 'transit', "leisure")
    time.sleep(10)

    __perform_duration_step_test(gmaps_client, from_places, to_places_work, 'driving', "work")
    time.sleep(10)
    __perform_duration_step_test(gmaps_client, from_places, to_places_work, 'transit', "work")
    time.sleep(10)


def __perform_duration_step_test(gmaps_client, from_places, to_places, mode, suffix):
    print("Started duration test with params:{}_{}".format(mode, suffix))
    finder = Directions.DirectionFinder(gmaps_client)
    duration_data = finder.get_duration_data(from_places, to_places, mode=mode)
    __save_duration_dict_to_json(duration_data, mode, suffix)
    print("Finished duration test with params:{}_{}".format(mode, suffix))


def __save_duration_dict_to_json(duration_data, mode, suffix):
    curr_datetime = datetime.datetime.now()
    date_str = curr_datetime.strftime("%d.%m_%H-%M")
    file_name = json_format_file.format(suffix, mode, date_str)
    with open(file_name, "w", encoding='utf-8') as file:
        json.dump(duration_data, file, indent=4, ensure_ascii=False)

    best_places = {}
    for key, value in duration_data.items():
        average = Helper.mean([Helper.convert_to_minutes(time_value) for time_value in value.values()])
        best_places[key] = average

    sorted_places = sorted(best_places.items(), key=lambda x: x[1])
    with open(file_name, "a", encoding='utf-8') as file:
        file.write("\n" * 3 + "-" * 50 + "SUMMARY" + "-" * 50 + "\n" * 3)
        for tuple_value in sorted_places:
            formatted_tuple_value = (tuple_value[0], "{0:.2f}".format(tuple_value[1]))
            file.write(str(formatted_tuple_value) + "\n")
