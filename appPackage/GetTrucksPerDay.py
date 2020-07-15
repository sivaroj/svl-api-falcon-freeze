import cx_Oracle
import psycopg2
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class GetTrucksPerDay:

    def get_data(self, user, password, dn_date):
        conn = None
        ora = ReadConf().ora()
        pg = ReadConf().postgres()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True':
            SQL_JOB = ReadConf().qryTrucksPerDay()['Query']
            # '2' = คนเดินตั๋ว ดูได้หลายบริษัทพร้อมกัน # 's' = บริษัทรถร่วม ดูได้เฉพาะบริษัทตัวเอง
            if is_login['status'] in ['2','s']:
                sub = 'and instr(\'{}\',L.supplier_no) >0'.format(is_login['company'])
                SQL_JOB = SQL_JOB.replace('{{inner_join_sub}}',sub)
                SQL_JOB = SQL_JOB.replace('{{factory}}', '')
            elif is_login['status'] == '1':
                # '1' บริษัทว่าจ้างขน ดูได้เฉพาะตัวเอง เช่น SSI TCR
                factory = 'and l.customer_no = \'{}\''.format(is_login['company'])
                SQL_JOB = SQL_JOB.replace('{{inner_join_sub}}', '')
                SQL_JOB = SQL_JOB.replace('{{factory}}', factory)
            elif is_login['status'] =='0':
                # '0' SVL
                SQL_JOB = SQL_JOB.replace('{{inner_join_sub}}', '')
                SQL_JOB = SQL_JOB.replace('{{factory}}', '')
            else:
                return json.dumps({'Error': 'ไม่สามารถดูข้อมูลได้'}).encode('utf-8')
            try:
                dsn_tns = cx_Oracle.makedsn(ora['server'], ora['port'], ora['service'])
                ora_conn = cx_Oracle.connect(ora['user'], ora['password'], dsn_tns
                                             , encoding="UTF-8")
                ora_cursor = ora_conn.cursor()
                parameters = {'dn_date': dn_date}
                ora_cursor.execute(SQL_JOB,parameters)
                data = collections.OrderedDict()
                trucks=[]
                for row in ora_cursor:
                    t = collections.OrderedDict()
                    t['supplier_no']=row[0]
                    t['supplier_name']=row[1]
                    t['total_trucks']= '{}'.format(row[6],'999')
                    t['fh_trucks']= '{}'.format(row[2],'999')
                    t['fh_wgt']='{}'.format(row[3],'999,999D999')
                    t['bh_trucks']='{}'.format(row[4],'999')
                    t['bh_wgt']='{}'.format(row[5],'999')
                    trucks.append(t)
                data['supplier']=trucks
                ora_cursor.close()
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except cx_Oracle.DatabaseError as e:
                return json.dumps({'Error': e.args[0].message}).encode('utf-8')
            finally:
                if ora_conn is not None:
                    ora_conn.close()
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')
