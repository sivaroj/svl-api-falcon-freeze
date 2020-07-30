import json
from appPackage.MAP import Here_map
import collections
import psycopg2
from appPackage.readConf import ReadConf
from appPackage.login_Postgres import Login_Postgres
from appPackage.ConvertUtil import ConvertUtil
import arrow

def updateDB():
    pg = ReadConf().postgres()
    user= pg['pg_user']
    password = pg['pg_pass']
    try:
        conn = psycopg2.connect(host=pg['server'], port=pg['port'], database=pg['database'], user=user, password=password)
        conn.autocommit = False
        cursor = conn.cursor()
        # 1. read dn_timestamp data->>'STATUS = 'N' -----------------------
        qryStr = "select id,data from dn_timestamp where data->>'STATUS'='N'"
        cursor.execute(qryStr)
        data = cursor.fetchall()
        # -----------------------------------------------------------------
        # 2. for row update data->>'STATUS = 'P' for lock --------------
        qryUpdatStatus =  ReadConf().upd_dn_timestamp_status()['Query']
        for row in data:
            print(row[0],row[1])

        print('update GPS')
        mode = 'fastest;truck;traffic:enabled'
        for row in data:
            source_latlng = row[1]['LAT_LNG']
            # -------------------------- มือถือ --------------------------------------------
            position_latlng = row[1]['POSITION']['latitude']+','+ row[1]['POSITION']['longitude']
            mobile_addr = json.loads(
                Here_map.ReverseGeoCoder(row[1]['POSITION']['latitude'], row[1]['POSITION']['longitude'], '1').decode(
                    'utf-8'))
            distance = json.loads(Here_map.CalculateWayPoint(position_latlng, source_latlng, mode).decode('utf-8'))
            position_far_from = {'distance': distance['distance'], 'travel_time': distance['travel_time']}
            print(position_far_from,mobile_addr)
            # --------------------------- รถบรรทุก ------------------------------------------
            truck_latlng = '{},{}'.format(row[1]['TRUCK_POSITION']['latitude'], row[1]['TRUCK_POSITION']['longitude'])
            truck_addr = json.loads(
                Here_map.ReverseGeoCoder(str(row[1]['TRUCK_POSITION']['latitude']),str(row[1]['TRUCK_POSITION']['longitude']), '1').decode('utf-8'))
            distance = json.loads(Here_map.CalculateWayPoint(truck_latlng, source_latlng, mode).decode('utf-8'))
            truck_far_from = {'distance': distance['distance'], 'travel_time': distance['travel_time']}
            print(truck_far_from,truck_addr)
        # -----------------------------------------------------------------
        cursor.close()
        # -----------------------------------------------------------------
    except (psycopg2.Error) as e:
        print(e.pgerror)
    finally:
        if conn is not None:
            conn.commit()
            conn.close()

if __name__ == '__main__':
    updateDB()