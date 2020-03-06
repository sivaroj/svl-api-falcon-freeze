import cx_Oracle
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres

class RouteForTimestampDn:
    def __init__(self):
        pass

    def get_data(self, user, password, dn_no):
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
                cursor.callproc('tonkm_package.QRY_ALLOWANCE_BY_DN',[dn_no])
                qryStr = ReadConf().qryForTimestamp()['Query']

                cursor.execute(qryStr)
                data = collections.OrderedDict()
                emp = collections.OrderedDict()
                dn = []
                t = collections.OrderedDict()
                for row in cursor:
                    emp['EMP_NO'] = row[0]
                    emp['ID_CARD'] = row[1]
                    emp['EMP_NAME'] = row[2]
                    t = collections.OrderedDict()
                    t['TRUCK_NO'] = row[3]
                    t['ENERGY_TYPE'] = row[4]
                    t['JOB_NO'] = row[5]
                    t['DN_NO'] = row[6]
                    t['DN_ORDER'] = row[7]
                    t['DN_DATE'] = row[8]
                    t['SOURCE_POINT'] = row[9]
                    t['SOURCE_NAME'] = row[10]
                    t['SOURCE_ADDR3'] = row[11]
                    t['LAT_LNG'] = row[12]
                    t['REMARK'] = row[13]
                    dn.append(t)
                emp['DN'] = dn
                cursor.close()
                return json.dumps(emp, indent=" ", ensure_ascii=False).encode('utf-8')
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
