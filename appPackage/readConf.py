import os
import configparser


class ReadConf():
    def __init__(self):
        self.conf = None
        wk_dir = os.path.dirname(os.path.realpath(__file__))
        # file name must be 'DBClassApp.conf'
        file_name = wk_dir + os.sep + 'DBClassApp.conf'
        self.conf = configparser.ConfigParser()
        self.conf._interpolation = configparser.ExtendedInterpolation()
        self.conf.read(str(file_name), encoding='utf-8')  # if use unicode utf-8

    # ----------------   Postgresql v 12 server 192.168.0.191 -------------------------
    def postgres12(self):
        return {'DB': 'Postgresql', 'server':  self.conf.get('PostgresqlV12', 'server'), 'port': self.conf.get('PostgresqlV12', 'port'),
                'database': self.conf.get('PostgresqlV12', 'database')}

    def ins_dn_timestamp(self):
        msg = self.conf.get('Query', 'ins_dn_timestamp')
        return {'Query': msg }

    def qry_in_out(self):
        return {'Query': self.conf.get('Query', 'qry_in_out')}
    # ------------------------------------------------------------------------------------------
    def postgres(self):
        return {'DB': 'Postgresql', 'server':  self.conf.get('Postgresql', 'server'), 'port': self.conf.get('Postgresql', 'port'),
                'database': self.conf.get('Postgresql', 'database')}

    def ora(self):
        return {'DB': 'Ora', 'server': self.conf.get('Ora', 'server'), 'port': self.conf.get('Ora', 'port'),
                'service': self.conf.get('Ora', 'service'), 'user': self.conf.get('Ora','user'),
                'password': self.conf.get('Ora', 'pass')}

    def qrySumLh_dn(self):
        return {'Query': self.conf.get('Query', 'qrySumLh_dn')}

    def qrySumSubLh_dn(self):
        return {'Query': self.conf.get('Query', 'qrySumSubLh_dn')}

    def qrySumSubProduct(self):
        return {'Query': self.conf.get('Query', 'qrySumSubProduct')}

    def qrySumProduct(self):
        return {'Query': self.conf.get('Query', 'qrySumProduct')}

    def qrySumFactoryProduct(self):
        return {'Query': self.conf.get('Query', 'qrySumFactoryProduct')}

    def qryDnTrucks(self):
        return {'Query': self.conf.get('Query', 'qryDnTrucks')}

    def qryCoilsOnTruck(self):
        return {'Query': self.conf.get('Query', 'qryCoilsOnTruck')}

    def qryGetCusOrder(self):
        return {'Query': self.conf.get('Query', 'qryGetCusOrder')}

    def qryGetCusOrderDtl(self):
        return {'Query': self.conf.get('Query', 'qryGetCusOrderDtl')}

    def qryForReceiver(self):
        return {'Query': self.conf.get('Query', 'qryForReceiver')}

    def qryReceiverDtl(self):
        return {'Query': self.conf.get('Query', 'qryReceiverDtl')}

    def qryForSubReceiver(self):
        return {'Query': self.conf.get('Query', 'qryForSubReceiver')}

    def qrySubReceiverDtl(self):
        return {'Query': self.conf.get('Query', 'qrySubReceiverDtl')}

    def qrySendDocument(self):
        return {'Query': self.conf.get('Query', 'qrySendDocument')}

    def qryTrucksPerDay(self):
        return {'Query': self.conf.get('Query', 'qryTrucksPerDay')}

    def qryDNEmpInMonth(self):
        return {'Query': self.conf.get('Query', 'qryDNEmpInMonth')}

    def qryDnBetweenDay(self):
        return {'Query': self.conf.get('Query', 'qryDnBetweenDay')}

    def qryAllDNinMonth(self):
        return {'Query': self.conf.get('Query', 'qryAllDNinMonth')}

    def qryDNperDayByEmp(self):
        return {'Query': self.conf.get('Query', 'qryDNperDayByEmp')}

    def GetEmpWorksBetweenDate(self):
        return {'Query': self.conf.get('Query', 'GetEmpWorksBetweenDate')}

    def qryChkDNError(self):
        return {'Query': self.conf.get('Query', 'qryChkDNError')}

    def qryAllowanceByEmp1(self):
        return {'Query': self.conf.get('Query', 'qryAllowanceByEmp1')}

    def qryAllowanceByEmp2(self):
        return {'Query': self.conf.get('Query', 'qryAllowanceByEmp2')}

    def qryAllowanceByEmp3(self):
        return {'Query': self.conf.get('Query', 'qryAllowanceByEmp3')}

    def qryFuelUsed(self):
        return {'Query': self.conf.get('Query', 'qryFuelUsed')}

    def qryAllTonKM(self):
        return {'Query': self.conf.get('Query', 'qryAllTonKM')}

    def qryDNperDay(self):
        return {'Query': self.conf.get('Query', 'qryDNperDay')}

    def qryEmpTimestamp(self):
        return {'Query': self.conf.get('Query', 'qryEmpTimestamp')}

    def qryForTimestamp(self):
        return {'Query': self.conf.get('Query', 'qryForTimestamp')}

    def qryEmpDnBetweenDate(self):
        return {'Query': self.conf.get('Query', 'qryEmpDnBetweenDate')}
