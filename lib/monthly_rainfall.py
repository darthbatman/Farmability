import requests
import json


# class GoogleMapsStaticAPIRequest(object):
#     def __init__(self, maptype, coordinate, zoom, size):
#         self.base_url = "https://maps.googleapis.com/maps/api/staticmap"
#         self.key = "AIzaSyAiQ0FVuhSohcRv9Vb_tnSWhqIYwvsiFhk"
#         self.maptype = maptype
#         self.coordinate = coordinate
#         self.zoom = zoom
#         self.size = size

#     def save_image(self, saved_image_path):
#         static_api_request = requests.get(
#             self.base_url + "?" +
#             "maptype" + "=" + self.maptype +
#             "&" + "center" + "=" +
#             str(self.coordinate[0]) + "," +
#             str(self.coordinate[1]) +
#             "&" + "zoom" + "=" + str(self.zoom) + "&" + "size" + "=" +
#             str(self.size[0]) + "x" + str(self.size[1]) +
#             "&" + "key" + "=" + self.key,
#             stream=True)
#         with open(saved_image_path, 'wb') as image_file:
#             static_api_request.raw.decode_content = True
#             shutil.copyfileobj(static_api_request.raw, image_file)


class NOAAWeatherAPIRequest(object):
    def __init__(self, min_latitude, min_longitude,
                 max_latitude, max_longitude):
        self.base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"
        self.token = "VKVbZaeexBHlGtqQjyHXSNEGHVfBzWuO"
        self.start_date = "2018-04-01"
        self.limit = "25"
        self.sort_field = "datacoverage"
        self.sort_order = "desc"
        self.min_latitude = str(min_latitude)
        self.min_longitude = str(min_longitude)
        self.max_latitude = str(max_latitude)
        self.max_longitude = str(max_longitude)

    def get_precipitation(self, latitude, longitude):
        min_latitude = latitude - 2
        min_longitude = longitude - 2
        max_latitude = latitude + 2
        max_longitude = longitude + 2

        rain_api_request = requests.get(
            self.base_url + "?" +
            "startdate" + "=" + self.maptype +
            "&" + "limit" + "=" +
            str(self.coordinate[0]) + "," +
            str(self.coordinate[1]) +
            "&" + "sortfield" + "=" + str(self.zoom) + "&" + "sortorder" + "=" +
            str(self.size[0]) + "extent" + str(self.size[1]) +
            "&" + "key" + "=" + self.key,
            headers={"token": self.token}, stream=True)


def weather(lat, lon):
    minLat = str(lat - 2)
    minLon = str(lon - 2)
    maxLat = str(lat + 2)
    maxLon = str(lon + 2)

    noaa_api_base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"

    url = noaa_api_base_url + "?startdate=2018-04-01&limit=25&sortfield=datacoverage&sortorder=desc&extent=" + minLat + "," + minLon + "," + maxLat + "," + maxLon
    api_token = "VKVbZaeexBHlGtqQjyHXSNEGHVfBzWuO"
    r = requests.get(url, headers={"token": api_token})
    response = json.loads(r.text)
    station = ''
    for i in range(0,len(response['results'])):
        st = response['results'][i]
        if(st['id'][0] == "G"):
            station = response['results'][i]
            break

    if (station == ''):
        return 4.65

    rainfall = {}
    for i in range(0,10):
        year = str(2009 + i)
        url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?stationid=" + station['id'] + "&datasetid=GSOM&units=standard&startdate=" + year + "-04-01&enddate=" + year + "-08-01&datatypeid=PRCP"
        r = requests.get(url, headers={ "token":"VKVbZaeexBHlGtqQjyHXSNEGHVfBzWuO" })
        response = json.loads(r.text)
        rainfall = {}
        if 'results' in response:
            data = response['results']
            rPerMonth = [None] * 5
            for j in range(0,5):
                rPerMonth[j] = data[j]['value']
            rainfall[2009+i] = rPerMonth
    total = 0
    num_months = 0
    for i in rainfall:
        for j in rainfall[i]:
            total += j
            num_months += 1
    if num_months == 0:
        return 4.65
    else:
        return total/num_months

if __name__ == "__main__":
    print(weather(40.1637926, -88.1760932))

    
