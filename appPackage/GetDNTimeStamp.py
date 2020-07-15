import json
import collections
import psycopg2
from appPackage.readConf import ReadConf
from appPackage.login_Postgres import Login_Postgres

class GetDNTimeStamp:
    def get_data(self, user, password, dn_no):
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|hr|line'.find(user) > 0):
            conn = None
            data = {}
            try:
                pg = ReadConf().postgres()
                conn = psycopg2.connect(host=pg['server'], port=pg['port'], database=pg['database'], user=user,
                                        password=password)
                cursor = conn.cursor()
                qryStr = ReadConf().qryGetDNTimeStamp()['Query']
                qryStr = qryStr.replace('{{dn_no}}', dn_no)
                cursor.execute(qryStr)
                records = cursor.fetchall()
                data = collections.OrderedDict()
                timestamp=[]
                truck_no=""
                emp_no=""

                for row in records:
                    t = collections.OrderedDict()
                    # ----------------------------------------------
                    truck_no = row[1]
                    emp_no = row[2]
                    # -----------------------------------------------
                    t['dn_no'] = row[0]
                    t['source_point'] = row[3]
                    t['source_poing_latlng'] = row[4]
                    t['customer_name'] = row[8]
                    t['customer_address'] = row[9]
                    if row[5] == '1':
                        t['in_out'] = 'เข้า'
                    else:
                        t['in_out'] = 'ออก'
                    t['mobile_data'] = row[6]
                    t['truck_data'] = row[7]
                    timestamp.append(t)
                emp = collections.OrderedDict()
                emp['truck_no'] = truck_no
                emp['emp_no'] = emp_no
                data['truck_driver'] = emp
                data['timestamp'] = timestamp
                cursor.close()
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except psycopg2.ConnectionException as e:
                # print(e.args[0].message)
                data['dn_no'] = 'Database error'
                data['truck_no'] = 'ไม่พบข้อมูล'
                data['emp_no'] = 'ไม่พบข้อมูล'
                data['source_point'] = 'ไม่พบข้อมูล'
                data['source_point_lat_lng'] = 'ไม่พบข้อมูล'
                data['in_out'] = 'ไม่พบข้อมูล'
                data['mobile_data'] = 'ไม่พบข้อมูล'
                data['truck_data'] = 'ไม่พบข้อมูล'
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            finally:
                if conn is not None:
                    conn.commit()
                    conn.close()
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')



