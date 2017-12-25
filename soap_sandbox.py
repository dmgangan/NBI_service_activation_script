
import requests
from requests import *
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import *
from zeep.transports import Transport

user='admin'
password='manager'
session = Session()
session.auth = HTTPBasicAuth(user, password)

#Path to WDSL file should be indicated
client = Client('cpeService.xml',transport=Transport(session=session))

mg_id=2
t_id=8004
v_id=24
request_data = {
    'cpeId': {
        'managedGroupId': mg_id,
        'subscriberId': t_id,
    },
	'vlanIdToUpdate':v_id,
    'backhauling': {
        'name': 'ICMP',
        'cpeSideIPAddressSource': 'PROFILE',
    }}
a=input('Add/Delete?: ')
try:
    if a=='d':
        response = client.service.cpeDeleteBHfromVR(**request_data)
    elif a=='a':
        response = client.service.cpeAddBHtoVR(**request_data)
except exceptions.Fault as error:
        print (error.message)
except requests.exceptions.ConnectionError as http_error:
    print('Connection problem...')
else: print('Successfuly {} BH:{} from VSAT:{} in VLAN:{}'.format(a,mg_id,t_id,v_id))
print ('\n')
