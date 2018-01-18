import os

################################################
# Check for environment variables
# If appropriate environment variables do not exist
# log error to logging library and exit
####################################################
def checkSetEnvVars (sio):
    if "HOST_IP" in os.environ:
        sio.server = os.getenv("HOST_IP")
    else:
        sio.alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, REMOVE_SDC_IP = <IP address of SDC to remove>")
        exit()

    if "USER" in os.environ:
        sio.user = os.getenv("USER")
    else:
        sio.alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, REMOVE_SDC_IP = <IP address of SDC to remove>")
        exit()

    if "PASSWORD" in os.environ:    
        sio.password = os.getenv("PASSWORD")
    else:
        sio.alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, REMOVE_SDC_IP = <IP address of SDC to remove>")
        exit()

    if "REMOVE_SDC_IP" in os.environ:
        sio.removeIP = os.getenv("REMOVE_SDC_IP")
    else:
        sio.alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, REMOVE_SDC_IP = <IP address of SDC to remove>")
        exit()
    
    sio.keyURL = sio.server + "/api/login"
    sio.sdcURL = sio.server + "/api/types/Sdc/instances"
        
################################################
# checkSdcId
# Function checks for SDC object within response from
# API endpoint: "/api/types/Sdc/instances" that matches
# sio.removeIP <the SDC IP we want to remove from the 
# cluser>
# Arguments: ScaleIO object from unregSdc and response
# object from API endpoing: "/api/types/Sdc/instances"
# Function will return the SDC Id if found, or exit
# if SDC is in a connected state or not found
####################################################
def checkSdcId (sio, res):        
    for i in res.json():
        if i['sdcIp'] == sio.removeIP:
            # ensure SDC is not connected to MDM
            if i["mdmConnectionState"] == "Connected":
                sio.alfred.error("The SDC with IP {} is connected to the MDM. Cannot unregister.".format(sio.removeIP))
                exit()
            else:
                return i["id"]
        # if function has not returned or exited, then we can't find SDC.
        # report error and exit.
        sio.alfred.error("Can't find an SDC with IP {}".format(sio.removeIP))
        exit()

##########################################
# httpErrorCheck
# Checks for 200 status_code
# Exits and reports error if 200 not found
# Requires ScaleIO Object and http response
# from ScaleIO API Endpoint
###########################################
def httpErrorCheck (sio, res):
    if  res.status_code != 200:
        sio.alfred.error("The process exited with a {} status".format(res.status_code))
        sio.alfred.error("The error message states: {}".format(res.content))
        exit()