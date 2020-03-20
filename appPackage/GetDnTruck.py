import psycopg2
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class GetDnTruck:
    def __init__(self):
        pass

    def get_data(self, user, password, dn_date):
        conn = None
        pg = ReadConf().postgres()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True':
            SQL_JOB = ReadConf().qryDnTrucks()['Query']
            SQL_DETAIL = ReadConf().qryCoilsOnTruck()['Query']
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
            try:
                conn = psycopg2.connect(host=pg['server'], port=pg['port'], database=pg['database'],
                                        user=user, password=password)
                cursor = conn.cursor()
                cursor2 = conn.cursor()
                parameters = {'dn_date': dn_date}
                cursor.execute(SQL_JOB, parameters)
                truckArray = []
                for row in cursor:
                    t = collections.OrderedDict()
                    t['COMPANY'] = row[0]
                    t['TRUCK'] = row[1]
                    t['TRUCK_OWNER'] = row[2]
                    t['COILS'] = row[3]
                    t['WEIGHT'] = row[4]
                    t['HAVECANCEL'] = row[5]
                    parameter_coil = {'dn_date': dn_date, 'company': row[0], 'car_regis_no': row[1]}
                    cursor2.execute(SQL_DETAIL, parameter_coil)
                    dtl = cursor2.fetchone()
                    t['DETAILS'] = dtl
                    truckArray.append(t)
                cursor2.close()
                cursor.close()
                return json.dumps(truckArray, indent=" ", ensure_ascii=False).encode('utf-8')
            except psycopg2.Error as e:
                return json.dumps({'Error': e.pgerror}).encode('utf-8')
            finally:
                if conn is not None:
                    conn.close()
        else:
            return json.dumps({'login':is_login['login']}).encode('utf-8')
