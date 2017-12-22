user='admin'
password='manager'
session = Session()
session.auth = HTTPBasicAuth(user, password)

#Path to WDSL file should be indicated
client = Client('cpeService.xml',transport=Transport(session=session))

request_data = {
    'cpeId': {
        'managedGroupId': '6',
        'subscriberId': '1',
    },
	'vlanIdToUpdate':'24',
    'backhauling': {
        'name': 'test-sctp',
        'cpeSideIPAddressSource': 'PROFILE',
    },}
try:
	response = client.service.cpeAddBHtoVR(**request_data)
except exceptions.Fault as error:
	foo = error
print (foo.message)

print ('\n')
