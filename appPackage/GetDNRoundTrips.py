import json
import collections
import cx_Oracle
from .readConf import ReadConf
from .login_Postgres import Login_Postgres

class GetDNRoundTrips:
    def __init__(self):
        pass

    def get_data(self, user, password, dn_no):
        print(user,password,dn_no)
        conn = None
        ora = ReadConf().ora()
        pg = ReadConf().postgres()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|hr|'.find(user) > 0):
            conn = None
            try:
                dsn_tns = cx_Oracle.makedsn(ora['server'], ora['port'], ora['service'])
                print(ora['user'],ora['password'])
                conn = cx_Oracle.connect(ora['user'], ora['password'], dsn_tns
                                         , encoding="UTF-8")
                conn.autocommit = False
                cursor = conn.cursor()
                v_source_point = cursor.var(cx_Oracle.STRING)
                v_receiver_point = cursor.var(cx_Oracle.STRING)
                v_dn_chain = cursor.var(cx_Oracle.STRING)
                v_driver = cursor.var(cx_Oracle.STRING)
                v_truck_no = cursor.var(cx_Oracle.STRING)
                v_ton_km = cursor.var(cx_Oracle.NUMBER)
                v_fuel_quan = cursor.var(cx_Oracle.NUMBER)
                data = collections.OrderedDict()
                cursor.callproc('tonkm_package.Json_DNRealtimePayment',
                                [dn_no, v_source_point, v_receiver_point, v_dn_chain, v_driver, v_truck_no, v_ton_km,
                                 v_fuel_quan])
                data['driver'] = v_driver.getvalue()
                data['truck_no'] = v_truck_no.getvalue()
                data['dn_chain'] = v_dn_chain.getvalue()
                data['source_point'] = v_source_point.getvalue()
                data['receiver'] = v_receiver_point.getvalue()
                data['load_noload'] = v_ton_km.getvalue()
                data['fuel_quan'] = v_fuel_quan.getvalue()
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except cx_Oracle.DatabaseError as e:
                # print(e.args[0].message)
                data['driver'] = e.args[0].message
                data['truck_no'] = 'ไม่พบข้อมูล'
                data['dn_chain'] = 'ไม่พบข้อมูล'
                data['source_point'] = 'ไม่พบข้อมูล'
                data['receiver'] = 'ไม่พบข้อมูล'
                data['ton_km'] = 0
                data['fuel_quan'] = 0
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            finally:
                if conn is not None:
                    conn.commit()
                    conn.close()

        else:
            return json.dumps({'login': is_login['login']}).encode('utf-8')