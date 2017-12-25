from requests import Session
import requests
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import *
from zeep.transports import Transport

class NbiFunction(object):
    req_cpe_bh = None
    req_cpe_rt = None
    nbi_user='admin'
    nbi_password='manager'
    clinet = None
    nbi_session = None
    def __init__(self,vsat):
        t_id=vsat['t_id']
        t_name=vsat['t_name']
        bh_vlan=vsat['bh_vlan']
        bh_name=vsat['bh_name']
        bh_src=vsat['bh_src']
        bh_src_ip=vsat['bh_src_ip']
        is_route=vsat['is_route']
        t_rt_ip=vsat['t_rt_ip']
        t_rt_msk=vsat['t_rt_msk']
        t_rt_gw=vsat['t_rt_gw']
        is_service=vsat['is_service']

        self.nbi_session = requests.Session()
        self.nbi_session.auth = HTTPBasicAuth(self.nbi_user, self.nbi_password)
        self.client = Client('cpeService.xml',transport=Transport(session=self.nbi_session))


        req_cpe = {
              'cpeId': {
                  'managedGroupId': '2',
                  'subscriberId': t_id,
              },}
        req_bh = {
            'vlanIdToUpdate': bh_vlan,
            'backhauling': {
                'name': bh_name,
                'cpeSideIPAddressSource': bh_src,},
                    }
        req_rt= {
            'vlanId': bh_vlan,
            'IPv4StaticRoute': {
                'network': t_rt_ip,
                'subnetMask': t_rt_msk,
                'nextHop': t_rt_gw,
                'ipV4Interface': 'LAN',
                'redistribute': 'RIPv2',
                'distributedMetric': '1',},
                    }
        self.req_cpe_bh = dict(req_cpe, **req_bh)
        self.req_cpe_rt = dict(req_cpe, **req_rt)
        print ('Init completed\n')
    def req(self, task):
        task=str(task)
        tasks={
            'addBH':{'reqst':'cpeAddBHtoVR','reqst_data':'req_cpe_bh'},
            'deleteBH':{'reqst':'cpeDeleteBHfromVR','reqst_data':'req_cpe_bh'},
            'addRoute':{'reqst':'cpeAddStaticRouteIPv4','reqst_data':'req_cpe_rt'},
            'deleteRoute':{'reqst':'cpeDeleteStaticRouteIPv4','reqst_data':'req_cpe_rt'}
            }
        if task in tasks.keys():
            try:
                response = getattr(self.client.service, tasks[task]['reqst'])(**getattr(self, tasks[task]['reqst_data']))
            except exceptions.Fault as error:
                raise ValueError(error.message)
            except requests.exceptions.ConnectionError as http_error:
                raise ValueError('Connection problem')
            except:
                raise ValueError('Unexpected problem')

    def addBH(self):
        self.req('addBH')

    def deleteBH(self):
        self.req('deleteBH')

    def addRoute(self):
        self.req('addRoute')

    def deleteRoute(self):
        self.req('deleteRoute')

    def test(self):
        print (self.req_cpe_bh)
def main():
    import pymysql
    conn = pymysql.connect("localhost","root","$SatCom$","soapapp")
    cur = conn.cursor(pymysql.cursors.DictCursor)
    id=str(8004)
    result = cur.execute("SELECT * FROM vsats WHERE t_id = %s", [id])
    vsat = cur.fetchone()

    req = NbiFunction(vsat)
    try:
        req.addBH()
    except Exception as e:
        print (str(e))
if __name__ == '__main__':
    main()
