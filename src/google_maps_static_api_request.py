import shutil
import requests


class GoogleMapsStaticAPIRequest(object):
    def __init__(self, maptype, coordinate, zoom, size):
        self.base_url = "https://maps.googleapis.com/maps/api/staticmap"
        self.key = "<API_KEY>"
        self.maptype = maptype
        self.coordinate = coordinate
        self.zoom = zoom
        self.size = size

    def save_image(self, saved_image_path):
        static_api_request = requests.get(
            self.base_url + "?" +
            "maptype" + "=" + self.maptype +
            "&" + "center" + "=" +
            str(self.coordinate[0]) + "," +
            str(self.coordinate[1]) +
            "&" + "zoom" + "=" + str(self.zoom) + "&" + "size" + "=" +
            str(self.size[0]) + "x" + str(self.size[1]) +
            "&" + "key" + "=" + self.key,
            stream=True)
        with open(saved_image_path, 'wb') as image_file:
            static_api_request.raw.decode_content = True
            shutil.copyfileobj(static_api_request.raw, image_file)