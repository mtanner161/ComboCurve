# ComboCurve API Res Monthly Cash Flow and Economic One Liners
# Developed by Michael Tanner
##
# Runs and exports clean csv's for (1) Reserves Category Monthly Cash Flow (2) Individual Well Economics and (3) Forecasted Production (both oil and gas)

# testgit
# import packages
from combocurve_api_v1 import ServiceAccount, ComboCurveAuth
import requests
import numpy as np
import json
import pandas as pd
from requests.models import Response


# connect to service account
service_account = ServiceAccount.from_file(
    ".\king\combocurve\ComboCurve\ext-api-kingoperating2dev-account-key.json\ext-api-kingoperating2dev-account-key.json"
)
api_key = "AIzaSyB8nd5sPJJNGwC94XufF4iliqNyDZHGjw8"  # set API Key
# specific Python ComboCurve authentication
combocurve_auth = ComboCurveAuth(service_account, api_key)

# This code chunk gets the Monthly Cash Flow for given Scenerio
# Call Stack - Get Econ Id

auth_headers = combocurve_auth.get_auth_headers()
# URl econid
url = "https://api.combocurve.com/v1/projects/61a92c8f34254c0013cacf3e/scenarios/61a93338b763c20015f3f68f/econ-runs"

response = requests.request(
    "GET", url, headers=auth_headers
)  # GET request to pull economic ID for next query

jsonStr = response.text  # convert to JSON string
dataObjBetter = json.loads(jsonStr)  # pass to data object - allows for parsing
row = dataObjBetter[0]  # sets row equal to first string set (aka ID)
econId = row["id"]  # set ID equal to variable

print(econId)  # check that varaible is passed correctly

# Reautenticated client
auth_headers = combocurve_auth.get_auth_headers()
# Set new url parsed with updated econID
urlone = (
    "https://api.combocurve.com/v1/projects/61a92c8f34254c0013cacf3e/scenarios/61a93338b763c20015f3f68f/econ-runs/"
    + econId
    + "/monthly-exports"
)

response = requests.request("POST", urlone, headers=auth_headers)  # runs POST request

# same as above chunk, parses JSON string and pull outs econRunID to be passed in next GET request
jsonStr = response.text
dataObjEconRunId = json.loads(jsonStr)
row = dataObjEconRunId
econRunId = row["id"]
print(econRunId)

# Reautenticated client
auth_headers = combocurve_auth.get_auth_headers()
# set new url with econRunID, skipping zero
urltwo = (
    "https://api.combocurve.com/v1/projects/61a92c8f34254c0013cacf3e/scenarios/61a93338b763c20015f3f68f/econ-runs/"
    + econId
    + "/monthly-exports/"
    + econRunId
    + "?skip=0"
)

# same as above, parsing as JSON string
response = requests.request("GET", urltwo, headers=auth_headers)
jsonStr = response.text
print(len(jsonStr))
# print(jsonStr)
dataObj = json.loads(jsonStr)
