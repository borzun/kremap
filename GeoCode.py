class Parser(object):

    def __init__(self, geocode_result=None):
        self.geocode_result = geocode_result
        if self.geocode_result is None:
            raise ValueError("ERROR: {} the input geocode_result is incorrect!").format(type(self))

        self.geocode_result = geocode_result

    def get_status(self):
        return Parser._get_value_from_geocode(self.geocode_result, "status")

    def get_place_id(self):
        return Parser._get_value_from_geocode(self.geocode_result, "place_id")

    def is_valid(self):
        status = self.get_status()
        return status == "OK"

    @staticmethod
    def _get_value_from_geocode(geocode, value):
        for item in geocode:
            if value in item:
                return item.get(value, "")
