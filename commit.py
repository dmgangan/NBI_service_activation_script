from  requests import *
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import *
from zeep.transports import Transport

##DEBUG LOGGING##
import logging.config
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

user='admin'
password='manager'
session = Session()
session.auth = HTTPBasicAuth(user, password)

#Path to WDSL file should be indicated
client = Client('cpeService.xml',transport=Transport(session=session))

request_data = {
    'cpeId': {
        'managedGroupId': '2',
        'subscriberId': '3',
    },
	'vlanIdToUpdate':'24',
    'backhauling': {
        'name': 'DSCP 40',
        'cpeSideIPAddressSource': 'PROFILE',
    },}
client.service.cpeAddBHtoVR(**request_data)
