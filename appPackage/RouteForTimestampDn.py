import cx_Oracle
import psycopg2
import json
import collections
import hashlib
import arrow
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class RouteForTimestampDn:
    def __init__(self):
        self.dn_order = 0

    def check_in_out(self,last_in_out):
        if last_in_out == '0':
            check_in = True
            check_out = False
        if last_in_out == '1':
            check_in = False
            check_out = True
        if last_in_out == '2':
            check_out = False
            if self.dn_order != 99:
                check_out = True



        return check_in, check_out
    def get_data(self, user, password, dn_no, emp_no):
        ora = ReadConf().ora()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|hr|'.find(user) > 0):
            conn = None
            data = {}
            try:

                # ---- 1 หา DN ว่ามีใน postgresql12 dn_timestamp หรือไม่ -------------------------------------
                # ------   1.1 ถ้ามี อ่านค่า dn_timestamp.md5 (ทุก row ต้องมีค่าเท่ากัน)
                # ------   1.2 ถ้าไม่เคยมีมาก่อน คำนวณ md5 จาก dn+':'+dn_date ตั่วอย่าง 2003110093:11/03/2020 นำไปคำนวณค่า md5
                pg = ReadConf().postgres12()  # new server postgresql v 12
                conn =psycopg2.connect(host=pg['server'], port=pg['port'], database=pg['database'], user=user, password=password)
                cursor = conn.cursor()
                qryStr = ReadConf().qry_in_out()['Query']
                qryStr = qryStr.replace('{{dn_no}}', dn_no)
                qryStr = qryStr.replace('{{emp_no}}', emp_no)
                cursor.execute(qryStr)
                result = cursor.fetchone()
                if isinstance(result, type(None)):
                    t = arrow.now()
                    dn_no_date = dn_no+':'+t.format('DD/MM/YYYY')
                    m = hashlib.md5(dn_no_date.encode())
                    md5 = m.hexdigest()
                    last_dn_order = 5
                    last_in_out = '0'
                else:
                    md5 = result[0]
                    last_dn_order = result[1]
                    last_in_out = result[2]

                # ------ 2 หาดำดับเส้นทางลงเวลา ขึ้นสินค้า ลงสินค้า --------------------------------------
                dsn_tns = cx_Oracle.makedsn(ora['server'], ora['port'], ora['service'])
                conn = cx_Oracle.connect(ora['user'], ora['password'], dsn_tns
                                         , encoding="UTF-8")
                conn.autocommit = False
                cursor = conn.cursor()
                cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY'")
                cursor.callproc('tonkm_package.QRY_ALLOWANCE_BY_DN', [dn_no])
                qryStr = ReadConf().qryForTimestamp()['Query']
                cursor.execute(qryStr)
                data = collections.OrderedDict()
                emp = collections.OrderedDict()
                dn = []
                i = 0
                records = cursor.fetchall()
                print(last_dn_order,last_in_out)
                print('total rows : ',len(records))
                for row in records:
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
                    t['MD5'] = md5
                    t['SOURCE_POINT'] = row[9]
                    t['SOURCE_NAME'] = row[10]
                    t['SOURCE_ADDR3'] = row[11]
                    t['LAT_LNG'] = row[12]
                    t['REMARK'] = row[13]
                    # ---- หา max(IN_OUT ของ (postgres12) dn_timestamp.IN_OUT ที่ dn_no และ source_point เท่ากัน
                    #  -- row[7] หมายถึง DN_ORDER
                    if last_in_out == '0':
                        if row[7] == last_dn_order:
                            t['IN'] = True
                            t['OUT'] = False
                        else:
                            t['IN'] = False
                            t['OUT'] = False
                    elif last_in_out == '1':
                        if row[7] < last_dn_order:
                            t['IN'] = False
                            t['OUT'] = False
                        elif row[7] == last_dn_order:
                            t['IN'] = False
                            t['OUT'] = True
                        else:
                            t['IN'] = False
                            t['OUT'] = False
                    elif last_in_out == '2':
                        if row[7] < last_dn_order:
                            t['IN'] = False
                            t['OUT'] = False
                            i = i + 1
                        elif row[7] == last_dn_order:
                            t['IN'] = False
                            t['OUT'] = False
                            i = i + 1
                        elif row[7] > last_dn_order:
                            if i > 0:
                                t['IN'] = True
                                t['OUT'] = False
                                i = 0;
                            else:
                                t['IN'] = False
                                t['OUT'] = False
                    else:
                        t['IN'] = False
                        t['OUT'] = False
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
