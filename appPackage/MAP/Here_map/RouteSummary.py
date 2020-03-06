import requests
import collections
import json
import appPackage.MAP.readConf as ReadConf
from appPackage.MAP import convertTool

def RouteSummary(origin, destination, transportMode):
    m = ReadConf.ReadConf().here_map()
    PARAMS = {'apiKey': m['apiKey'], 'origin': origin, 'destination': destination, 'transportMode': transportMode, 'return': 'summary'}
    r = requests.get(url=m['routeURLv8'], params=PARAMS)
    route = r.json()
    duration = route['routes'][0]['sections'][0]['summary']['duration']
    baseDuration = route['routes'][0]['sections'][0]['summary']['baseDuration']
    distance = route['routes'][0]['sections'][0]['summary']['length']
    data = collections.OrderedDict()
    data['origin'] = origin
    data['destination'] = destination
    data['transportMode'] = transportMode
    data['duration'] = convertTool.convertTimeFormat(duration)
    data['distance'] = distance/1000
    data['baseDuration'] = convertTool.convertTimeFormat(baseDuration)
    return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
    # return distance, travel_time
