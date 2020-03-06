import cx_Oracle
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class GetAllDnInMonthByEmp:
    def __init__(self):
        pass

    def get_data(self, user, password, date_of_work, emp_no, id_card):
        conn = None
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
                if type(id_card) != type(None):
                    qryStr = "select emp_no,social_no,name||' '||surname from employee where status = 'A' and social_no='" + id_card + "'"
                else:
                    qryStr = "select emp_no,social_no,name||' '||surname from employee where  emp_no = '" + emp_no + "'"

                cursor.execute(qryStr)
                records = cursor.fetchall()
                for row in records:
                    emp_no = row[0]
                    data['emp_no'] = row[0]
                    data['id_card'] = row[1]
                    data['driver'] = row[2]
                total_amt = 0.0
                total_fuel = 0.0
                """tonkm_package.QRY_ALLOWANCE_BY_EMP(emp_no,mmyyyy)
                   mmyyyy must be 02/2020 format
                """
                mmyyyy = date_of_work
                if len(date_of_work) == 10:
                    mmyyyy = date_of_work[3:]
                cursor.callproc('tonkm_package.QRY_ALLOWANCE_BY_EMP', [emp_no, mmyyyy ])
                qryStr = ReadConf().qryAllDNinMonth()['Query']
                cursor.execute(qryStr)
                records = cursor.fetchall()
                if (len(records) > 0):
                    empDnInMonth = []
                    for row in records:
                        t = collections.OrderedDict()
                        t['mmyy'] = row[0]
                        t['dn_no'] = row[1]
                        t['truck_no'] = row[2]
                        t['load_noload'] = row[3]
                        t['fuel_quan'] = row[4]
                        t['fuel_unit'] = row[5]

                        empDnInMonth.append(t)
                        total_amt += row[3]
                        total_fuel += row[4]
                        '''data['emp'].append(empInMonth)'''
                        data['total_load_noload'] = round(total_amt, 2)
                        data['total_fuel'] = round(total_fuel, 3)
                        data['DN'] = empDnInMonth
                        data['DN'] = empDnInMonth
                else:
                    data = collections.OrderedDict()
                    empDnInMonth = []
                    t = collections.OrderedDict()
                    t['mmyy'] = 'ไม่พบข้อมูล'
                    t['emp_no'] = emp_no
                    empDnInMonth.append(t)
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
