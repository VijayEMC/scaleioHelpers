import os

################################################
# Check for environment variables, set to variables
# within object
# If appropriate environment variables do not exist
# log error to logging library and exit
####################################################
def checkSetEnvVars (sio):
    if "HOST_IP" in os.environ:
        sio.server = os.getenv("HOST_IP")
    else:
        sio.alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, GUID = <IP address of SDC to remove>, NEWNAME=<new name for SDC>")
        exit()

    if "USER" in os.environ:
        sio.user = os.getenv("USER")
    else:
        sio.alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, GUID = <IP address of SDC to remove>, NEWNAME=<new name for SDC>")
        exit()

    if "PASSWORD" in os.environ:    
        sio.password = os.getenv("PASSWORD")
    else:
        sio.alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, GUID = <IP address of SDC to remove>, NEWNAME=<new name for SDC>")
        exit()

    if "GUID" in os.environ:
        sio.renameGuid = os.getenv("GUID")
    else:
        sio.alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, GUID = <IP address of SDC to remove>, NEWNAME=<new name for SDC>")
        exit()
    
    if "NEWNAME" in os.environ:
        sio.newSdcName = os.getenv("NEWNAME")
    else:
        sio.alfred.error("Error reading Enviornment Variables. Please include the following: HOST_IP = <IP of ScaleIO Gateway>, USER = <username>, PASSWORD = <password>, GUID = <IP address of SDC to remove>, NEWNAME=<new name for SDC>")
        exit()
        
###################################
# Set URLs in SIO object
#################################

def setUrls(sio):
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
        if i['sdcGuid'] == sio.renameGuid:
            return i["id"]
    # if function has not returned or exited, then we can't find SDC.
    # report error and exit.
    sio.alfred.error("Can't find an SDC with guid: {}".format(sio.renameGuid))
    exit(1)

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