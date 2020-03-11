import collections
import json
import requests
import appPackage.MAP.readConf as ReadConf
from appPackage.MAP import Here_map
from appPackage.MAP.convertTool import ConvertTool


def BusNow(vehicleList):
    conf = ReadConf.ReadConf().Nostra_map()
    url = conf['apiURL']+'/busnow'
    headers={'Content-Type': 'application/json'}
    body = {"token": conf['token'], "vehicleList": vehicleList}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    print(r.text)
    vehicles = json.loads(r.text)['bus']
    data = []
    for vehicle in vehicles:
        truck_position = collections.OrderedDict()
        truck_addr = json.loads(Here_map.ReverseGeoCoder(str(vehicle['latitude']), str(vehicle['longitude']), '2').decode('utf-8'))
        addr = truck_addr['Address'][0]['label']
        truck_position['vehicle'] = vehicle['vehicleName']
        truck_position['datetime'] = ConvertTool.tzToStr(vehicle['dateTime'])
        truck_position['speed'] = vehicle['speed']
        truck_position['heading'] = vehicle['direction']
        truck_position['latitude'] = vehicle['latitude']
        truck_position['longitude'] = vehicle['longitude']
        truck_position['address'] = addr
        truck_position['engine'] = vehicle['evEngine']
        data.append(truck_position)
    return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
