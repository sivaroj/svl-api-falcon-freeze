import psycopg2
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class GetCusOrder:
    def __init__(self):
        pass

    def get_data(self,user, password, dn_date):
        conn = None
        pg = ReadConf().postgres()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True':
            SQL_JOB = ReadConf().qryGetCusOrder()['Query']
            SQL_JOB2 = ReadConf().qryGetCusOrderDtl()['Query']
            if is_login['status'] in ['2', 's']:
                inner_join = ' and lg.customer_no ~ \'(^' + is_login['company'] + ')\' '
                SQL_JOB = SQL_JOB.replace('{{inner_join_sub}}',inner_join)
                SQL_JOB = SQL_JOB.replace('{{factory}}', '')
                SQL_JOB2 = SQL_JOB2.replace('{{inner_join_sub}}', inner_join)
                SQL_JOB2 = SQL_JOB2.replace('{{factory}}', '')
            elif is_login['status'] == '1':
                factory = 'and l.customer_no =\'' + is_login['company'] + '\''
                SQL_JOB = SQL_JOB.replace('{{inner_join_sub}}', '')
                SQL_JOB = SQL_JOB.replace('{{factory}}', factory)
                SQL_JOB2 = SQL_JOB2.replace('{{inner_join_sub}}', '')
                SQL_JOB2 = SQL_JOB2.replace('{{factory}}', factory)
            else:
                SQL_JOB = SQL_JOB.replace('{{inner_join_sub}}', '')
                SQL_JOB = SQL_JOB.replace('{{factory}}', '')
                SQL_JOB2 = SQL_JOB2.replace('{{inner_join_sub}}', '')
                SQL_JOB2 = SQL_JOB2.replace('{{factory}}', '')
            try:
                conn = psycopg2.connect(host=pg['server'], port=pg['port'], database=pg['database'],
                                        user=user, password=password)
                cursor = conn.cursor()
                cursor2 = conn.cursor()
                parameters = {'dn_date': dn_date}
                cursor.execute(SQL_JOB, parameters)
                cusOrderArray = []
                for row in cursor:
                    t = collections.OrderedDict()
                    t['COMPANY'] = row[4]
                    t['CUS'] = row[0]
                    t['RECEIVER'] = row[1]
                    t['TRUCKS'] = row[2]
                    t['WEIGHT'] = row[3]
                    if row[0] is None:
                        cus = 'and l.cus is null'
                    else:
                        cus = 'and l.cus = \'' + row[0] + '\''
                    qry_dtl = SQL_JOB2.replace('{{cus}}',cus)
                    parameter_dtl = {'dn_date': dn_date,'receiver': row[1]}
                    cursor2.execute(qry_dtl, parameter_dtl)
                    for row_dtl in cursor2:
                        dtl = row_dtl[0]
                    t['trucks'] = dtl
                    cusOrderArray.append(t)
                cursor.close()
                cursor2.close()
                return json.dumps(cusOrderArray, indent=" ", ensure_ascii=False).encode('utf-8')
            except psycopg2.Error as e:
                return json.dumps({'Error': e.pgerror}).encode('utf-8')
            finally:
                if conn is not None:
                    conn.close()
        else:
            return json.dumps({'login':is_login['login']}).encode('utf-8')
