import requests
import appPackage.MAP.readConf as ReadConf
import collections
import json


def ReverseGeoCoder(lat, lng, acc):
    m = ReadConf.ReadConf().here_map()
    PARAMS = {'apiKey': m['apiKey'], 'prox': lat+','+lng+','+acc, 'mode': 'retrieveAddresses'}
    r = requests.get(url=m['reverseGeocodeURL'], params=PARAMS)
    addr = r.json()

    address = []
    for d in addr['Response']['View'][0]['Result']:
        t = collections.OrderedDict()
        t['distance'] = d['Distance']
        t['label'] = d['Location']['Address']['Label']
        address.append(t)
    geolocation = collections.OrderedDict()
    geolocation['Latitude'] = lat
    geolocation['Longitude'] = lng
    geolocation['Acc'] = acc
    geolocation['Address'] = address
    return json.dumps(geolocation, indent=" ", ensure_ascii=False).encode('utf-8')
    #return data['Response']['View'][0]['Result'][0]['Location']['Address']['Label']
    #return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')

