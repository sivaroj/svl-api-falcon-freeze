from wsgiref import simple_server
import falcon
import json
import base64
from appPackage import Login_Postgres
from appPackage import GetSumLh_dn as gSum
from appPackage import GetSumSubLh_dn as gSumSub
from appPackage import GetSumProduct as gSumPro
from appPackage import GetSumSubProduct as gSumSubPro
from appPackage import GetSumFactoryProduct as gSumFac
from appPackage import GetCusOrder as gCus
from appPackage import GetReceivers as gRec
from appPackage import GetSendDocument as gDoc
from appPackage import GetTrucksPerDay as gTruck
from appPackage import GetDNRoundTrips as gTrip
from appPackage import GetDNRoundTripDetail as gDetail
from appPackage import GetEmpInMonth as gEmp
from appPackage import GetAllDnInMonthByEmp as gAllEmp
from appPackage import GetEmpWorksBetweenDate as gEmpDate
from appPackage import DriverDnPerDay as gDriver
from appPackage import ChkDnError as chkDn
from appPackage import QryAllowanceByEmp as qbyEmp
from appPackage import AllTonKM as Tonkm
from appPackage import RouteForTimestamp as rForTs
from appPackage import RouteForTimestampDn as rForTsDn
from appPackage import EmpDnBetweenDate as eDnDate
from appPackage.MAP import Here_map
from appPackage import TruckPosition as tPos


def response(resp, methods, status, data):
    resp.set_header('Access-Control-Allow-Origin', '*')
    resp.set_header('Access-Control-Allow-Methods', methods)
    resp.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')
    resp.status = status
    resp.body = data


def decodedHeaderAuth(req):
    if req:
        authStr = req.split(' ', 1)
        if authStr[0] == 'Basic':
            try:
                decoded = base64.b64decode(authStr[1]).decode('utf-8')
            except Exception as ex:
                raise falcon.HTTPUnauthorized(
                    title='401 Unauthorized',
                    description='Invalid Authorization Header:: Unable to decode credentials',
                    challenges=None
                )
            try:
                return decoded.split(':', 1)
            except ValueError:
                raise falcon.HTTPUnauthorized(
                    title='401 Unauthorized',
                    description='Invalid Authorization: Unable to decode credentials',
                    challenges=None)

        else:
            return '', ''

    else:
        return 'No authorization'


def getUserPass(req):
    request_header = req.get_header('Authorization')
    if type(request_header)==type(None):
        username = None
        password = None

    else:
        username, password = decodedHeaderAuth(request_header)
    return username, password


class Login(object):
    def __init__(self):
        self.loginProcess = Login_Postgres

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, POST, OPTIONS', falcon.HTTP_200, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        login = Login_Postgres(user=username, password=password)
        data = login.login()
        response(resp, 'GET, POST, OPTIONS', falcon.HTTP_200, data)

    def on_post(self, req, resp):
        username, password = getUserPass(req)
        login = Login_Postgres(user= username, password=password)
        data = login.login()
        response(resp, 'GET, POST, OPTIONS', falcon.HTTP_201, data)


