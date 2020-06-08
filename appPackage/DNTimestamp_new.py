import json
from appPackage.MAP import Nostra
from appPackage.MAP import Here_map
import collections
import psycopg2
from appPackage.readConf import ReadConf
from appPackage.login_Postgres import Login_Postgres
import arrow
import time

def convert_truck(t):
    v_truck_no = t
    prefix = t[:1]
    suffix = t[1:]
    if suffix.__len__() < 3:
        v_truck_no = prefix + '0' + suffix
    return v_truck_no


class DNTimestamp_new:

    def put_data(self, user, password, body):
        source_latlng = body['LAT_LNG']
        mode = 'fastest;truck;traffic:enabled'
        data = collections.OrderedDict(body)

        # ------------- TRUCK_POSITION --------------------------------------
        truck_no = convert_truck(body['TRUCK_NO'])
        truck_position = json.loads(Nostra.BusNow(truck_no).decode('utf-8'))
        # print('truck_no {} position {} '.format(truck_no,truck_position))
        truck_latlng = str(truck_position[0]['latitude']) + ',' + str(truck_position[0]['longitude'])
        # print('source {} dest {}'.format(source_latlng,truck_latlng))
        try:
            distance = json.loads(Here_map.CalculateWayPoint(truck_latlng, source_latlng, mode).decode('utf-8'))
            far_from = {'distance': distance['distance'],'travel_time': distance['travel_time']}
        except: #
            far_from = {'distance': 0, 'travel_time': 0}

        t = collections.OrderedDict()
        t = truck_position[0]
        t['far_from'] = far_from
        data['TRUCK_POSITION'] = t
        # ----------------- MOBILE POSITION ---------------------------------------------
        old_position = data['POSITION']
        source_latlng = data['LAT_LNG']
        dt = arrow.now
        position_latlng = str(old_position['latitude'])+','+str(old_position['longitude'])
        distance = json.loads(Here_map.CalculateWayPoint(position_latlng, source_latlng, mode).decode('utf-8'))
        position_far_from = {'distance': distance['distance'],'travel_time': distance['travel_time']}
        old_position['timestamp'] = time.time()
        old_position['far_from'] = position_far_from
        mobile_addr = json.loads(
            Here_map.ReverseGeoCoder(str(old_position['latitude']), str(old_position['longitude']), '1').decode('utf-8'))
        ts = arrow.now().format('YYYY-MM-DD HH:mm:ss')
        old_position['address'] = mobile_addr['Address'][0]['label']
        old_position['timestamp'] = ts
        data['POSITION'] = old_position
        # -----------------------INSERT TO POSTGRES-----------------------------------
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|hr|'.find(user) > 0):
            #-- pg = ReadConf().postgres12() server ใหม่ทำงานผ่าน ทดสอบเป็น server เดิมด้วย
            pg = ReadConf().postgres()
            conn = psycopg2.connect(host=pg['server'], port=pg['port'], database=pg['database'], user= user, password= password)
            conn.autocommit = False
            try:
                cursor = conn.cursor()
                json_data = json.dumps(data,ensure_ascii=False,indent=None).encode('utf-8').decode('utf-8')
                qryStr = ReadConf().ins_dn_timestamp()['Query']
                qryStr = qryStr.replace('{{data}}', json_data)
                cursor.execute(qryStr)
                # print(qryStr)
                return json.dumps('{"insert": "successful"}',ensure_ascii=False).encode(encoding='utf-8')
            except (psycopg2.Error) as e:
                return json.dumps({'login': e.pgerror, 'company': '', 'status': ''}, indent=" ",
                                ensure_ascii=False).encode(encoding='utf-8')
            finally:
                if conn is not None:
                    conn.commit()
                    conn.close()
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')
