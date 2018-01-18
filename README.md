# scaleioHelpers

#################
unregSdc.py
################

- Required Imports: logging, requests
- Script requires four environment variables: ScaleIO Gateway IP, Username, Password, IP address of SDC to be removed.
- SDC to be removed must be in a "disconnected" state, otherwise script will exit and report error.