class GetSumLH_dn(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'work_date' in params:
                dn_date =params['work_date']
                data = gSum.GetSumLH_dn.get_data(self,user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class GetSumSubLh_dn(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'work_date' in params:
                dn_date =params['work_date']
                data =  gSumSub.get_data(self,user=username, password=password, work_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class GetSumProduct(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'work_date' in params:
                dn_date =params['work_date']
                data =  gSumPro.get_data(self,user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class GetSumSubProduct(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'work_date' in params:
                dn_date = params['work_date']
                data = gSumSubPro.get_data(self,user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class GetSumFactoryProduct(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'work_date' in params:
                dn_date =params['work_date']
                data =  gSumFac.get_data(self,user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class GetCusOrder(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'work_date' in params:
                dn_date =params['work_date']
                data = gCus.get_data(self, user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date')


class GetReceivers(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'work_date' in params:
                dn_date =params['work_date']
                data = gRec.get_data(self, user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class GetSendDocument(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('begin_date' in params) and ('end_date' in params):
                begin_date = params['begin_date']
                end_date = params['end_date']
                data = gDoc.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_20, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class GetTrucksPerDay(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'work_date' in params:
                work_date = params['work_date']
                data = gTruck.get_data(self, user=username, password=password, dn_date=work_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class GetDNRoundTrip(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'dn_no' in params:
                dn_no = params['dn_no']
                data = gTrip.get_data(self, user=username, password=password, dn_no=dn_no)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require dn_no parameter.')


class GetDNRoundTripDetail(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'dn_no' in params:
                dn_no = params['dn_no']
                data = gDetail.get_data(self, user=username, password=password, dn_no=dn_no)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require dn_no parameters')


class GetEmpInMonth(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('begin_date' not in params) or ( 'end_date' not in params):
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')
            else:
                begin_date = params['begin_date']
                end_date = params['end_date']
                data = gEmp.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)


class GetAllDnInMonthByEmp(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('date_of_work' in params):
                date_of_work = params['date_of_work']
            else:
                date_of_work = None
            if ('emp_no' in params):
                emp_no = params['emp_no']
            else:
                emp_no=None
            if ('id_card' in params):
                id_card = params['id_card']
            else:
                id_card=None
            if type(date_of_work)==type(None) or (type(emp_no)==type(None) and type(id_card)==type(None)):
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require date_of_work emp_no id_card parameters.')
            else:
                data = gAllEmp.get_data(self, user=username, password=password, date_of_work=date_of_work, emp_no=emp_no, id_card=id_card)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)


class GetEmpWorksBetweenDate(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('begin_date' in params) and ('end_date' in params):
                begin_date = params['begin_date']
                end_date = params['end_date']
                data = gEmpDate.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class DriverDNperDay(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            password, secure_id = password.split(':')
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('begin_date' in params) and ('end_date' in params):
                begin_date = params['begin_date']
                end_date = params['end_date']
                data = gDriver.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date, secure_id=secure_id)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class CheckDNError(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('begin_date' in params) and ('end_date' in params):
                begin_date = params['begin_date']
                end_date = params['end_date']
                data = chkDn.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class QryAllowanceByEmp(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('begin_date' in params) and ('end_date' in params) and ('emp_no' in params):
                begin_date = params['begin_date']
                end_date = params['end_date']
                emp_no = params['emp_no']
                data = qbyEmp.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date, emp_no=emp_no)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date emp_no parameters.')


class AllTonKM(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('begin_date' in params) and ('end_date' in params) :
                begin_date = params['begin_date']
                end_date = params['end_date']
                data = Tonkm.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class RouteForTimestamp(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            password, id_card = password.split(':')
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('begin_date' in params) and ('end_date' in params):
                begin_date = params['begin_date']
                end_date = params['end_date']
                data = rForTs.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date, id_card=id_card)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class RouteForTimestampDn(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'dn_no' in params:
                dn_no = params['dn_no']
                data = rForTsDn.get_data(self, user=username, password=password, dn_no=dn_no)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require dn_no parameter.')


class EmpDnBetweenDate(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            password, emp_no = password.split(':')
            print(password,emp_no)
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('begin_date' in params) and ('end_date' in params):
                begin_date = params['begin_date']
                end_date = params['end_date']
                data = eDnDate.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date, emp_no=emp_no)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date emp_no parameter.')


class HereReverseGeoLocation(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('latitude' in params) and ('longitude' in params) and ('acc' in params):
                latitude = params['latitude']
                longitude = params['longitude']
                acc = params['acc']
                data = Here_map.ReverseGeoCoder(latitude, longitude, acc).decode('utf-8')
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require latitude longitude acc parameters.')


class HereRouteSummary(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('origin' in params) and ('destination' in params) and ('transportMode' in params):
                origin = params['origin']
                destination = params['destination']
                transportMode = params['transportMode']
                data = Here_map.RouteSummary(origin=origin, destination=destination,transportMode=transportMode).decode('utf-8')
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require latitude longitude acc parameters.')


class TruckPosition(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_201, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if 'vehicles' in params:
                vehicles = params['vehicles']
                data = tPos.get_data(self, user=username, password=password, vehicles=vehicles)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require vehicles parameter.')


app = application = falcon.API()
# -----------------------------------------------------------------------
chkUser = Login()
getSumLh_dn = GetSumLH_dn()
getSumSubLh_dn = GetSumSubLh_dn()
getSumProduct = GetSumProduct()
getSumSubProduct = GetSumSubProduct()
getSumFactoryProduct = GetSumFactoryProduct()
getCusOrder = GetCusOrder()
getReceivers = GetReceivers()
getSendDocument = GetSendDocument()
getTrucksPerDay = GetTrucksPerDay()
getDNRoundTrip = GetDNRoundTrip()
getDNRoundTripDetail = GetDNRoundTripDetail()
getEmpInMonth = GetEmpInMonth()
getAllDnInMonthByEmp = GetAllDnInMonthByEmp()
getEmpWorksBetweenDate = GetEmpWorksBetweenDate()
driverDNperDay = DriverDNperDay()
chkDNError = CheckDNError()
qryAllowanceByEmp = QryAllowanceByEmp()
getTonKM = AllTonKM()
routeForTimestamp = RouteForTimestamp()
routeForTimestampDN = RouteForTimestampDn()
empDnBetweenDate = EmpDnBetweenDate()
hereReverseGeoLocation = HereReverseGeoLocation()
hereRouteSummary = HereRouteSummary()
truckPosition = TruckPosition()
# -----------------------------------------------------------------------
app.add_route('/api_v3/chkUser', chkUser)
app.add_route('/api_v3/getSumLh_dn', getSumLh_dn)
app.add_route('/api_v3/getSumSubLh_dn', getSumSubLh_dn)
app.add_route('/api_v3/getSumProduct', getSumProduct)
app.add_route('/api_v3/getSumSubProduct', getSumSubProduct)
app.add_route('/api_v3/getSumFactoryProduct', getSumFactoryProduct)
app.add_route('/api_v3/getCusOrder', getCusOrder)
app.add_route('/api_v3/getReceivers', getReceivers)
app.add_route('/api_v3/getSendDocument', getSendDocument)
app.add_route('/api_v3/getTrucksPerDay', getTrucksPerDay)
app.add_route('/api_v3/getDNRoundTrip', getDNRoundTrip)
app.add_route('/api_v3/getDNRoundTrip_detail', getDNRoundTripDetail)
app.add_route('/api_v3/getEmpInMonth', getEmpInMonth)
app.add_route('/api_v3/getAllDnInMonthByEmp', getAllDnInMonthByEmp)
app.add_route('/api_v3/getEmpWorksBetweenDate', getEmpWorksBetweenDate)
app.add_route('/api_v3/driverDNperDay', driverDNperDay)
app.add_route('/api_v3/chkDNError', chkDNError)
app.add_route('/api_v3/qryAllowanceByEmp', qryAllowanceByEmp)
app.add_route('/api_v3/getTonKM', getTonKM)
app.add_route('/api_v3/routeForTimestamp', routeForTimestamp)
app.add_route('/api_v3/routeForTimestampDN', routeForTimestampDN)
app.add_route('/api_v3/empDnBetweenDate', empDnBetweenDate)
app.add_route('/api_v3/reverseGeoLocation', hereReverseGeoLocation)
app.add_route('/api_v3/routeSummary', hereRouteSummary)
app.add_route('/api_v3/truckPositions', truckPosition)
# -----------------------------------------------------------------------
