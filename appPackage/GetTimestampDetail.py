import psycopg2
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres
from appPackage.ConvertUtil import  ConvertUtil

class GetTimestampDetail:
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
                qryStr = ReadConf().qryTimestampDetail()['Query']
                # แปลง dd/mm/yyyy เป็น yyyy-mm-dd
                bdate = ConvertUtil.dateBEtoAD(self, begin_date)
                edate = ConvertUtil.dateBEtoAD(self, end_date)
                # parameter = {'begin_date': bdate, 'end_date': edate}
                qryStr = qryStr.replace('{{begin_date}}',bdate)
                qryStr = qryStr.replace('{{end_date}}', edate)
                cursor.execute(qryStr)
                records = cursor.fetchone()
                if records is None:
                    data = []
                else:
                    data = records[0]
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except psycopg2.Error as e:
                return json.dumps({'Error': e.pgerror}).encode('utf-8')
                data['error'] = e.args[0].message
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            finally:
                if conn is not None:
                    conn.commit()
                    conn.close()
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')
