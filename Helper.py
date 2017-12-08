import re


def get_status_code_from_response(response_message, default_value="OK"):
    for item in response_message:
        if "status" in item:
            return item.get("status", None)

    return default_value


def get_value_from_dict_list(key, dict_list):
    for item in dict_list:
        if key in item:
            return item.get(key, None)


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def convert_to_minutes(time_str):
    hours_match = re.search(r"(\d+) \b(hour|hours)\b", time_str)

    hours = 0 if hours_match is None else int(hours_match.group(1))

    mins_match = re.search(r"(\d+) \bmins\b", time_str)
    minutes = 0 if mins_match is None else int(mins_match.group(1))

    return hours * 60 + minutes
