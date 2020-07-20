import psycopg2
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres
from appPackage.ConvertUtil import  ConvertUtil

class GetTimestampByDate:
    def get_data(self,user,password,begin_date,end_date):
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|line|hr|'.find(user) > 0):
            conn = None
            try:
                pg = ReadConf().postgres()
                conn = psycopg2.connect(host=pg['server'], port=pg['port'], database=pg['database'], user=user,
                                        password=password)
                cursor = conn.cursor()
                qryStr = ReadConf().qryTimestampByDate()['Query']
                # แปลง dd/mm/yyyy เป็น yyyy-mm-dd
                bdate = ConvertUtil.dateBEtoAD(self, begin_date)
                edate = ConvertUtil.dateBEtoAD(self, end_date)
                parameter = {'begin_date': bdate, 'end_date': edate}
                cursor.execute(qryStr,parameter)
                records = cursor.fetchall()
                data = []
                dn=collections.OrderedDict()
                dn=[]
                for row in records:
                    # t = collections.OrderedDict()
                    # t['emp_no'] = row[0]
                    # t['driver'] = row[1]
                    # t['tel'] = row[2]
                    # t['dn_date'] = row[3]
                    # t['dn_no'] = row[4]
                    # t['source_point'] = row[5]
                    # t['in_out'] = row[8]
                    # t['timestamp'] = row[9]
                    # t['address'] = row[10]
                    # t['distance'] = row[11]
                    # t['latitude'] = row[12]
                    # t['longitude'] = row[13]
                    # t['customer_name'] = row[14]
                    # t['customer_addr1'] = row[15]

                    t = collections.OrderedDict()
                    t['emp_no'] = row[0]
                    t['driver'] = row[1]
                    t['tel'] = row[2]
                    t['dn_date'] = row[3]
                    t['dn_no'] = row[4]
                    t['source_point'] = row[5]
                    t['in_out'] = row[6]
                    t['timestamp'] = row[7]
                    t['address'] = row[8]
                    t['distance'] = row[9]
                    t['latitude'] = row[10]
                    t['longitude'] = row[11]
                    t['customer_name'] = row[12]
                    t['customer_addr1'] = row[13]
                    dn.append(t)
                data.append(dn)
                cursor.close()
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except psycopg2.Error as e:
                return json.dumps({'Error': e.pgerror}).encode('utf-8')
                data['emp_no'] = e.args[0].message
                t['driver'] = 'ไม่พบข้อมูล'
                t['tel'] = ''
                t['dn_date'] = ''
                t['dn_no'] = ''
                t['source_point'] = ''
                t['in_out'] = ''
                t['timestamp'] = ''
                t['address'] = ''
                t['distance'] = ''
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            finally:
                if conn is not None:
                    conn.commit()
                    conn.close()
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')
