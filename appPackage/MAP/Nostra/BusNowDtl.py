import cx_Oracle
import collections
import json
import requests
import appPackage.MAP.readConf as ReadConf
from appPackage.MAP import Here_map
from appPackage.MAP.convertTool import ConvertTool
from appPackage.readConf import ReadConf as ora_conf

def BusNowDtl(vehicleList):
    conf = ReadConf.ReadConf().Nostra_map()
    url = conf['apiURL']+'/busnow'
    headers={'Content-Type': 'application/json'}
    body = {"token": conf['token'], "vehicleList": vehicleList}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    vehicles = json.loads(r.text)['bus']
    ora = ora_conf().ora()
    try:
        dsn_tns = cx_Oracle.makedsn(ora['server'], ora['port'], ora['service'])
        ora_conn = cx_Oracle.connect(ora['user'], ora['password'], dsn_tns
                                     , encoding="UTF-8")
        ora_cursor = ora_conn.cursor()
        ora_qryStr = ora_conf().qryBusNowDtl()['Query']

        data = []
        for vehicle in vehicles:
            truck_position = collections.OrderedDict()
            truck_addr = json.loads(Here_map.ReverseGeoCoder(str(vehicle['latitude']), str(vehicle['longitude']), '2').decode('utf-8'))
            parameter = {'truck_no': vehicle['vehicleName']}
            # print(vehicle)
            ora_cursor.execute(ora_qryStr,parameter)
            for row in ora_cursor:
                addr = truck_addr['Address'][0]['label']
                truck_position['vehicle'] = vehicle['vehicleName']
                truck_position['datetime'] = ConvertTool.tzToStr(vehicle['dateTime'])
                truck_position['speed'] = vehicle['speed']
                truck_position['heading'] = vehicle['direction']
                truck_position['latitude'] = vehicle['latitude']
                truck_position['longitude'] = vehicle['longitude']
                truck_position['address'] = addr
                truck_position['engine'] = vehicle['evEngine']
                truck_position['dn_no'] = row[0]
                truck_position['emp_no'] = row[1]
                truck_position['emp_name'] = row[2]
                truck_position['tel'] = row[3]
                data.append(truck_position)
        ora_cursor.close()
        return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
    except cx_Oracle.DatabaseError as e:
        data['error'] = e.args[0].message
        return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')

    finally:
        if ora_conn is not None:
            ora_conn.close()