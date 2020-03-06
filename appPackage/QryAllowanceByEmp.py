import cx_Oracle
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class QryAllowanceByEmp:
    def __init__(self):
        pass

    def get_data(self, user, password, begin_date, end_date, emp_no):
        ora = ReadConf().ora()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|hr|'.find(user) > 0):
            conn = None
            data = {}
            mmyyyy = end_date[3:]
            try:
                dsn_tns = cx_Oracle.makedsn(ora['server'], ora['port'], ora['service'])
                conn = cx_Oracle.connect(ora['user'], ora['password'], dsn_tns
                                         , encoding="UTF-8")
                conn.autocommit = False
                cursor = conn.cursor()
                cursor2 = conn.cursor()
                cursor3 = conn.cursor()
                params = {'begin_date': begin_date, 'end_date': end_date}
                cursor.callproc('tonkm_package.QRY_ALLOWANCE_BY_EMP', [emp_no, mmyyyy])
                qryFuelUsed = ReadConf().qryFuelUsed()['Query']
                cursor.execute(qryFuelUsed, params)
                row = cursor.fetchone()
                ngvUsed = row[0]
                dieselUsed = row[1]
                qryStr = ReadConf().qryAllowanceByEmp1()['Query']
                cursor.execute(qryStr, params)
                data = collections.OrderedDict()
                dn = []
                t = collections.OrderedDict()
                for row in cursor:
                    t = collections.OrderedDict()
                    t['EMP_NO'] = row[0]
                    t['WORK_DATE'] = begin_date + ' - ' + end_date
                    t['DRIVER'] = row[1]
                    t['TEL'] = row[2]
                    t['NATIONAL_NO'] = row[3]
                    t['TOTAL_DN'] = row[4]
                    t['KM_ADJ_LOAD'] = row[5]
                    t['KM_ADJ_NOLOAD'] = row[6]
                    t['TON_KM_AMT'] = row[7]
                    t['FUEL_NGV'] = row[8]
                    t['FUEL_DIESEL'] = row[9]
                    t['NGV_USED'] = ngvUsed
                    t['DIESEL_USED'] = dieselUsed
                    t['MULTIDROP'] = row[10]
                    t['DIFFICULTY'] = row[11]
                data['TOTAL'] = t
                """ -------------Loop 2 summary By DN  ------------------------ """
                qryStr2 = ReadConf().qryAllowanceByEmp2()['Query']
                cursor2.execute(qryStr2, params)
                adj_distance = '-'
                for row2 in cursor2:
                    t2 = collections.OrderedDict()
                    t2['DN_NO'] = row2[0]
                    t2['DN_DATE'] = row2[1]
                    t2['TRUCK_NO'] = row2[2]
                    t2['ENGINE_TYPE'] = row2[3]
                    t2['DESTINATION'] = row2[4]
                    t2['TON_KM_AMT'] = row2[5]
                    t2['FUEL_NGV'] = row2[6]
                    t2['FUEL_DIESEL'] = row2[7]
                    t2['FUEL_USED'] = row2[10]
                    t2['MULTIDROP'] = row2[8]
                    t2['DIFFICULTY'] = row2[9]
                    """--------------Loop 3  แสดง DN  detail ------------"""
                    qryStr3 = ReadConf().qryAllowanceByEmp3()['Query']
                    qryStr3 = qryStr3.replace('{{dn_no}}', row2[0])
                    cursor3.execute(qryStr3, params)
                    dn_detail = []
                    for row3 in cursor3:
                        t3 = collections.OrderedDict()
                        t3['DN_ORDER'] = row3[0]
                        t3['PRODUCT'] = row3[1]
                        t3['START_PLACE'] = row3[2]
                        t3['TO_PLACE'] = row3[3]
                        t3['WEIGHT'] = row3[4]
                        t3['KM_ADJ'] = row3[5]
                        t3['TON_KM_AMT'] = row3[6]
                        t3['FUEL_QUAN'] = row3[7]
                        t3['FUEL_UNIT'] = row3[8]
                        t3['MULTIDROP'] = row3[9]
                        t3['DIFFICULTY'] = row3[10]
                        t3['TRANS_REMARK'] = row3[11]
                        t3['REMARK'] = row3[12]
                        t3['ADJ_DISTANCE'] = row3[13]
                        if row3[13] == 'adj_distance':
                            adj_distance='รอปรับปรุงระยะทาง'
                        dn_detail.append(t3)
                    t2['ADJ_DISTANCE'] = adj_distance
                    t2['ROUTE'] = dn_detail
                    dn.append(t2)
                data['DN'] = dn
                cursor.close()
                cursor2.close()
                cursor3.close()
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

