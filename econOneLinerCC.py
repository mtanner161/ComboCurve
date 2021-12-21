from types import NoneType
from combocurve_api_v1 import ServiceAccount, ComboCurveAuth
import requests
import numpy as np
import json
import pandas as pd
from requests.models import Response


service_account = ServiceAccount.from_file(
    ".\king\combocurve\ComboCurve\ext-api-kingoperating2dev-account-key.json\ext-api-kingoperating2dev-account-key.json"
)
api_key = "AIzaSyB8nd5sPJJNGwC94XufF4iliqNyDZHGjw8"  # set API Key
# specific Python ComboCurve authentication
combocurve_auth = ComboCurveAuth(service_account, api_key)

# Call stack to get econ oneliner

# Auethenticate the client
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
# set new url with econRunID, skipping zero
urltwo = (
    "https://api.combocurve.com/v1/projects/61a92c8f34254c0013cacf3e/scenarios/61a93338b763c20015f3f68f/econ-runs/"
    + econId
    + "/one-liners"
)

# same as above, parsing as JSON string
response = requests.request("GET", urltwo, headers=auth_headers)
jsonStr = response.text
print(len(jsonStr))
# print(jsonStr)
dataObj = json.loads(jsonStr)
print(dataObj)

# create temp varible with dataObj
temp = dataObj[0]
temp2 = temp["output"]  # extract output

df = pd.json_normalize(response.json())
df = df.transpose()
dfNP = df.to_numpy()


# create file pointer and set to write mode
fp = open(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\combocurve\ComboCurve\cleanEconOneLiner.csv",
    "w",
)

# header
fp.write("Output, Value\n")

# loops through each item in
for key, value in temp2.items():
    if type(value) != str and type(value) != NoneType:
        if key == "firstDiscountRoi" or key == "irr":
            fred = key + "," + str(float(value)) + "\n"
            fp.write(fred)
        else:
            fred = key + "," + str(float(value) * 1000) + "\n"
            fp.write(fred)
    elif type(value) == NoneType:
        continue
    else:
        fred = key + "," + value + "\n"

fp.close()

df = pd.json_normalize(response.json())
df = df.transpose()
