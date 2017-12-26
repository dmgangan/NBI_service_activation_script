from requests import Session
import requests
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import *
from zeep.transports import Transport

class NbiFunction(object):
    req_cpe_bh = None
    req_cpe_rt = None
    req_en_bh = None
    req_ds_bh = None
    req_add_sla_m = {'cpe':None}
    req_add_sla_s = {'cpe':None}
    req_add_rtn_m = {'cpe':None}
    req_add_rtn_s = {'cpe':None}
    nbi_user='admin'
    nbi_password='manager'
    clinet = None
    nbi_session = None
    info_flash = None
    def __init__(self,cpe):

        self.nbi_session = requests.Session()
        self.nbi_session.auth = HTTPBasicAuth(self.nbi_user, self.nbi_password)
        self.client = Client('cpeService.xml',transport=Transport(session=self.nbi_session))

        req_cpe = {
              'cpeId': {
                  'managedGroupId': cpe['managedGroupId'],
                  'subscriberId': cpe['subscriberId'],
              },}
        req_bh = {
            'vlanIdToUpdate': cpe['VRvlanId'],
            'backhauling': {
                'name': cpe['BHName'],
                'cpeSideIPAddressSource': cpe['BHcpeSideIPAddressSource'],
                'cpeSideIPAddressValue':cpe['BHcpeSideIPAddressValue']},
                    }
        req_rt = {
            'vlanId': cpe['VRvlanId'],
            'IPv4StaticRoute': {
                'network': cpe['RouteNetwork'],
                'subnetMask': cpe['RouteSubnetMask'],
                'nextHop': cpe['RouteNextHop'],
                'ipV4Interface': 'LAN',
                'redistribute': 'RIPv2',
                'distributedMetric': '1',},
                    }
        req_bh1 = {
            'vlanIdToUpdate':cpe['VRvlanId'],
            'vr':{
                'vlanId':cpe['VRvlanId'],
                'enableBackhauling':'SET_BY_MANAGED_GROUP'
                }}

        req_bh2 = {
            'vlanIdToUpdate':cpe['VRvlanId'],
            'vr':{
                'vlanId':cpe['VRvlanId'],
                'enableBackhauling':'DISABLE'
                }}
        req_sla_main = { 'slaName':cpe['slaName']}
        req_sla_sec = { 'slaName':cpe['slaNameBL']}
        req_rtn_main = { 'rtnClassifierName':cpe['rtnClassifierName']}
        req_rtn_sec = { 'rtnClassifierName':cpe['rtnClassifierNameBL']}

        self.req_cpe_bh = dict(req_cpe, **req_bh)
        self.req_cpe_rt = dict(req_cpe, **req_rt)
        self.req_en_bh = dict(req_cpe, **req_bh1)
        self.req_ds_bh = dict(req_cpe, **req_bh2)
        self.req_add_sla_m['cpe']=dict(req_cpe, **req_sla_main)
        self.req_add_sla_s['cpe']=dict(req_cpe, **req_sla_sec)
        self.req_add_rtn_m['cpe']=dict(req_cpe, **req_rtn_main)
        self.req_add_rtn_s['cpe']=dict(req_cpe, **req_rtn_main)
        print ('Init completed...\n')

    def req(self, task, safe=None):
        task=str(task)
        tasks={
            'addBH':{'reqst':'cpeAddBHtoVR','reqst_data':'req_cpe_bh'},
            'deleteBH':{'reqst':'cpeDeleteBHfromVR','reqst_data':'req_cpe_bh'},
            'addRoute':{'reqst':'cpeAddStaticRouteIPv4','reqst_data':'req_cpe_rt'},
            'deleteRoute':{'reqst':'cpeDeleteStaticRouteIPv4','reqst_data':'req_cpe_rt'},
            'ebableBH':{'reqst':'cpeModifyVR','reqst_data':'req_en_bh'},
            'disableBH':{'reqst':'cpeModifyVR','reqst_data':'req_ds_bh'},
            'setSLAm':{'reqst':'modifyCPE','reqst_data':'req_add_sla_m'},
            'setSLAs':{'reqst':'modifyCPE','reqst_data':'req_add_sla_s'},
            'setRTNm':{'reqst':'modifyCPE','reqst_data':'req_add_rtn_m'},
            'setRTNs':{'reqst':'modifyCPE','reqst_data':'req_add_rtn_s'}
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

    def enableBH(self):
        self.req('ebableBH')

    def disableBH(self):
        self.req('disableBH')

    def addSLAm(self):
        self.req('setSLAm')

    def addSLAs(self):
        self.req('setSLAs')

    def addRTNm(self):
        self.req('setRTNm')

    def addRTNs(self):
        self.req('setRTNs')

    def test(self):
        print (self.req_cpe_bh)

class NbiGetFunction(object):

    nbi_user='admin'
    nbi_password='manager'
    clinet = None
    nbi_session = None
    info_flash = None

    def __init__(self):
        self.nbi_session = requests.Session()
        self.nbi_session.auth = HTTPBasicAuth(self.nbi_user, self.nbi_password)
        self.client = Client('cpeService.xml',transport=Transport(session=self.nbi_session))

    def getCpebyId(self,cpe):
        request_cpe = {
            'id': {
                'managedGroupId': cpe['managedGroupId'],
                'subscriberId': cpe['subscriberId'],
            },}
        request_route = {
                'cpeId':
                {'managedGroupId': cpe['managedGroupId'],
                'subscriberId': cpe['subscriberId']},
                'vlanId':cpe['VRvlanId']}
        cpe_data = self.client.service.getCPEbyID(**request_cpe)
        cpe_route = self.client.service.getCPEStaticRouteIPv4(**request_route)
        return_data = {}
        return_data['subscriberId'] = cpe_data['cpeId']['subscriberId']
        return_data['description'] = cpe_data['description']
        return_data['managedGroupId'] = cpe_data['cpeId']['managedGroupId']
        return_data['macAddress'] = cpe_data['macAddress']
        return_data['slaName'] = cpe_data['slaName']
        return_data['slaNameBL'] = None
        return_data['rtnClassifierName'] = cpe_data['rtnClassifierName']
        return_data['rtnClassifierNameBL'] = None
        return_data['operationalState'] = cpe_data['operationalState']
        return_data['authorization'] = cpe_data['authorization']
        return_data['VRvlanId'] = cpe_data['vrs']['VR'][0]['vlanId']
        return_data['VRsubscriberPublicIpAddress'] = cpe_data['vrs']['VR'][0]['ipv4']['subscriberPublicIpAddress']
        return_data['VRipv4Prefix'] = cpe_data['vrs']['VR'][0]['ipv4']['ipv4Prefix']
        return_data['VRenableBackhauling'] = cpe_data['vrs']['VR'][0]['enableBackhauling']
        return_data['BHName'] = cpe_data['vrs']['VR'][0]['backhaulings']['Backhauling'][0]['name']
        return_data['BHcpeSideIPAddressSource'] = cpe_data['vrs']['VR'][0]['backhaulings']['Backhauling'][0]['cpeSideIPAddressSource']
        return_data['BHcpeSideIPAddressValue'] = cpe_data['vrs']['VR'][0]['backhaulings']['Backhauling'][0]['cpeSideIPAddressValue']
        if len(cpe_route)>0:
            return_data['RouteNetwork'] = cpe_route[0]['network']
            return_data['RouteSubnetMask'] = cpe_route[0]['subnetMask']
            return_data['RouteNextHop'] = cpe_route[0]['nextHop']
        else:
            return_data['RouteNetwork']= None
            return_data['RouteSubnetMask']= None
            return_data['RouteNextHop'] = None

        return return_data

    def getCPEsByManagedGroup():
        pass


def main():
    cpe={}
    cpe['subscriberId'] = 1002
    cpe['managedGroupId'] = 2
    cpe['VRvlanId'] = '97'
    cpe['BHName'] = 'ICMP'
    cpe['BHcpeSideIPAddressSource'] = 'PROFLE'
    cpe['BHcpeSideIPAddressValue'] = None
    cpe['RouteNetwork'] = '8.8.8.8'
    cpe['RouteSubnetMask'] = '255.255.255.255'
    cpe['RouteNextHop'] = '10.0.0.1'
    cpe['slaName'] = 'SLA_SOAP'
    cpe['slaNameBL'] = 'SLA_test'
    cpe['rtnClassifierName'] = 'RTN'
    cpe['rtnClassifierNameBL'] = 'TEST_RTN'

    print (cpe)

    vsat = NbiFunction(cpe)
    vsat2 = NbiGetFunction()
    result = vsat2.getCpebyId(cpe)
    print (result)
    print ('-SUCCESS-')
if __name__ == '__main__':
    main()
