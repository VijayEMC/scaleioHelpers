import requests
import logging
import os
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import unregSdcLib

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ScaleIO object containing all variables
# Upon instantiation, object will contain all Env Variables
class ScaleIO(object):
    
    def __init__(self):    
        # instantiate Logger
        logging.basicConfig()
        self.alfred = logging.getLogger("Remove_SDC_Script")

        self.server = None
        self.user = None
        self.password = None
        self.removeIP = None
        self.keyURL = None
        self.sdcURL = None
        unregSdcLib.checkSetEnvVars(self)

# create ScaleIO object
sio = ScaleIO()

####################
# start Http Session
#####################
_session = requests.Session()

##############################################
# make key call and receive authorization token
################################################
token = _session.get(sio.keyURL, auth=HTTPBasicAuth(sio.user, sio.password), verify=False)
# Check for http Errors
unregSdcLib.httpErrorCheck(sio, token)

####################################
# Add authorization token to session
#####################################
_session.auth = HTTPBasicAuth('', token.json())

####################
# get list of SDCs
#####################
res = _session.get(sio.sdcURL)
unregSdcLib.httpErrorCheck(sio, res)

##########################
# Print length of SDC List
###########################
sio.alfred.info("There are {} SDCs registered before execution".format(len(res.content)))

#################################################
# find id of SDC by looping through list of SDCs
# returned from ScaleIO
#################################################
sdcId = unregSdcLib.checkSdcId(sio, res)

##################
# unregister SDC
###################
sdcUnregisterSdcURL = sio.server + "/api/instances/Sdc::" + sdcId + "/action/removeSdc"
res = _session.post(sdcUnregisterSdcURL)
unregSdcLib.httpErrorCheck(sio, res)

##############################################
# Log final HTTP status with logging mechanism
################################################
sio.alfred.info("The process exited with a {} status".format(res.status_code))
sio.alfred.info("The error message states: {}".format(res.content))





