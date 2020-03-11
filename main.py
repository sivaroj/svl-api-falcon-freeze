from wsgiref import simple_server
import falcon
import json
import base64
from appPackage import Login_Postgres
from appPackage import GetSumLh_dn
from appPackage import GetSumSubLh_dn
from appPackage import GetSumProduct
from appPackage import GetSumSubProduct
from appPackage import GetSumFactoryProduct
from appPackage import GetCusOrder
from appPackage import GetReceivers
from appPackage import GetSendDocument
from appPackage import GetTrucksPerDay
from appPackage import GetDNRoundTrips
from appPackage import GetDNRoundTripDetail
from appPackage import GetEmpInMonth
from appPackage import GetAllDnInMonthByEmp
from appPackage import GetEmpWorksBetweenDate
from appPackage import DriverDnPerDay
from appPackage import ChkDnError
from appPackage import QryAllowanceByEmp
from appPackage import AllTonKM
from appPackage import RouteForTimestamp
from appPackage import RouteForTimestampDn
from appPackage import EmpDnBetweenDate
from appPackage.MAP import Here_map
from appPackage import TruckPosition
from appPackage import DNTimestamp


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


class Get_Sum_LH_dn(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = GetSumLh_dn.GetSumLH_dn.get_data(self,user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class Get_Sum_Sub_Lh_dn(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data =  GetSumSubLh_dn.get_data(self,user=username, password=password, work_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class Get_Sum_Product(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data =  GetSumProduct.get_data(self,user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class Get_Sum_Sub_Product(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = GetSumSubProduct.get_data(self,user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class Get_Sum_Factory_Product(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data =  GetSumFactoryProduct.get_data(self,user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class Get_Cus_Order(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = GetCusOrder.get_data(self, user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date')


class Get_Receivers(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = GetReceivers.get_data(self, user=username, password=password, dn_date=dn_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require work_date parameter.')


class Get_Send_Document(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = GetSendDocument.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_20, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class Get_Trucks_Per_Day(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = GetTrucksPerDay.get_data(self, user=username, password=password, dn_date=work_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class Get_DN_Round_Trip(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = GetDNRoundTrips.get_data(self, user=username, password=password, dn_no=dn_no)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require dn_no parameter.')


class Get_DN_Round_Trip_Detail(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = GetDNRoundTripDetail.get_data(self, user=username, password=password, dn_no=dn_no)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require dn_no parameters')


class Get_Emp_In_Month(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = GetEmpInMonth.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)


class Get_All_Dn_In_Month_By_Emp(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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


class Get_Emp_Works_Between_Date(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = GetEmpWorksBetweenDate.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class Driver_DN_Per_Day(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = DriverDnPerDay.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date, secure_id=secure_id)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class Check_DN_Error(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = ChkDnError.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class Qry_Allowance_By_Emp(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = QryAllowanceByEmp.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date, emp_no=emp_no)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date emp_no parameters.')


class All_Ton_KM(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = AllTonKM.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class Route_For_Timestamp(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = RouteForTimestamp.get_data(self, user=username, password=password, begin_date=begin_date, end_date=end_date, id_card=id_card)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date parameters.')


class Route_For_Timestamp_Dn(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = RouteForTimestampDn.get_data(self, user=username, password=password, dn_no=dn_no)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require dn_no parameter.')


class Emp_Dn_Between_Date(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

    def on_get(self, req, resp):
        username, password = getUserPass(req)
        if (username is None) or (password is None):
            response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: user password')
        else:
            password, emp_no = password.split(':')
            params = dict({})
            for key, value in req.params.items():
                params.update({key: value})
            if ('begin_date' in params) and ('end_date' in params):
                begin_date = params['begin_date']
                end_date = params['end_date']
                data = EmpDnBetweenDate.get_data(self, user=username, password=password, begin_date=begin_date, end_date= end_date, emp_no=emp_no)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require begin_date end_date emp_no parameter.')


class HereReverseGeoLocation(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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


class Truck_Position(object):

    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)

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
                data = TruckPosition.get_data(self, user=username, password=password, vehicles=vehicles)
                response(resp, 'GET, OPTIONS', falcon.HTTP_200, data)
            else:
                response(resp, 'GET, OPTIONS', falcon.HTTP_404, 'error: Require vehicles parameter.')


class DN_Timestamp(object):
    def on_options(sef, req, resp):
        data = json.dumps('').encode('utf-8')
        response(resp, 'POST, OPTIONS', falcon.HTTP_200, data)

    def on_post(self, req, resp, **kwargs):
        username, password = getUserPass(req)
        login = Login_Postgres(user=username, password=password)
        is_login = json.loads(login.login().decode('utf-8'))
        if is_login['login'] == 'True' and ('|csdplan|hrconnect|hr|'.find(username) > 0):
            # jsonParams = json.loads(req.media)
            jsonParams = req.media
            #data = DNTimestamp.put_data(self,jsonParams)
            data = jsonParams
            # response(resp, 'POST, OPTIONS', falcon.HTTP_200, json.dumps(data).encode('utf-8'))
            data = DNTimestamp.put_data(self,data)
            response(resp, 'POST, OPTIONS', falcon.HTTP_201, json.dumps('{"post":"success"}'))
        else:
            response(resp, 'POST OPTIONS', falcon.HTTP_404, 'error: User can not login.')


app = application = falcon.API()
# -----------------------------------------------------------------------
chkUser = Login()
getSumLh_dn = Get_Sum_LH_dn()
getSumSubLh_dn = Get_Sum_Sub_Lh_dn()
getSumProduct = Get_Sum_Product()
getSumSubProduct = Get_Sum_Sub_Product()
getSumFactoryProduct = Get_Sum_Factory_Product()
getCusOrder = Get_Cus_Order()
getReceivers = Get_Receivers()
getSendDocument = Get_Send_Document()
getTrucksPerDay = Get_Trucks_Per_Day()
getDNRoundTrip = Get_DN_Round_Trip()
getDNRoundTripDetail = Get_DN_Round_Trip_Detail()
getEmpInMonth = Get_Emp_In_Month()
getAllDnInMonthByEmp = GetAllDnInMonthByEmp()
getEmpWorksBetweenDate = Get_Emp_Works_Between_Date()
driverDNperDay = Driver_DN_Per_Day()
chkDNError = Check_DN_Error()
qryAllowanceByEmp = Qry_Allowance_By_Emp()
getTonKM = All_Ton_KM()
routeForTimestamp = Route_For_Timestamp()
routeForTimestampDN = Route_For_Timestamp_Dn()
empDnBetweenDate = Emp_Dn_Between_Date()
hereReverseGeoLocation = HereReverseGeoLocation()
hereRouteSummary = HereRouteSummary()
truckPosition = Truck_Position()
dnTimestamp = DN_Timestamp()
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
app.add_route('/api_v3/dnTimestamp', dnTimestamp)
# -----------------------------------------------------------------------
if __name__ == '__main__':
    http = simple_server.make_server('0.0.0.0', 6000, app)
    http.serve_forever()
