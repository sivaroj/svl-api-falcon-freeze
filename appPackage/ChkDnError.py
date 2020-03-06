import cx_Oracle
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class ChkDnError:
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
                data = collections.OrderedDict()
                qryStr = ReadConf().qryChkDNError()['Query']
                qryStr = qryStr.replace('{{begin_date}}', begin_date)
                qryStr = qryStr.replace('{{end_date}}', end_date)
                cursor.execute(qryStr)
                data = collections.OrderedDict()
                dnError = []
                i = 1
                for row in cursor:
                    t = collections.OrderedDict()
                    t['NO'] = str(i)
                    t['DN_NO'] = row[0]
                    t['TRUCK_NO'] = row[1]
                    t['EMP_NO'] = row[2]
                    t['DRIVER'] = row[3]
                    t['ERROR'] = row[4]
                    t['ERROR_COUNT'] = row[5]
                    t['BH_DN'] = row[6]
                    t['REMARK'] = row[7]
                    dnError.append(t)
                    i = i + 1
                data['ERROR'] = dnError
                cursor.close()
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except cx_Oracle.DatabaseError as e:
                # print(e.args[0].message)
                data = collections.OrderedDict()
                t = collections.OrderedDict()
                t['DN_NO'] = e.args[0].message
                t['TRUCK_NO'] = 'ไม่พบข้อมูล'
                t['EMP_NO'] = 'ไม่พบข้อมูล'
                t['DRIVER'] = 'ไม่พบข้อมูล'
                t['ERROR'] = 'ไม่พบข้อมูล'
                t['ERROR_COUNT'] = 'ไม่พบข้อมูล'
                t['BH_DN'] = 'ไม่พบข้อมูล'
                t['REMARK'] = 'ไม่พบข้อมูล'
                data['ERROR'] = t
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            finally:
                if conn is not None:
                    conn.commit()
                    conn.close()
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')

