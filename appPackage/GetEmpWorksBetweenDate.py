import cx_Oracle
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class GetEmpWorksBetweenDate:
    def __init__(self):
        pass

    def get_data(self, user, password, begin_date, end_date):
        ora = ReadConf().ora()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and is_login['status'] == '0' or is_login['company'] == 'LTC':
            conn = None
            data={}
            try:
                dsn_tns = cx_Oracle.makedsn(ora['server'], ora['port'], ora['service'])
                conn = cx_Oracle.connect(ora['user'], ora['password'], dsn_tns
                                         , encoding="UTF-8")
                conn.autocommit = False
                cursor = conn.cursor()

                data = collections.OrderedDict()
                qryStr = ReadConf().GetEmpWorksBetweenDate()['Query']
                parameters = {'begin_date': begin_date, 'end_date': end_date}
                cursor.execute(qryStr,parameters)
                data = collections.OrderedDict()
                empInMonth = []
                for row in cursor:
                    t = collections.OrderedDict()
                    t['emp_no'] = row[0]
                    t['id_card'] = row[1]
                    t['driver'] = row[2]
                    t['FH'] = row[3]
                    t['BH'] = row[4]
                    empInMonth.append(t)
                data['drivers'] = empInMonth
                cursor.close()
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except cx_Oracle.DatabaseError as e:
                print(e.args[0].message)
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
