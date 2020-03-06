import psycopg2
import json
import collections
from .readConf import ReadConf
from .login_Postgres import Login_Postgres


class GetSendDocument:
    def __init__(self):
        pass

    def get_data(self, user, password, begin_date, end_date):
        conn = None
        pg = ReadConf().postgres()
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True':
            SQL_JOB = ReadConf().qrySendDocument()['Query']
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
                parameters = {'begin_date': begin_date, 'end_date': end_date}
                cursor.execute(SQL_JOB, parameters)
                sendDocArray = []
                for row in cursor:
                    t = collections.OrderedDict()
                    t['CUSTOMER_NO'] = row[0]
                    t['DN_DATE'] = row[1]
                    t['WGT'] = row[2]
                    t['TRUCK_NO'] = row[3]
                    t['CUS_DOC'] = row[4]
                    t['DEST_REMARK'] = row[5]
                    t['TRACKING_NO'] = row[6]
                    t['SENDING'] = row[7]
                    t['SEND_DATE'] = row[8]
                    t['ETA_RTN'] = row[9]
                    sendDocArray.append(t)
                cursor.close()
                return json.dumps(sendDocArray, indent=" ", ensure_ascii=False).encode('utf-8')
            except psycopg2.Error as e:
                return json.dumps({'Error': e.pgerror}).encode('utf-8')
            finally:
                if conn is not None:
                    conn.close()
        else:
            return json.dumps({'login':is_login['login']}).encode('utf-8')