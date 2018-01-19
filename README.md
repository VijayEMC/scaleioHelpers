# scaleioHelpers

#################
unregSdc.py
################

- Required Imports: logging, requests, unregSdcLib
- Script requires four environment variables: ScaleIO Gateway IP, Username, Password, IP address of SDC to be removed.Environment variables should be set as: HOST_IP=<IP of ScaleIO Gateway> USER=<username> PASSWORD=<password> REMOVE_SDC_IP=<IP address of SDC to remove> 
- SDC to be removed must be in a "disconnected" state, otherwise script will exit and report error.


#################
renameSdc.py
################

- Required Imports: logging, requests, renameSdcLib
- Script requires five environment variables: ScaleIO Gateway IP, Username, Password, Guid of SDC, and New Name for Sdc to be removed. Environment variables should be set as: HOST_IP=<IP of ScaleIO Gateway> USER=<username> PASSWORD=<password> GUID=<Guid of SDC to remove> NEWNAME=<new name for SDC>
- SDC will be renamed with the given environment variable NEWNAME as its new name.


