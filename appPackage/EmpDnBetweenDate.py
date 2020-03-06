import cx_Oracle
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class EmpDnBetweenDate:
    def __init__(self):
        pass

    def get_data(self, user, password, begin_date, end_date, emp_no):
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
                qryStr = ReadConf().qryEmpDnBetweenDate()['Query']
                parameters = {'begin_date': begin_date, 'end_date': end_date, 'emp_no': emp_no}
                cursor.execute(qryStr, parameters)
                data = collections.OrderedDict()
                empInMonth = []
                for row in cursor:
                    t = collections.OrderedDict()
                    t['DN_DATE'] = row[0]
                    t['DN_NO'] = row[1]
                    t['JOB_NO'] = row[2]
                    t['SOURCE'] = row[3]
                    t['DESTINATION'] = row[4]
                    empInMonth.append(t)
                data['DN'] = empInMonth
                cursor.close()
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except cx_Oracle.DatabaseError as e:
                print(e.args[0].message)
                data['ERROR'] = e.args[0].message
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            finally:
                if conn is not None:
                    conn.commit()
                    conn.close()
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')
