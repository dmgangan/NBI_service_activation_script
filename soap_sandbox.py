
import requests
from requests import *
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import *
from zeep.transports import Transport

user='admin'
password='manager'
session = Session()
session.auth = HTTPBasicAuth(user, password)


client = Client('cpeService.xml',transport=Transport(session=session))

mg_id=2
t_id=1002
l_idx=0
vlan=97
request_data = {
    'id': {
        'managedGroupId': mg_id,
        'subscriberId': t_id,
    },}

request_data2 = {
        'managedGroupId': mg_id,
        'lastIndex': l_idx
        }

request_data3 = {
    'cpeId':
        {'managedGroupId': mg_id,
        'subscriberId': t_id},
        'vlanIdToUpdate':vlan,
        'vr':   {
                'vlanId':vlan,
                'enableBackhauling':'SET_BY_MANAGED_GROUP'
                }
        }
request_data4 = {
    'cpeId':
        {'managedGroupId': mg_id,
        'subscriberId': t_id},
        'vlanId':vlan}
a=input('Add/Delete?: ')
try:
    #response = client.service.getCPEbyID(**request_data)
    #response2 = client.service.getCPEsByManagedGroup(**request_data2)
    #response3 = client.service.cpeModifyVR(**request_data3)
    response4 = client.service.getCPEStaticRouteIPv4(**request_data4)
except exceptions.Fault as error:
        print (error.message)
except requests.exceptions.ConnectionError as http_error:
    print('Connection problem...')
else: print('Successfuly:{} '.format(t_id))
#if response3:
    #print (response['vrs']['VR'][0]['vlanId'])
    #print (response2)
print (response4)
print ('\n')
