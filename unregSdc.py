import requests
import logging
import os
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


    
# instantiate Logger
logging.basicConfig()
alfred = logging.getLogger("Remove_SDC_Script")

################################################
## Check for environment variables
## If appropriate environment variables do not exist
## log error to loggin library and exit
####################################################

if "HOST_IP" in os.environ:
    server = os.getenv("HOST_IP")
else:
    alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, REMOVE_SDC_IP = <IP address of SDC to remove>")
    exit()

if "USER" in os.environ:
    user = os.getenv("USER")
else:
    alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, REMOVE_SDC_IP = <IP address of SDC to remove>")
    exit()

if "PASSWORD" in os.environ:    
    password = os.getenv("PASSWORD")
else:
    alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, REMOVE_SDC_IP = <IP address of SDC to remove>")
    exit()
    
if "REMOVE_SDC_IP" in os.environ:
    removeIP = os.getenv("REMOVE_SDC_IP")
else:
    alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, REMOVE_SDC_IP = <IP address of SDC to remove>")
    exit()

# build URLs
keyURL = server + "/api/login"
sdcURL = server + "/api/types/Sdc/instances"

# start Session
_session = requests.Session()

# make key call and receive authorization token
token = _session.get(keyURL, auth=HTTPBasicAuth(user, password), verify=False)

# ensure response code is 200
# exit if code not 200
# report error via logging mechanism
if  token.status_code != 200:
    alfred.error("The process exited with a {} status".format(token.status_code))
    alfred.error("The error message states: {}".format(token.content))
    exit()


# Add authorization token to session
_session.auth = HTTPBasicAuth('', token.json())

# get list of SDCs
res = _session.get(sdcURL)

# Status code checking
if  res.status_code != 200:
    alfred.error("The process exited with a {} status".format(res.status_code))
    alfred.error("The error message states: {}".format(res.content))
    exit()

# Print length of SDC List
alfred.info("There are {} SDCs registered before execution".format(len(res.content)))



# find id of SDC by looping through list of SDCs
# returned from ScaleIO
sdcId = None

for i in res.json():
    if i['sdcIp'] == removeIP:
        sdcId = i["id"]
        # ensure SDC is not connected to MDM
        if i["mdmConnectionState"] == "Connected":
            alfred.error("The SDC with IP {} is connected to the MDM. Cannot unregister.".format(removeIP))
            exit()
        # exit loop
        break
        
# Exit script if we do not find matching SDC to IP address
# found in environment variables
if sdcId == None:
    alfred.error("Can't find an SDC with IP {}".format(removeIP))
    exit()

# unregister SDC
sdcUnregisterSdcURL = server + "/api/instances/Sdc::" + sdcId + "/action/removeSdc"
res = _session.post(sdcUnregisterSdcURL)

if  res.status_code != 200:
    alfred.error("The process exited with a {} status".format(res.status_code))
    alfred.error("The error message states: {}".format(res.content))
    exit()

# Log final HTTP status with logging mechanism
alfred.info("The process exited with a {} status".format(res.status_code))
alfred.info("The error message states: {}".format(res.content))





