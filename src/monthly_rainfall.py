import requests
import json
from geopy.geocoders import Nominatim

def weather(lat, lon):
    minLat = str(lat - 2)
    minLon = str(lon - 2)
    maxLat = str(lat + 2)
    maxLon = str(lon + 2)

    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?startdate=2018-04-01&limit=25&sortfield=datacoverage&sortorder=desc&extent=" + minLat + "," + minLon + "," + maxLat + "," + maxLon
    r = requests.get(url, headers={ "token":"VKVbZaeexBHlGtqQjyHXSNEGHVfBzWuO" })
    response = json.loads(r.text)
    station = ''
    for i in range(0,len(response['results'])):
        st = response['results'][i]
        if(st['id'][0] == "G"):
            station = response['results'][i]
            break

    if (station == ''):
        return 4.65

    #url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets?stationid=" + station['id']
    #r = requests.get(url, headers={ "token":"VKVbZaeexBHlGtqQjyHXSNEGHVfBzWuO" })
    #response = json.loads(r.text)
    #print(response)
    #print(station['id'])
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
    print(weather(40.1637926,-88.1760932))

    
