import requests
import json


class Here_map:
    def __init__(self):
        apiKey = 'WAYtOD-5LCWn5ZhGhEgZUbB3Q84POzIXOJEmcArHqKc'
        reverseGeocodeURL = 'https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json'
        routeURL = 'https://route.ls.hereapi.com/routing/7.2/calculateroute.json'

    def ReverseGeoCoder(lat, lng, acc):
        if type(lat)==type(None) or lat == ',' or lat=='null' or type(lng)==type(None) or lng==',' or lng=='null':
            return json.dumps('{data: not found}')
        else:
            global apiKey
            # reverseGeocodeURL = 'https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json'
            global reverseGeocodeURL
            PARAMS = {'apiKey': apiKey, 'prox': lat + ',' + lng + ',' + acc, 'mode': 'retrieveAddresses'}
            r = requests.get(url=reverseGeocodeURL, params=PARAMS)
            data = r.json()
            return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')

