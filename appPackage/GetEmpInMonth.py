import cx_Oracle
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class GetEmpInMonth:
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
                qryStr = ReadConf().qryDnBetweenDay()['Query']
                parameters = {'begin_date': begin_date, 'end_date': end_date}
                cursor.execute(qryStr, parameters)
                data = collections.OrderedDict()
                empInMonth = []
                i = 1
                for row in cursor:
                    t = collections.OrderedDict()
                    t['no'] = i
                    t['emp_no'] = row[0]
                    t['id_card'] = row[3]
                    t['driver_name'] = row[1]
                    t['dn'] = row[2]
                    empInMonth.append(t)
                    i = i+1
                '''data['emp'].append(empInMonth)'''
                data['drivers'] = empInMonth
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except cx_Oracle.DatabaseError as e:
                '''return (json.dumps({'DN': '-','TON-KM':'-','FUEL-QUAN':'-'}, indent=" ", ensure_ascii=False).encode(
                encoding='utf-8')) '''
                data['driver'] = 'ไม่พบข้อมูล หรือมีปัญหา'
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
