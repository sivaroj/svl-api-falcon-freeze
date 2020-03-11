import requests
import collections
import json
import appPackage.MAP.readConf as ReadConf
from appPackage.MAP.convertTool import ConvertTool


def CalculateWayPoint(waypoint0,waypoint1,mode):
    m = ReadConf.ReadConf().here_map()
    PARAMS = {'apiKey': m['apiKey'], 'waypoint0': waypoint0, 'waypoint1': waypoint1, 'mode': mode, 'language': 'th_TH',
              'departure': 'now'}
    r = requests.get(url=m['routeURL'], params=PARAMS)
    route = r.json()
    distance = route['response']['route'][0]['summary']['distance']
    seconds = route['response']['route'][0]['summary']['travelTime']
    travel_time = ConvertTool.convertTimeFormat(seconds)
    data = collections.OrderedDict()
    data['waypoint0'] = waypoint0
    data['waypoint1'] = waypoint1
    data['mode'] = mode
    data['distance'] = distance
    data['travel_time'] = travel_time
    return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
    #return distance, travel_time
