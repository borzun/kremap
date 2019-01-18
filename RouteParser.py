import Helper


class RouteParser(object):
    def __init__(self, direction_result=None):
        self.direction_result = direction_result
        if self.direction_result is None:
            raise ValueError(
                "ERROR: {} the input direction_result is incorrect!").format(type(self))

    def get_status(self):
        return Helper.get_status_code_from_response(self.direction_result)

    def get_duration(self):
        legs_list = Helper.get_value_from_dict_list("legs", self.direction_result)
        if legs_list is None:
            return None

        duration_dict = Helper.get_value_from_dict_list("duration", legs_list)
        if legs_list is None:
            return None

        return duration_dict.get("text", "None")

    def is_valid(self):
        status = self.get_status()
        return status == "OK"
