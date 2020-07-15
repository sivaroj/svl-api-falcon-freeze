from appPackage.login_Postgres import Login_Postgres
from appPackage.MAP import Nostra
# from appPackage.MAP import Here_map
# from appPackage.MAP import convertTool as ctool
import json
# import collections


class TruckPositionDtl:
    def get_data(self, user, password, vehicles):
        login = Login_Postgres(user=user, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|hr|line'.find(user) > 0):
            vehicles = json.loads(Nostra.BusNowDtl(vehicles).decode('utf-8'))
            return json.dumps(vehicles, indent=" ", ensure_ascii=False).encode('utf-8')
        else:
            return json.dumps({'login': 'สิทธิการเข้าถึงข้อมูลถูกจำกัด'}).encode(('utf-8'))
