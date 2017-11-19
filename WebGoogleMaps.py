from WebBrowser import WebBrowser

def create_open_web_google_maps_URL(place_id):
    return "https://www.google.com/maps/place/?q=place_id:{}".format(place_id)

def open_with_place_id(place_id):
    if (place_id is None) or (isinstance(place_id, str) is False):
        raise ValueError("ERROR: {} is invalid place_id object!".format(place_id))

    browser = WebBrowser()
    url = create_open_web_google_maps_URL(place_id)
    return browser.open_url(url)
