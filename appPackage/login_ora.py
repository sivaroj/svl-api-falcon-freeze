import cx_Oracle
from .readConf import ReadConf
import json
#-- not use
class login_ora:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def login(self):
        ora = ReadConf.ora()
        conn = None




