import Helper

class Parser(object):

    def __init__(self, geocode_result=None):
        self.geocode_result = geocode_result
        if self.geocode_result is None:
            raise ValueError("ERROR: {} the input geocode_result is incorrect!").format(type(self))

    def get_status(self):
        return Helper.get_status_code_from_response(self.geocode_result)

    def get_place_id(self):
        return Parser._get_value_from_geocode(self.geocode_result, "place_id")

    def is_valid(self):
        status = self.get_status()
        return status == "OK"

    def get_location(self):
        geometry_dict = Parser._get_value_from_geocode(self.geocode_result, "geometry")
        location_dict = geometry_dict['location']
        if ((location_dict is None) or ('lat' not in location_dict) or ('lng' not in location_dict)):
            return None

        return (location_dict['lat'], location_dict['lng'])

    @staticmethod
    def _get_value_from_geocode(geocode, value):
        for item in geocode:
            if value in item:
                return item.get(value, "")
