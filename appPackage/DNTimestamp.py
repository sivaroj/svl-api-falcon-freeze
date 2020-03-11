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
        source_latlng = body['LAT_LNG']
        mode = 'fastest;truck;traffic:enabled'
        data = collections.OrderedDict(body)
        # ------------- TRUCK_POSITION --------------------------------------
        truck_no = convert_truck(body['TRUCK_NO'])
        truck_position = json.loads(Nostra.BusNow(truck_no).decode('utf-8'))
        truck_latlng = str(truck_position[0]['latitude']) + ',' + str(truck_position[0]['longitude'])
        distance = json.loads(Here_map.CalculateWayPoint(truck_latlng, source_latlng, mode).decode('utf-8'))
        far_from = {'distance': distance['distance'],'travel_time': distance['travel_time']}
        t = collections.OrderedDict()
        t = truck_position[0]
        t['far_from'] = far_from
        data['TRUCK_POSITION'] = t
        # ----------------- POSITION ---------------------------------------------
        position_latlng = str(body['POSITION']['latitude']) + ',' + str(body['POSITION']['longitude'])
        routeSummary = json.loads(Here_map.RouteSummary(origin=position_latlng,destination=source_latlng,transportMode='truck').decode('utf-8'))
        position_far_from = {'distance': routeSummary['distance'],'travel_time': routeSummary['duration']}
        old_position = data['POSITION']
        old_position['far_from'] = position_far_from
        data['POSITION'] = old_position
        # -----------------------INSERT TO POSTGRES-----------------------------------
        
        return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
