import cx_Oracle
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class AllTonKM:
    def __init__(self):
        pass

    def get_data(self, user, password, begin_date, end_date):
        ora = ReadConf().ora()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|hr|'.find(user) > 0):
            conn = None
            data = {}
            try:
                dsn_tns = cx_Oracle.makedsn(ora['server'], ora['port'], ora['service'])
                conn = cx_Oracle.connect(ora['user'], ora['password'], dsn_tns
                                         , encoding="UTF-8")
                conn.autocommit = False
                cursor = conn.cursor()
                cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY'")
                cursor.callproc('tonkm_package.new_payment_lh', [begin_date, end_date])
                qryStr = ReadConf().qryAllTonKM()['Query']
                cursor.execute(qryStr)
                data = []
                for row in cursor:
                    t = collections.OrderedDict()
                    t['DN_ORDER'] = row[0]
                    t['TRUCK_NO'] = row[1]
                    t['EMP_NO'] = row[2]
                    t['DRIVER_NAME'] = row[3]
                    t['DN_DATE'] = row[4]
                    t['DN_NO'] = row[5]
                    t['PRODUCT'] = row[6]
                    t['SOURCE_POINT'] = row[7]
                    t['RECEIVER'] = row[8]
                    t['WEIGHT'] = row[9]
                    t['DISTANCE'] = row[10]
                    t['KM_ADJ'] = row[11]
                    t['TON_KM_AMT'] = row[12]
                    t['ENGINE_TYPE'] = row[13]
                    t['FUEL_RATE'] = row[14]
                    t['FUEL_QUAN'] = row[15]
                    t['MULTIDROP'] = row[16]
                    t['DIFFICULTY'] = row[17]
                    t['TRANS_REMARK'] = row[18]
                    t['REMARK'] = row[19]
                    data.append(t)
                cursor.close()
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
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')

