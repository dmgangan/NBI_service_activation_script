
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
request_data = {|
    'id': {
        'managedGroupId': mg_id,
        'subscriberId': t_id,
    },}

request_data2 = {
        'managedGroupId': mg_id,
        'lastIndex': l_idx
        }
a=input('Add/Delete?: ')
try:
    response = client.service.getCPEbyID(**request_data)
    response2 = client.service.getCPEsByManagedGroup(**request_data2)
except exceptions.Fault as error:
        print (error.message)
except requests.exceptions.ConnectionError as http_error:
    print('Connection problem...')
else: print('Successfuly:{} '.format(t_id))
if response:
    print (response['vrs']['VR'][0]['vlanId'])
    print (response2)
print ('\n')
