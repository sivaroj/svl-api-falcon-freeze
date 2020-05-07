import psycopg2
from .readConf import ReadConf
import json


class Login_Postgres:
    def __init__(self,user,password):
        self.user = user
        self.password = password

    def login(self):
        pg = ReadConf().postgres()
        conn = None
        try:
            conn = psycopg2.connect(host=pg['server'], port=pg['port'], database=pg['database'], user=self.user, password=self.password)
            cur = conn.cursor()
            cur.execute("""select company,status from loginsvlfirst where username=%(username)s """,
                        {'username': self.user})
            row = cur.fetchone()
            company = row[0]
            status = row[1]
            cur.close()
            return json.dumps({'login': 'True', 'company': company, 'status': status}, indent=" ",
                              ensure_ascii=False).encode(encoding='utf-8')
        except psycopg2.OperationalError as e:
            return json.dumps({'login': e.args[0].split('\n')[0], 'company': '', 'status': ''}, indent=" ",
                              ensure_ascii=False).encode(encoding='utf-8')
        except psycopg2.Error as e:
            return json.dumps({'login': e.pgerror, 'company': '', 'status': ''}, indent=" ",
                              ensure_ascii=False).encode(encoding='utf-8')
        finally:
            if conn is not None:
                conn.close()