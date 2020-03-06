import psycopg2
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class GetSumFactoryProduct:
    def __init__(self):
        pass

    def get_data(self, user, password, dn_date):
        conn = None
        pg = ReadConf().postgres()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True':
            SQL_JOB = ReadConf().qrySumFactoryProduct()['Query']
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
            parameters = {'dn_date': dn_date}
            try:
                conn = psycopg2.connect(host=pg['server'], port=pg['port'], database=pg['database'],
                                        user=user, password=password)
                cursor = conn.cursor()
                cursor.execute(SQL_JOB, parameters)
                dnArray = []
                for row in cursor:
                    t = collections.OrderedDict()
                    t['CUSTOMER_NO'] = row[0]
                    t['PRODUCT'] = row[1]
                    t['TRUCKS'] = row[4]
                    t['TOTAL_WEIGHT'] = row[2]
                    t['PCT'] = row[3]
                    t['COIL_REMAIN'] = row[5]
                    t['ASSOCIATED'] = row[6]
                    dnArray.append(t)
                cursor.close()
                return json.dumps(dnArray, indent=" ", ensure_ascii=False).encode('utf-8')
            except psycopg2.Error as e:
                return json.dumps({'Error': e.pgerror})
            finally:
                if conn is not None:
                    conn.close()
        else:
            return {'login': 'error'}