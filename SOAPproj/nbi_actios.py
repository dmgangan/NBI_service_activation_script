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
    info_flash = None
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
    def req(self, task, safe=None):
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
                if safe == 'safe':
                    if str(error).startswith('Static route') and str(error).endswith(('does not exist','already exists')):
                        self.info_flash =str(error.message)
                        pass
                    else: raise ValueError(error.message)
                else: raise ValueError(error.message)
            except requests.exceptions.ConnectionError as http_error:
                raise ValueError(tasks[task]['reqst']+': Connection problem')
            except:
                raise ValueError(tasks[task]['reqst']+': Unexpected problem')

    def addBH(self):
        self.req('addBH')

    def deleteBH(self):
        self.req('deleteBH')

    def addRoute(self, safe=None):
        self.req('addRoute',safe)

    def deleteRoute(self,safe=None):
        self.req('deleteRoute',safe)

    def tetraOn(self):
        self.deleteRoute('safe')
        self.addBH()
        self.addRoute('safe')

    def tetraOff(self):
        self.deleteRoute('safe')
        self.deleteBH()
        self.addRoute('safe')

    def test(self):
        print (self.req_cpe_bh)
def main():
    import pymysql
    conn = pymysql.connect("localhost","root","$SatCom$","soapapp")
    cur = conn.cursor(pymysql.cursors.DictCursor)
    for i in range(1,500):
        t_name = str(i)+'VSAT'
        bh_vlan = '24'
        bh_name = str(i)+'BH'
        bh_src = 'PROFILE'
        bh_src_ip = '0.0.0.0'
        is_route = 'YES'
        t_rt_ip = '8.8.8.8'
        t_rt_msk = '255.255.255.255'
        t_rt_gw = '10.0.0.1'
        is_service = 'YES'
        result = cur.execute("INSERT INTO vsats(t_id, t_name, bh_vlan, bh_name, bh_src, bh_src_ip, is_route, t_rt_ip, t_rt_msk, t_rt_gw, is_service) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i, t_name, bh_vlan, bh_name, bh_src, bh_src_ip, is_route, t_rt_ip, t_rt_msk, t_rt_gw, is_service))
    conn.commit()
    cur.close()
if __name__ == '__main__':
    main()
