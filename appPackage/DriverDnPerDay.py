import cx_Oracle
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class DriverDnPerDay:

    def __init__(self):
        pass

    def get_data(self, user, password, begin_date, end_date, secure_id):
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
                conn.autocommit = False
                cursor = conn.cursor()
                data = collections.OrderedDict()
                qryStr = "select emp_no,social_no,name||' '||surname,tel from employee where status = 'A' and social_no='" + secure_id + "'"
                cursor.execute(qryStr)
                row = cursor.fetchone()
                emp_no = row[0]
                if not emp_no.strip():
                    emp_no = ' '
                data['emp_no'] = row[0]
                data['id_card'] = row[1]
                data['driver'] = row[2]
                data['tel'] = row[3]
                mmyy = end_date[3:]
                cursor.callproc('tonkm_package.QRY_ALLOWANCE_BY_EMP', [emp_no, mmyy])
                qryStr = ReadConf().qryDNperDay()['Query']
                cursor.execute(qryStr, {'begin_date': begin_date, 'end_date': end_date})
                empInMonth = []
                total_load_noload = 0.0
                fuel_NGV = 0.0
                fuel_Diesel = 0.0
                NGV_USED = 0.0
                DIESEL_USED = 0.0
                total_multidrop = 0.0
                total_km_load = 0.0
                total_km_noload = 0.0
                total_difficulty = 0.0
                adj_distance = ''
                for row in cursor:
                    t = collections.OrderedDict()
                    t['dn_no'] = row[0]
                    t['destination'] = []
                    dist = row[6].strip().split('\n')
                    t['destination'] = dist
                    t['multidrop'] = row[10]
                    total_multidrop = total_multidrop + row[10]
                    t['difficulty'] = row[11]
                    total_difficulty = total_difficulty + row[11]
                    t['truck_no'] = row[5]
                    t['load_noload'] = row[1]
                    total_load_noload += row[1]
                    t['fuel_quan'] = row[2]
                    t['fuel_unit'] = row[4]
                    t['fuel_used'] = row[12]
                    t['km_load'] = row[8]
                    t['km_noload'] = row[9]
                    if row[3] == 'N':
                        fuel_NGV = round(fuel_NGV + row[2], 3)
                        NGV_USED = round(NGV_USED + row[12], 3)
                    else:
                        fuel_Diesel = round(fuel_Diesel + row[2], 3)
                        DIESEL_USED = round(DIESEL_USED + row[12], 3)
                    t['remark'] = row[13]
                    if row[13] != 'good':
                        adj_distance = 'รอปรับปรุงระยะทาง'

                    empInMonth.append(t)
                    total_km_load = total_km_load + float(row[8])
                    total_km_noload = total_km_noload + float(row[9])
                '''data['emp'].append(empInMonth)'''
                data['Multidrop'] = total_multidrop
                data['Difficulty'] = total_difficulty
                data['Load_noload'] = round(total_load_noload, 2)
                data['NGV'] = fuel_NGV
                data['NGV_used'] = NGV_USED
                data['Diesel'] = fuel_Diesel
                data['Diesel_used'] = DIESEL_USED
                data['total_km_load'] = round(total_km_load, 3)
                data['total_km_noload'] = round(total_km_noload, 3)
                data['adj_distance'] = adj_distance
                data['DN'] = empInMonth
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

