import requests
import collections
import json
import appPackage.MAP.readConf as ReadConf
from appPackage.MAP.convertTool import ConvertTool


def CalculateWayPoint(waypoint0,waypoint1,mode):
    m = ReadConf.ReadConf().here_map()
    if (waypoint0==',') or (waypoint0=='null') or (waypoint1==',') or waypoint1=='null':
        data = collections.OrderedDict()
        data['waypoint0'] = 0
        data['waypoint1'] = 0
        data['mode'] = mode
        data['distance'] = 0
        data['travel_time'] = 0
        return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
    else:
        PARAMS = {'apiKey': m['apiKey'], 'waypoint0': waypoint0, 'waypoint1': waypoint1, 'mode': mode, 'language': 'th_TH',
                  'departure': 'now'}
        # print('waypoint 0 {} waypoint 1 {}'.format(waypoint0,waypoint1))
        try:
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
        except: #
            data = collections.OrderedDict()
            data['waypoint0'] = 0
            data['waypoint1'] = 0
            data['mode'] = mode
            data['distance'] = 0
            data['travel_time'] = 0
            return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
    #return distance, travel_time
