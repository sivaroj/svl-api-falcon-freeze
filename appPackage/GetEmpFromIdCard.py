import cx_Oracle
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres

class GetEmpFromIdCard:
    def __init__(self):
        pass

    def get_data(self, user, password, id_card, emp_no=''):
        ora = ReadConf().ora()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and is_login['status'] == '0' or is_login['company'] == 'LTC':
            conn = None
            data = {}
            try:
                dsn_tns = cx_Oracle.makedsn(ora['server'], ora['port'], ora['service'])
                conn = cx_Oracle.connect(ora['user'], ora['password'], dsn_tns
                                         , encoding="UTF-8")
                cursor = conn.cursor()

                if type(id_card) != type(None):
                    qryStr = 'select emp_no,name,surname,social_no from employee where social_no= '+id_card
                    print(qryStr)
                else:
                    qryStr = 'select emp_no,name,surname,social_no from employee where emp_no= ' + emp_no
                    print(qryStr)
                cursor.execute(qryStr)
                data = collections.OrderedDict()
                row = cursor.fetchone()
                data = collections.OrderedDict()
                data['emp_no'] = row[0]
                data['name'] = row[1]+' '+row[2]
                data['id_card'] = row[3]
                cursor.close()
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except cx_Oracle.DatabaseError as e:
                print(e.args[0].message)
                data['emp_no'] = e.args[0].message
                data['name'] = 'ไม่พบข้อมูล'
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            finally:
                if conn is not None:
                    conn.commit()
                    conn.close()
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')
