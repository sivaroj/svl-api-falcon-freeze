import json
from appPackage.MAP import Nostra
from appPackage.MAP import Here_map
import collections
def convert_truck(t):
    v_truck_no = t
    prefix = t[:1]
    suffix = t[1:]
    if suffix.__len__() < 3:
        v_truck_no = prefix + '0' + suffix
    return v_truck_no
class DNTimestamp:

    def put_data(self, body):

        source_latlng = body['lat_lng']
        mode = 'fastest;truck;traffic:enabled'
        data = collections.OrderedDict(body)
        truck_no = convert_truck(body['truck_no'])
        truck_position = json.loads(Nostra.BusNow(truck_no).decode('utf-8'))
        truck_latlng = str(truck_position[0]['latitude']) + ',' + str(truck_position[0]['longitude'])
        distance = json.loads(Here_map.CalculateWayPoint(truck_latlng, source_latlng, mode).decode('utf-8'))
        far_from = {'distance': distance['distance'],'travel_time': distance['travel_time']}
        t = collections.OrderedDict()
        t = truck_position[0]
        t['far_from'] = far_from
        data['truck_position'] = t

        position_latlng = str(body['position']['latitude']) + ',' + str(body['position']['longitude'])
        # addr = json.loads(Here_map.ReverseGeoCoder(str(body['position']['latitude']),str(body['position']['longitude']),'10').decode('utf-8'))
        distance = json.loads(Here_map.CalculateWayPoint(position_latlng,source_latlng,mode).decode('utf-8'))
        position_far_from = {'distance': distance['distance'],'travel_time': distance['travel_time']}
        old_position = data['position']
        #old_position['address'] = addr['Address'][0]['label']
        old_position['far_from'] = position_far_from
        data['position'] = old_position

        return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
