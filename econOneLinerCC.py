## Economoic One Liner ComboCurve (Single Well)
## Developed by Michael Tanner - King Operating


# packages needed
from types import NoneType
from combocurve_api_v1 import ServiceAccount, ComboCurveAuth
import requests
import json
import pandas as pd
from requests.models import Response
from dotenv import load_dotenv
import os

load_dotenv()

# connect to service account
service_account = ServiceAccount.from_file(
    ".\king\combocurve\ComboCurve\ext-api-kingoperating2dev-account-key.json\ext-api-kingoperating2dev-account-key.json"
)
api_key = os.getenv("API_KEY_PASS")  # set API Key from enviroment variable
# specific Python ComboCurve authentication
combocurve_auth = ComboCurveAuth(service_account, api_key)

# Call stack to get econ oneliner

# set project and scenerioId - GET FROM ComboCurve
projectId = "61a92c8f34254c0013cacf3e"
scenarioId = "61a93338b763c20015f3f68f"

# Auethenticate the client
auth_headers = combocurve_auth.get_auth_headers()
# URl econid
url = (
    "https://api.combocurve.com/v1/projects/"
    + projectId
    + "/scenarios/"
    + scenarioId
    + "/econ-runs"
)

# GET request to pull economic ID for next query
response = requests.request("GET", url, headers=auth_headers)

jsonStr = response.text  # convert to JSON string
dataObjBetter = json.loads(jsonStr)  # pass to data object - allows for parsing
row = dataObjBetter[0]  # sets row equal to first string set (aka ID)
econId = row["id"]  # set ID equal to variable

print(econId)  # check that varaible is passed correctly

# Reautenticated client
auth_headers = combocurve_auth.get_auth_headers()
# set new url with econRunID
urltwo = (
    "https://api.combocurve.com/v1/projects/"
    + projectId
    + "/scenarios/"
    + scenarioId
    + "/econ-runs/"
    + econId
    + "/one-liners"
)

# same as above, parsing as JSON string
response = requests.request("GET", urltwo, headers=auth_headers)
jsonStr = response.text  # loads in string
# loads JSON str into dataObj
dataObj = json.loads(jsonStr)

# create temp varible with dataObj
temp = dataObj[0]
temp2 = temp["output"]  # extract output


# create file pointer and set to write mode
fp = open(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\combocurve\ComboCurve\cleanEconOneLiner.csv",
    "w",
)


## This next section writes a CSV (only the sub JSON is parsed "output" because its a single well - we do not care about well ID)
# writes to CSV headers
for key, value in temp2.items():
    var = key + ", "
    fp.write(var)

# goes to values row
fp.write("\n")

# writes to CSV values
for key, value in temp2.items():
    var = str(value) + ", "
    fp.write(var)

fp.close()  # closes the file pointer and finishes the export to main dir

print("Done")

########################################## Working on passing table to s3 bucket
########

import boto3 as aws
from botocore.config import Config


s3 = aws.resource("s3")
for bucket in s3.buckets.all():
    print(bucket.name)


print("yay")
