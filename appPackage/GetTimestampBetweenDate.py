import psycopg2
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class GetTimestampBetweenDate:
    def get_data(self,user,password,begin_date,end_date,emp_no):
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|line|hr|'.find(user) > 0):
            conn = None
            try:
                pg = ReadConf().postgres()
                conn = psycopg2.connect(host=pg['server'], port=pg['port'], database=pg['database'], user=user,
                                        password=password)
                cursor = conn.cursor()
                qryStr = ReadConf().qryTimestampBetweenDate()['Query']
                parameter = {'begin_date':begin_date, 'end_date':end_date,'emp_no':emp_no}
                cursor.execute(qryStr,parameter)
                records = cursor.fetchall()
                t = collections.OrderedDict()
                data=[]
                for row in records:
                    t = collections.OrderedDict()
                    t['dn_date'] = row[0]
                    t['dn_no'] = row[1]

                    data.append(t)
                cursor.close()
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except psycopg2.Error as e:
                return json.dumps({'Error': e.pgerror}).encode('utf-8')
                data['emp_no'] = e.args[0].message
                t['dn_date'] = 'ไม่พบข้อมูล'
                t['dn_no'] = ''
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            finally:
                if conn is not None:
                    conn.commit()
                    conn.close()
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')
