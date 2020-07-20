import json
import collections
import psycopg2
import cx_Oracle
from .readConf import ReadConf
from appPackage.login_Postgres import Login_Postgres

class EmpLHWeekly:
    def get_data(self, user, password, id_card, emp_no=''):
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|line|hr|'.find(user) > 0):
            try:
                ora = ReadConf().ora()
                dsn_tns = cx_Oracle.makedsn(ora['server'], ora['port'], ora['service'])
                ora_conn = cx_Oracle.connect(ora['user'], ora['password'], dsn_tns
                                             , encoding="UTF-8")
                ora_conn.autocommit = False
                ora_cursor = ora_conn.cursor()
                ora_cursordtl = ora_conn.cursor()

                # ---------------- หา emp_no ถ้าส่ง บัตรประชาชนมา --------------------
                if type(id_card) != type(None):
                    qry_emp = 'select e.emp_no ,e.name||\' \'||e.surname as emp_name from employee e where e.social_no = :id_card and e.status=:status'
                    ora_cursor.execute(qry_emp,{'id_card': id_card, 'status':'A'})
                    ora_cursor.execute(qry_emp)
                    row = ora_cursor.fetchone()
                    qry_emp_no = row[0]
                    qry_emp_name = row[1]
                else:
                    qry_emp = 'select e.emp_no ,e.name||\' \'||e.surname as emp_name from employee e where e.emp_no = :emp_no and e.status=:status'
                    ora_cursor.execute(qry_emp, {'emp_no': emp_no, 'status': 'A'})
                    ora_cursor.execute(qry_emp)
                    row = ora_cursor.fetchone()
                    qry_emp_no = emp_no
                    qry_emp_name = row[1]

                # ----------------- query insert emp_lh_weekly_api ---------------
                ora_cursor.callproc('svl_api.prepare_emp_lh_weekly',[qry_emp_no])
                # ------------------query emp_lh_weekly in detail ----------------
                qryStr = ReadConf().weekly_sum()['Query']
                qryStrDtl = ReadConf().weekly_detail()['Query']
                ora_cursor.execute(qryStr)
                records = ora_cursor.fetchall()
                data = collections.OrderedDict()
                weekly = []
                weekly_sum = collections.OrderedDict()
                i = 1
                for row in records:
                    w = collections.OrderedDict()
                    w['processdate'] = row[0]
                    w['prv_balance'] = row[3]
                    w['sum_fuel_cash'] = row[4]
                    w['sum_bill_fuel'] = row[5]
                    w['sum_adv_cash'] = row[6]
                    w['sum_oth_amount'] = row[7]
                    w['sum_net'] = row[8]
                    w['sum_for_dn'] = row[9]
                    w['weekly_amount'] = row[10]
                    ora_cursordtl.execute(qryStrDtl,{'processdate': row[0], 'emp_no': row[2]})
                    dtl_records = ora_cursordtl.fetchall()
                    dn = []
                    for r in dtl_records:
                        # print('processdate {} type {} dn_date {} dn_no {}'.format(row[0],r[1],r[5],r[4]))
                        t = collections.OrderedDict()
                        t['type'] = r[1]
                        t['truck_no'] = r[3]
                        t['dn_no'] = r[4]
                        t['dn_date'] = r[5]
                        t['fuel_cash'] = r[7]
                        t['clear_cash'] = r[8]
                        t['advance_cash'] = r[9]
                        t['express'] = r[10]
                        t['net'] = r[11]
                        dn.append(t)
                    w['dn'] = dn
                    # weekly_sum['processdate'] =w
                    weekly.append(w)
                    i = i + 1
                    if i > 5:
                        break
                # ----------------------------------------------------------------
                data['emp_no'] = qry_emp_no
                data['emp_name'] = qry_emp_name
                data['weekly'] = weekly
                ora_cursor.close()
                ora_cursordtl.close()
                return json.dumps(data, indent=" ", ensure_ascii=False).encode('utf-8')
            except psycopg2.Error as e:
                return json.dumps({'Error': e.pgerror}).encode('utf-8')
            finally:
                if ora_conn is not None:
                    ora_conn.commit()
                    ora_conn.close()
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode('utf-8')

