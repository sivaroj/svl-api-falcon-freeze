import requests
import collections
import json
import appPackage.MAP.readConf as ReadConf
from appPackage.MAP.convertTool import ConvertTool

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
    data['duration'] = ConvertTool.convertTimeFormat(duration)
    data['distance'] = distance
    data['baseDuration'] = ConvertTool.convertTimeFormat(baseDuration)
    return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
    # return distance m, travel_time hh:mm:ss
