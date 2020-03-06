import psycopg2
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class GetSumSubLh_dn:
    def __init__(self):
        pass

    def get_data(self, user, password, work_date):
        pg = ReadConf().postgres()
        conn = None
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True':
            SQL_JOB = ReadConf().qrySumSubLh_dn()['Query']
            try:
                conn = psycopg2.connect(host=pg['server'],port=pg['port'],database=pg['database'],user=user,password=password)
                cursor = conn.cursor()
                if is_login['status'] in ['2', 's']:
                    SQL_JOB = SQL_JOB.replace('{{inner_join_sub}}',
                                              'inner join line_lh_car_regis lg on lg.car_regis = l.car_regis_no and lg.status=\'N\'' +
                                              'and lg.customer_no ~ \'(^' + is_login['company'] + ')\''
                                              )
                    SQL_JOB = SQL_JOB.replace('{{factory}}', '')
                elif is_login['status'] == '1':
                    SQL_JOB = SQL_JOB.replace('{{inner_join_sub}}', '')
                    SQL_JOB = SQL_JOB.replace('{{factory}}', 'and l.customer_no =\'' + is_login['company'] + '\'')
                else:
                    SQL_JOB = SQL_JOB.replace('{{inner_join_sub}}', '')
                    SQL_JOB = SQL_JOB.replace('{{factory}}', '')

                parameters = {'dn_date': work_date}
                cursor.execute(SQL_JOB, parameters)
                dnArray = []
                for row in cursor:
                    t = collections.OrderedDict()
                    t['TOTAL_WEIGHT'] = row[0]
                    t['TOTAL_TRUCKS'] = row[1]
                    t['TOTAL_COILS'] = row[2]
                    t['TOTAL_RECEIVERS'] = row[3]
                    t['TOTAL_DN'] = row[4]
                    dnArray.append(t)
                cursor.close()
                return json.dumps(dnArray, indent=" ", ensure_ascii=False).encode('utf-8')
            except psycopg2.Error as e:
                return json.dumps({'Error': e.pgerror}).encode('utf-8')
            finally:
                if conn is not None:
                    conn.close()
        else:
            return json.dumps({'login':is_login['login']}).encode('utf-8')
