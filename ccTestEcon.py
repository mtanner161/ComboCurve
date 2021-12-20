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


# Call Stack - Get Econ Id

auth_headers = combocurve_auth.get_auth_headers()
# URl econid
url = "https://api.combocurve.com/v1/projects/61a92c8f34254c0013cacf3e/scenarios/61a93338b763c20015f3f68f/econ-runs"

# URL get monthly production
# url = 'https://api.combocurve.com/v1/monthly-productions?skip=0&take=25'
response = requests.request("GET", url, headers=auth_headers)

jsonStr = response.text
dataObjBetter = json.loads(jsonStr)
row = dataObjBetter[0]
econId = row["id"]

print(econId)

auth_headers = combocurve_auth.get_auth_headers()
urlone = (
    "https://api.combocurve.com/v1/projects/61a92c8f34254c0013cacf3e/scenarios/61a93338b763c20015f3f68f/econ-runs/"
    + econId
    + "/monthly-exports"
)

response = requests.request("POST", urlone, headers=auth_headers)

jsonStr = response.text
dataObjEconRunId = json.loads(jsonStr)
row = dataObjEconRunId
econRunId = row["id"]

auth_headers = combocurve_auth.get_auth_headers()
urltwo = (
    "https://api.combocurve.com/v1/projects/61a92c8f34254c0013cacf3e/scenarios/61a93338b763c20015f3f68f/econ-runs/"
    + econId
    + "/monthly-exports/"
    + econRunId
    + "?skip=0"
)

response = requests.request("GET", urltwo, headers=auth_headers)
jsonStr = response.text
print(len(jsonStr))
print(jsonStr)

print(econRunId)


dataObj = json.loads(jsonStr)
